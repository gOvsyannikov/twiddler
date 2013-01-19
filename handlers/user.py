import webapp2, main
from google.appengine.api import users
from models import *

class MainHandler(webapp2.RequestHandler):
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
        age = self.request.get('age')
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

        if age:
            temp = try_fetch(age, int)
            if temp and temp > 0:
                user.age = temp
        else:
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

def try_fetch(x, t):
    try:
        return t(x)
    except:
        return None

