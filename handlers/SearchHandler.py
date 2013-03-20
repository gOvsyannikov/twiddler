import webapp2, main
from google.appengine.api import users
from models import *

class SearchHandler(webapp2.RequestHandler):
    def get(self, request):
        user = users.get_current_user()
        request = request.decode("UTF-8")
        if not user:
            self.redirect(users.create_login_url("/")); return

        try:
            my_user = MyUser.all().filter('login', user.user_id()).fetch(1)[0]
        except:
            self.response.set_status(401); return
        my_user._id = my_user.key().id()

        resultUsers = []
        val = 0
        while True:
            profiles = MyUser.all().fetch(199, val)
            if not profiles:
                break
            for profile in profiles:
                if (profile.name and profile.name.find(request) > -1) \
                    or (profile.surname and profile.surname.find(request) > -1) \
                    or (profile.vk_id and profile.vk_id.find(request) > -1) \
                    or (profile.fb_id and profile.fb_id.find(request) > -1):
                    resultUsers.append(profile)
            val += 200

        resultEvents = []
        val = 0
        while True:
            events = MyEvent.all().fetch(199, val)
            if not events:
                break
            for event in events:
                if event.name.find(request) > -1:
                    resultEvents.append(event)
            val += 200

        template_values = {
            'user_id' : my_user._id,
            'user_list' : resultUsers,
            'event_list' : resultEvents,
            'request' : request
        }
        template = main.jinja_environment.get_template('/templates/searchResult.html')
        self.response.out.write(template.render(template_values))



