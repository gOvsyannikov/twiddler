import webapp2, main
from google.appengine.api import users
import datetime, time
from models import *


class EditHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url("/")); return

        my_user = MyUser.all().filter('login', user.user_id()).fetch(1)[0]
        if not my_user:
            self.response.set_status(401); return
        my_user._id = my_user.key().id()

        template_values = {
            'user' : my_user
        }
        template = main.jinja_environment.get_template('templates/edit.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        web_user = users.get_current_user()
        if not web_user:
            self.redirect(users.create_login_url("/")); return

        user = MyUser.all().filter('login', web_user.user_id()).fetch(1)[0]
        if not user:
            self.response.set_status(401); return
        user._id = user.key().id()

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
            t = time.strptime(birthday, '%Y-%m-%d')
            bd = datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday)
            interval = datetime.datetime.utcnow() - bd
            user.age = int(interval.days / 365)
        else:
            user.birthday = None
            user.age = None

        if info:
            user.info = info
        else:
            user.info = None

        user.put()
        user._id = user.key().id()

        self.redirect('/user/' + str(user._id))