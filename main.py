import webapp2, jinja2, os
from handlers.user import *

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

app = webapp2.WSGIApplication([
                                  ('/', FindHandler),
                                  (r'/user/(.*)', ProfileHandler),
                                  ('/edit', EditHandler),
                                  (r'/plan/(.*)', PlanHandler),
                                  (r'/bookmarks/(.*)', BookmarksHandler),
                                  ('/logout', LogoutHandler)
                              ], debug=True)

