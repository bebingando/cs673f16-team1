import json
import re

from issue_tracker.serializers import IssueSerializer
from issue_tracker import models as it_models

from channels import Channel
from channels.auth import channel_session_user_from_http, channel_session_user

from .settings import MSG_TYPE_LEAVE, MSG_TYPE_ENTER, NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS, MSG_TYPE_MUTED
from .models import Room
from .utils import get_room_or_error, catch_client_error
from .exceptions import ClientError


### WebSocket handling ###


# This decorator copies the user from the HTTP session (only available in
# websocket.connect or http.request messages) to the channel session (available
# in all consumers with the same reply_channel, so all three here)
@channel_session_user_from_http
def ws_connect(message):
    # Initialise their session
    message.channel_session['rooms'] = []


# Unpacks the JSON in the received WebSocket frame and puts it onto a channel
# of its own with a few attributes extra so we can route it
# This doesn't need @channel_session_user as the next consumer will have that,
# and we preserve message.reply_channel (which that's based on)
def ws_receive(message):
    # All WebSocket frames have either a text or binary payload; we decode the
    # text part here assuming it's JSON.
    # You could easily build up a basic framework that did this encoding/decoding
    # for you as well as handling common errors.
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("chat.receive").send(payload)


@channel_session_user
def ws_disconnect(message):
    # Unsubscribe from any connected rooms
    for room_id in message.channel_session.get("rooms", set()):
        try:
            room = Room.objects.get(pk=room_id)
            # Removes us from the room's send group. If this doesn't get run,
            # we'll get removed once our first reply message expires.
            room.websocket_group.discard(message.reply_channel)
        except Room.DoesNotExist:
            pass


### Chat channel handling ###


# Channel_session_user loads the user out from the channel session and presents
# it as message.user. There's also a http_session_user if you want to do this on
# a low-level HTTP handler, or just channel_session if all you want is the
# message.channel_session object without the auth fetching overhead.
@channel_session_user
@catch_client_error
def chat_join(message):
    # Find the room they requested (by ID) and add ourselves to the send group
    # Note that, because of channel_session_user, we have a message.user
    # object that works just like request.user would. Security!
    room = get_room_or_error(message["room"], message.user)

    # Send a "enter message" to the room if available
    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        room.send_message(None, message.user, MSG_TYPE_ENTER)

    # OK, add them in. The websocket_group is what we'll send messages
    # to so that everyone in the chat room gets them.
    room.websocket_group.add(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).union([room.id]))
    # Send a message back that will prompt them to open the room
    # Done server-side so that we could, for example, make people
    # join rooms automatically.
    message.reply_channel.send({
        "text": json.dumps({
            "join": str(room.id),
            "title": room.title,
        }),
    })


@channel_session_user
@catch_client_error
def chat_leave(message):
    # Reverse of join - remove them from everything.
    room = get_room_or_error(message["room"], message.user)

    # Send a "leave message" to the room if available
    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        room.send_message(None, message.user, MSG_TYPE_LEAVE)

    room.websocket_group.discard(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).difference([room.id]))
    # Send a message back that will prompt them to close the room
    message.reply_channel.send({
        "text": json.dumps({
            "leave": str(room.id),
        }),
    })


@channel_session_user
@catch_client_error
def chat_send(message):
    # Check that the user in the room
    if int(message['room']) not in message.channel_session['rooms']:
        raise ClientError("ROOM_ACCESS_DENIED")
    # Find the room they're sending to, check perms
    room = get_room_or_error(message["room"], message.user)
    # Intercept the message, check for special key prefixes
    muted_text = parse_for_special_actions(message)
    if muted_text:
        # Send the muted message
        room.send_message(muted_text, message.user, MSG_TYPE_MUTED)
    else:
        # Send the message along
        room.send_message(message["message"], message.user)

def parse_for_special_actions(message):
    def raise_error(alternatives):
        raise ClientError("Invalid parameters used with the {0} command. Requires {1}.".format(command, alternatives))

    def new_issue():
        pattern = re.compile(r".*(title|name)=\'(?P<title>[^\']+)\'")
        match = pattern.match(message_text)
        if match:
            title = match.group('title')
            issue = it_models.Issue(title=title,reporter=message.user)
            issue.save()
            m = "{0} submitted a new issue to the tracker: Issue #{1}, Title: {2}".format(message.user.username, issue.pk, issue.title)
            print m
            return m
        else:
            raise_error("""title='foo'"" or ""name='bar'""")

    def issue_comment():
        pattern = re.compile(r".*issue=(?P<issue_id>[0-9]+).*comment=\'(?P<comment>[^\']+)\'")
        match = pattern.match(message_text)
        if match and len(match.groups()) == 2:
            issue_id = match.group('issue_id')
            comment = match.group('comment')
            issue = it_models.Issue.objects.get(id=issue_id)
            issue_comment = it_models.IssueComment(comment=comment, issue_id=issue, poster=message.user)
            issue_comment.save()
            m = "{0} added a comment to issue #{1}: {2}".format(message.user.username, issue.pk, issue_comment.comment)
            print m
            return m
        else:
            raise_error("""issue=id"" and ""comment='comment text'""")

    def issue_status():
        pattern = re.compile(r".*issue=(?P<id>[0-9]+).*status=\'(?P<status>[^\']+)\'")
        match = pattern.match(message_text)
        if match and len(match.groups()) == 2:
            id = match.group('id')
            status = match.group('status')
            ok_statuses = [s[0] for s in it_models.STATUSES]
            if not status in ok_statuses:
                raise_error("status to be one of: {0}".format(", ".join(ok_statuses)))
            issue = it_models.Issue.objects.get(id=id)
            issue.status = status
            issue.save(update_fields=['status'])
            m = "{0} updated status of issue #{1} to: {2}".format(message.user.username, issue.pk, issue.status)
            print m
            return m
        else:
            raise_error("""issue=id"" and ""status='valid status'""")

    def issue_priority():
        pattern = re.compile(r".*issue=(?P<id>[0-9]+).*priority=\'(?P<priority>[^\']+)\'")
        match = pattern.match(message_text)
        m = None
        if match and len(match.groups()) == 2:
            id = match.group('id')
            priority = match.group('priority')
            ok_priorities = [p[0] for p in it_models.PRIORITIES]
            if not priority in ok_priorities:
                raise_error("priority to be one of: {0}".format(", ".join(ok_priorities)))
            issue = it_models.Issue.objects.get(id=id)
            issue.priority = priority
            issue.save(update_fields=['priority'])
            m = "{0} updated priority of issue #{1} to: {2}".format(message.user.username, issue.pk, issue.priority)
            print m
        else:
            raise_error("""issue=id"" and ""priority='valid priority'""")
        return m

    def issue_type():
        pattern = re.compile(r".*issue=(?P<id>[0-9]+).*type=\'(?P<type>[^\']+)\'")
        match = pattern.match(message_text)
        m = None
        if match and len(match.groups()) == 2:
            id = match.group('id')
            issue_type = match.group('type')
            ok_types = [t[0] for t in it_models.TYPES]
            if not issue_type in ok_types:
                raise_error("type to be one of: {0}".format(", ".join(ok_types)))
            issue = it_models.Issue.objects.get(id=id)
            issue.issue_type = issue_type
            issue.save(update_fields=['issue_type'])
            m = "{0} updated type of issue #{1} to: {2}".format(message.user.username, issue.pk, issue.issue_type)
            print m
        else:
            raise_error("""issue=id"" and ""type='valid type'""")
        return m

    message_text = message["message"]
    command_pattern = re.compile(r"^/[a-zA-Z0-9-]+")
    command_match = command_pattern.match(message_text)
    if command_match:
        command = command_match.group()
        print "Command found in chat input: {0}".format(command)
        if command == "/new-issue":
            return new_issue()
        elif command == "/issue-comment":
            return issue_comment()
        elif command == "/set-issue-status":
            return issue_status()
        elif command == "/set-issue-priority":
            return issue_priority()
        elif command == "/set-issue-type":
            return issue_type()
        else:
            raise ClientError("Invalid command: {0}".format(command))
    else:
        return None

