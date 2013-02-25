import webapp2, main
from google.appengine.api import users
from models import *

class BookmarksHandler(webapp2.RequestHandler):
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

        bookmark_list = my_user.bookmarks
        user_list = []

        for s in bookmark_list:
            num = try_fetch(s, int)
            t_user = MyUser.get_by_id(num)
            t_user._id = t_user.key().id()
            user_list.append(t_user)

        template_values = {
            'user' : my_user,
            'user_id' : my_user._id,
            'user_list' : user_list
        }

        template = main.jinja_environment.get_template('templates/bookmarks.html')
        self.response.out.write(template.render(template_values))

def try_fetch(x, t):
    try:
        return t(x)
    except:
        return None

