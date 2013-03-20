import webapp2, main
from google.appengine.api import users
import datetime
from models import *


class PlanHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url("/")); return

        try:
            my_user = MyUser.all().filter('login', user.user_id()).fetch(1)[0]
        except:
            self.response.set_status(401); return
        my_user._id = my_user.key().id()

        plan_list = []
        for user_plan in my_user.plan:
            curr = MyEvent.get_by_id(int(user_plan))
            curr._id = curr.key().id()
            plan_list.append(curr)

        template_values = {
            'plan_list': plan_list,
            'user_id': my_user._id
        }
        template = main.jinja_environment.get_template('templates/plan.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url("/")); return

        try:
            my_user = MyUser.all().filter('login', user.user_id()).fetch(1)[0]
        except:
            self.response.set_status(401); return

        name = self.request.get('name')
        start_date = self.request.get('start_date')
        start_time = self.request.get('start_time')
        end_date = self.request.get('end_date')
        end_time = self.request.get('end_time')
        status = self.request.get('status')
        info = self.request.get('info')
        event = MyEvent(name=name, info=info, status=int(status))

        date = start_date.split('-')
        time = start_time.split(':')
        mystart = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]))
        date = end_date.split('-')
        time = end_time.split(':')
        myend = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]))

        if myend < mystart:
            self.redirect('/plan'); return

        event.start = mystart
        event.end = myend
        event.put()
        event.login = str(event.key().id())
        event._id = event.key().id()
        my_user.plan.append(event.login)
        my_user.put()
        my_user._id = my_user.key().id()

        self.redirect('/plan')


def try_fetch(x, t):
    try:
        return t(x)
    except:
        return None