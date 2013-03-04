import webapp2, main
from google.appengine.api import users
from models import *

class BookmarksHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url("/")); return

        my_user = MyUser.all().filter('login', user.user_id()).fetch(1)[0]
        if not my_user:
            self.response.set_status(401); return
        my_user._id = my_user.key().id()

        user_list = []
        for s in my_user.bookmarks:
            t_user = MyUser.get_by_id(int(s))
            t_user._id = t_user.key().id()
            user_list.append(t_user)

        template_values = {
            'user_id' : my_user._id,
            'user_list' : user_list
        }

        template = main.jinja_environment.get_template('templates/bookmarks.html')
        self.response.out.write(template.render(template_values))