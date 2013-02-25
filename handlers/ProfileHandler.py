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

        if not user:
            self.response.set_status(401)
            return

        if not curr_user.user_id() == user.login:
            mark = False

        mas_users = MyUser.all().fetch(200)
        for temp_user in mas_users:
            if temp_user.login == curr_user.user_id():
                c_user = temp_user
                c_user._id = c_user.key().id()
                break

        mark2 = False
        for usr in c_user.bookmarks:
            t_id = try_fetch(usr, int)
            u = MyUser.get_by_id(t_id)
            if u.login == user.login:
                mark2 = True
                break

        template_values = {
            'user' : user,
            'user_id' : c_user._id,
            'mark' : mark,
            'mark2' : mark2
        }
        template = main.jinja_environment.get_template('templates/profile.html')
        self.response.out.write(template.render(template_values))

    def post(self, user_id):
        tid = try_fetch(user_id, int)
        if not tid:
            self.response.set_status(401)
            return
        user = MyUser.get_by_id(tid)
        if not user:
            self.response.set_status(401)
            return

        curr_user = users.get_current_user()

        if not curr_user:
            self.response.set_status(401)
            return

        mas_users = MyUser.all().fetch(200)
        for temp_user in mas_users:
            if temp_user.login == curr_user.user_id():
                c_user = temp_user
                break

        mark2 = False
        for usr in c_user.bookmarks:
            t_id = try_fetch(usr, int)
            u = MyUser.get_by_id(t_id)
            if u.login == user.login:
                mark2 = True
                break
        if not mark2:
            c_user.bookmarks.append(str(tid))
        else:
            c_user.bookmarks.remove(str(tid))
        c_user.put()
        self.redirect('/user/' + str(user_id))

        # user.delete()
        # self.redirect(users.create_logout_url("/"))

def try_fetch(x, t):
    try:
        return t(x)
    except:
        return None