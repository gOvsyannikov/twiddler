import webapp2, main
from google.appengine.api import users
from models import *

class SearchHandler(webapp2.RequestHandler):
    def get(self, request):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url("/")); return

        my_user = MyUser.all().filter('login', user.user_id()).fetch(1)[0]
        if not my_user:
            self.response.set_status(401); return
        my_user._id = my_user.key().id()