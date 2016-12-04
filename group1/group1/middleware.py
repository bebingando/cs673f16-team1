from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth import logout
from .settings import EXPIRE_TIME


class SessionSecurityMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            return
        now = datetime.now()

        if 'last_activity_time' not in request.session:
            self.set_last_activity(request.session, now)

        delta = now - self.get_last_activity(request.session)

        expire_session = EXPIRE_TIME

        if delta >= timedelta(seconds=expire_session):
            logout(request)
            context = {'confirm_message': 'Time out! you should log in again!', 'button_desc': 'Sign in'}
            return render(request, 'TimeOut.html', context)
        else:
            self.set_last_activity(request.session, now)

    @staticmethod
    def get_last_activity(session):
        try:
            return datetime.strptime(session['last_activity_time'], '%Y-%m-%dT%H:%M:%S.%f')
        except AttributeError:
            return datetime.now()

    @staticmethod
    def set_last_activity(session, now):
        session['last_activity_time'] = now.strftime('%Y-%m-%dT%H:%M:%S.%f')







