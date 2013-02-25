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
                return

            location = my_user.location

            template_values = {
                'last_seen' : location,
                'user_id' : my_user._id
            }

            template = main.jinja_environment.get_template('/templates/find.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url("/"))

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

        lat = self.request.get('lat')
        lon = self.request.get('lon')

        latI = try_fetch(lat, float)
        lonI = try_fetch(lon, float)

        if latI and lonI and abs(latI) <= 90 and abs(lonI) <= 180:
            my_user.location = lat + ',' + lon #db.GeoPtProperty(latI, lonI)

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
