import webapp2, main
from google.appengine.api import users
import datetime, time
from models import *

class PlanHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        my_user = None

        if user:
            mas_users = MyUser.all().fetch(200)

            for temp_user in mas_users:
                if user.user_id() == temp_user.login:
                    my_user = temp_user
                    my_user._id = my_user.key().id()
                    break

        if not my_user:
            self.response.set_status(401)
            return

        plan_list = []
        plan_mas = MyEvent.all().fetch(200)
        for curr_plan in plan_mas:
            for user_plan in my_user.plan:
                if int(curr_plan.key().id()) == int(user_plan):
                    plan_list.append(curr_plan)
                    curr_plan._id = curr_plan.key().id()

        template_values = {
            'plan_list' : plan_list,
            'user_id' : my_user._id,
            'user' : user,
            'plan_mas' : plan_mas
        }
        template = main.jinja_environment.get_template('templates/plan.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        user = users.get_current_user()
        my_user = None

        if user:
            mas_users = MyUser.all().fetch(200)

            for temp_user in mas_users:
                if user.user_id() == temp_user.login:
                    my_user = temp_user
                    my_user._id = my_user.key().id()
                    break

        if not my_user:
            self.response.set_status(401)
            return

        name = self.request.get('name')
        start_date = self.request.get('start_date')
        start_time = self.request.get('start_time')
        end_date = self.request.get('end_date')
        end_time = self.request.get('end_time')
        status = self.request.get('status')
        info = self.request.get('info')

        event = MyEvent()
        event.name = name
        event.info = info

        if try_fetch(status, int) != None:
            event.status = int(status)
        else:
            event.status = 1

        start = start_date.split('-')
        time = start_time.split(':')
        mystart = datetime.datetime(int(start[0]), int(start[1]), int(start[2]), int(time[0]), int(time[1]))

        end = end_date.split('-')
        time = end_time.split(':')
        myend = datetime.datetime(int(end[0]), int(end[1]), int(end[2]), int(time[0]), int(time[1]))

        if myend < mystart:
            self.redirect('/plan')

        event.start = mystart
        event.end = myend

        event.put()
        event.login = str(event.key().id())
        event._id = event.key().id()

        my_user.plan.append(event.login)
        my_user.put()

        self.redirect('/plan')

def try_fetch(x, t):
    try:
        return t(x)
    except:
        return None

