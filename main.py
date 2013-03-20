import webapp2, jinja2, os
from handlers.ProfileHandler import *
from handlers.EditHandler import *
from handlers.MainHandler import *
from handlers.BookmarksHandler import *
from handlers.PlanHandler import *
from handlers.DeleteHandler import *
from handlers.SearchHandler import *

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

app = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  (r'/user/(.*)', ProfileHandler),
                                  ('/edit', EditHandler),
                                  ('/plan', PlanHandler),
                                  (r'/plan/(.*)', DeleteHandler),
                                  ('/bookmarks', BookmarksHandler),
                                  ('/logout', LogoutHandler),
                                  (r'/search/(.*)', SearchHandler)
                              ], debug=True)

