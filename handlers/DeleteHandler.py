import webapp2
from google.appengine.api import users
from models import *


class DeleteHandler(webapp2.RequestHandler):
    def get(self, event_id):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url("/")); return

        my_user = MyUser.all().filter('login', user.user_id()).fetch(1)[0]
        if not my_user:
            self.response.set_status(401); return
        my_user._id = my_user.key().id()

        if my_user.plan.count(event_id) > 0:
            my_user.plan.remove(str(event_id))
            curr = MyEvent.get_by_id(int(event_id))
            curr.delete()
            my_user.put()
            my_user._id = my_user.key().id()

        self.redirect('/plan')