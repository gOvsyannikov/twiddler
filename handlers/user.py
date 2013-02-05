import webapp2, main
from google.appengine.api import users
import datetime
from models import *

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        my_user = None

        if user:
            mas_users = MyUser.all().fetch(200)
            print len(mas_users)

            for temp_user in mas_users:
                if user.user_id() == temp_user.login:
                    my_user = temp_user
                    my_user._id = my_user.key().id()
                    break

            if not my_user:
                my_user = MyUser()
                my_user.login = user.user_id()
                my_user.email = user.email()
                my_user.put()
                my_user._id = my_user.key().id()
                self.redirect('/edit/' + str(my_user._id))

            template_values = {
                'user' : my_user
            }

            template = main.jinja_environment.get_template('templates/main.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url("/"))

    def post(self):
        self.redirect(users.create_logout_url("/"))



class EditHandler(webapp2.RequestHandler):
    def get(self, user_id):

        curr_user = users.get_current_user()
        mark = True

        tid = try_fetch(user_id, int)
        if not tid:
            self.response.set_status(401)
            return

        user = MyUser.get_by_id(tid)

        if not user:
            self.response.set_status(401)
            return

        if not curr_user.user_id() == user.login:
            mark = False

        template_values = {
            'user' : user,
            'user_id' : user_id,
            'mark' : mark
        }
        template = main.jinja_environment.get_template('templates/edit.html')
        self.response.out.write(template.render(template_values))


    def post(self, user_id):

        tid = try_fetch(user_id, int)
        if not tid:
            self.response.set_status(401)
            return

        user = MyUser.get_by_id(tid)

        if not user:
            self.response.set_status(401)
            return

        name = self.request.get('name')
        surname = self.request.get('surname')
        email = self.request.get('email')
        phone = self.request.get('phone')
        vk = self.request.get('vk')
        fb = self.request.get('fb')
        birthday = self.request.get('birthday')
        info = self.request.get('info')

        if name:
            user.name = name
        else:
            user.name = None

        if surname:
            user.surname = surname
        else:
            user.surname = None

        if email:
            user.email = email
        else:
            user.email = None

        if phone:
            user.phone = phone
        else:
            user.phone = None

        if vk:
            user.vk_id = vk
        else:
            user.vk_id = None

        if fb:
            user.fb_id = fb
        else:
            user.fb_id = None

        if birthday:
            user.birthday = birthday
            dates = birthday.split("-")
            now = datetime.datetime.now()
            age = int(now.year) - int(dates[0])
            if age > 0:
                month = int(now.month) - int(dates[1])
                if month > 0:
                    user.age = age
                elif month == 0:
                    day = int(now.day) - int(dates[2])
                    if day < 0:
                        user.age = age - 1
                    else:
                        user.age = age
                else:
                    user.age = age - 1
        else:
            user.birthday = None
            user.age = None

        if info:
            user.info = info
        else:
            user.info = None

        user.put()

        self.redirect('/user/' + str(user_id))

class ProfileHandler(webapp2.RequestHandler):
    def get(self, user_id):

        curr_user = users.get_current_user()
        mark = True

        tid = try_fetch(user_id, int)
        if not tid:
            self.response.set_status(401)
            return

        user = MyUser.get_by_id(tid)

        if not user:
            self.response.set_status(401)
            return

        if not curr_user.user_id() == user.login:
            mark = False

        template_values = {
            'user' : user,
            'user_id' : user_id,
            'mark' : mark
        }
        template = main.jinja_environment.get_template('templates/profile.html')
        self.response.out.write(template.render(template_values))

    def post(self, user_id):
        tid = try_fetch(user_id, int)
        if not tid:
            self.response.set_status(401)
            return

        user = MyUser.get_by_id(tid)

        if not user:
            self.response.set_status(401)
            return

        user.delete()
        self.redirect(users.create_logout_url("/"))

class PlanHandler(webapp2.RequestHandler):
    def get(self, user_id):
        curr_user = users.get_current_user()

        tid = try_fetch(user_id, int)
        if not tid:
            self.response.set_status(401)
            return

        user = MyUser.get_by_id(tid)

        if not user:
            self.response.set_status(401)
            return

        if not curr_user.user_id() == user.login:
            self.response.set_status(406)
            return

        plan_list = []
        plan_mas = MyEvent.all().fetch(200)
        for curr_plan in plan_mas:
            for user_plan in user.plan:
                if int(curr_plan.key().id()) == int(user_plan):
                    plan_list.append(curr_plan)
                    curr_plan._id = curr_plan.key().id()

        template_values = {
            'plan_list' : plan_list,
            'user_id' : user_id,
            'user' : user,
            'plan_mas' : plan_mas
        }
        template = main.jinja_environment.get_template('templates/plan.html')
        self.response.out.write(template.render(template_values))

    def post(self, user_id):
        curr_user = users.get_current_user()

        tid = try_fetch(user_id, int)
        if not tid:
            self.response.set_status(401)
            return

        user = MyUser.get_by_id(tid)

        if not user:
            self.response.set_status(401)
            return

        if not curr_user.user_id() == user.login:
            self.response.set_status(406)
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
            self.redirect('/plan/' + str(user_id))

        event.start = mystart
        event.end = myend

        event.put()
        event.login = str(event.key().id())
        event._id = event.key().id()

        user.plan.append(event.login)
        user.put()

        self.redirect('/plan/' + str(user_id))

def try_fetch(x, t):
    try:
        return t(x)
    except:
        return None

