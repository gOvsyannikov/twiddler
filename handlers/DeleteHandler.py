import webapp2, main
from google.appengine.api import users
from models import *

class DeleteHandler(webapp2.RequestHandler):
    def get(self, event_id):
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

        for user_plan in my_user.plan:
            if int(event_id) == int(user_plan):
                my_user.plan.remove(str(event_id))
                break

        my_user.put()

        self.redirect('/plan')
