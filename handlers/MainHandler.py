import webapp2, main, math
from google.appengine.api import users
from models import *

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url("/")); return

        try:
            my_user = MyUser.all().filter('login', user.user_id()).fetch(1)[0]
        except:
            my_user = MyUser(login=user.user_id(), email=user.email())
            my_user.put()
            my_user._id = my_user.key().id()
            self.redirect('/edit')
            return
        my_user._id = my_user.key().id()
        user_list = []
        for s in my_user.bookmarks:
            t_user = MyUser.get_by_id(int(s))
            user_list.append(t_user)

        try:
            neighbours = find_neighbours(my_user, 20)
        except:
            neighbours = []

        template_values = {
            'last_seen' : my_user.location,
            'user_id' : my_user._id,
            'neighbours' : neighbours,
            'user_list' : user_list
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

        lat = self.request.get('Lat')
        lon = self.request.get('Lon')
        latI = try_fetch(lat, float)
        lonI = try_fetch(lon, float)
        if latI and lonI and abs(latI) <= 90 and abs(lonI) <= 180:
            my_user.location = lat + ',' + lon
            my_user.lon = lonI
            my_user.lat = latI
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

def find_neighbours(user, radius):
    mylon = user.location.lon
    mylat = user.location.lat
    lon1 = mylon - radius / abs(math.cos(math.radians(mylat)) * 111.0)
    lon2 = mylon + radius / abs(math.cos(math.radians(mylat)) * 111.0)
    lat1 = mylat - (radius / 111.0)
    lat2 = mylat + (radius / 111.0)
    var = 0
    result = []
    while True:
        profiles = MyUser.all().filter('lon >', lon1).fetch(199, var)
        if not profiles:
            break
        for temp in profiles:
            if temp.lon < lon2 and lat2 > temp.lat > lat1 and temp.login != user.login:
                result.append(temp)
        var += 200
    return result