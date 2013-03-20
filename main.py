import webapp2, jinja2, os
from handlers.ProfileHandler import *
from handlers.EditHandler import *
from handlers.MainHandler import *
from handlers.BookmarksHandler import *
from handlers.PlanHandler import *
from handlers.DeleteHandler import *
<<<<<<< HEAD
from handlers.SearchHandler import *
=======
from handlers.FindHandler import *
>>>>>>> b660ab5d9c20d01f81e9e277c35ddf726ff562bf

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

app = webapp2.WSGIApplication([
                                  ('/', FindHandler),
                                  (r'/user/(.*)', ProfileHandler),
                                  ('/edit', EditHandler),
                                  ('/plan', PlanHandler),
                                  (r'/plan/(.*)', DeleteHandler),
                                  ('/bookmarks', BookmarksHandler),
                                  ('/logout', LogoutHandler),
                                  (r'/search/(.*)', SearchHandler)
                              ], debug=True)

