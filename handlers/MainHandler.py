import webapp2, main
from google.appengine.api import users
from models import *

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url("/")); return

        my_user = MyUser.all().filter('login', user.user_id()).fetch(1)[0]
        if not my_user:
            my_user = MyUser(login=user.user_id(), email=user.email())
            my_user.put()
            my_user._id = my_user.key().id()
            self.redirect('/edit/' + str(my_user._id))
            return
        my_user._id = my_user.key().id()

        template_values = {
            'last_seen' : my_user.location,
            'user' : my_user
        }
        template = main.jinja_environment.get_template('/templates/find.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url("/")); return

        my_user = MyUser.all().filter('login', user.user_id()).fetch(1)[0]
        if not my_user:
            self.response.set_status(401); return
        my_user._id = my_user.key().id()

        lat = self.request.get('lat')
        lon = self.request.get('lon')
        latI = try_fetch(lat, float)
        lonI = try_fetch(lon, float)
        if latI and lonI and abs(latI) <= 90 and abs(lonI) <= 180:
            my_user.location = latI + ',' + lonI

        my_user.put()
        self.redirect("/")


class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect(users.create_logout_url("/"))


def try_fetch(x, t):
    try:
        return t(x)
    except:
        return None