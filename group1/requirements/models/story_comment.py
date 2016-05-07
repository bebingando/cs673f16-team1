from django.db import models
from story import Story


class StoryComment(models.Model):
    story = models.ForeignKey(Story)
    title = models.CharField(default='', max_length=1024)
    comment = models.CharField(default='', max_length=1024)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    user = models.CharField(default='', max_length=1024)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'requirements'


def get_comments_for_story(story):
    if story is None:
        return None
    return StoryComment.objects.filter(story_id=story.id)


def get_comment(commentid):
    try:
        return StoryComment.objects.get(id=commentid)
    except Exception:
        return None
    
def get_all_comments():
    return StoryComment.objects.all()

def create_comment(story, fields):
    if story is None:
        return None
    if fields is None:
        return None

    title = fields.get('title', '')
    comment = fields.get('comment', '')
    user = fields.get('user', '')

    commentinstance = StoryComment(
        story=story,
        title=title,
        comment=comment,
        user = user,
    )
    commentinstance.save()
    return commentinstance
