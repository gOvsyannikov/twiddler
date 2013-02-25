import webapp2, main
from google.appengine.api import users
import datetime, time
from models import *

class EditHandler(webapp2.RequestHandler):
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

        template_values = {
            'user' : my_user,
            'user_id' : my_user._id
        }
        template = main.jinja_environment.get_template('templates/edit.html')
        self.response.out.write(template.render(template_values))

    def post(self):

        web_user = users.get_current_user()
        user = None

        if web_user:
            mas_users = MyUser.all().fetch(200)

            for temp_user in mas_users:
                if web_user.user_id() == temp_user.login:
                    user = temp_user
                    user._id = user.key().id()
                    break

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
            #t = time.strptime(birthday, '%Y-%m-%d')
            #bd = datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday, 0,0,0)
            #interval = datetime.datetime.utcnow()-bd
            #days = interval.days

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
        user._id = user.key().id()

        self.redirect('/user/' + str(user._id))

def try_fetch(x, t):
    try:
        return t(x)
    except:
        return None


