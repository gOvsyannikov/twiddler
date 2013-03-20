import webapp2, main
from google.appengine.api import users
from models import *

class ProfileHandler(webapp2.RequestHandler):
    def get(self, user_id):
        curr_user = users.get_current_user()
        mark = True

        tid = try_fetch(user_id, int)
        if not tid:
            self.response.set_status(401)
            return

        user = MyUser.get_by_id(tid)
        user._id = user.key().id()

        if not user:
            self.response.set_status(401)
            return

        if not curr_user.user_id() == user.login:
            mark = False

        c_user = MyUser.all().filter('login', curr_user.user_id()).fetch(1)[0]
        c_user._id = c_user.key().id()

        mark2 = False
        if c_user.bookmarks.count(str(user._id)) > 0:
            mark2 = True

        plan_list = []
        for user_plan in user.plan:
            curr = MyEvent.get_by_id(int(user_plan))
            curr._id = curr.key().id()
            plan_list.append(curr)

        template_values = {
            'user' : user,
            'user_id' : c_user._id,
            'mark' : mark,
            'mark2' : mark2,
            'plan_list' : plan_list
        }
        template = main.jinja_environment.get_template('templates/profile.html')
        self.response.out.write(template.render(template_values))

    def post(self, user_id):
        tid = try_fetch(user_id, int)
        if not tid:
            self.response.set_status(401)
            return
        user = MyUser.get_by_id(tid)
        user._id = user.key().id()

        if not user:
            self.response.set_status(401)
            return

        curr_user = users.get_current_user()

        if not curr_user:
            self.response.set_status(401)
            return

        c_user = MyUser.all().filter('login', curr_user.user_id()).fetch(1)[0]
        c_user._id = c_user.key().id()

        mark2 = False
        if c_user.bookmarks.count(str(user._id)) > 0:
            mark2 = True

        if not mark2:
            c_user.bookmarks.append(str(tid))
        else:
            c_user.bookmarks.remove(str(tid))
        c_user.put()
        self.redirect('/user/' + str(user_id))


def try_fetch(x, t):
    try:
        return t(x)
    except:
        return None