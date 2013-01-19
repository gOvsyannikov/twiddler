import webapp2, jinja2, os
from handlers.user import *

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

app = webapp2.WSGIApplication([
                                  ('/', MainHandler),
                                  (r'/user/(.*)', ProfileHandler),
                                  (r'/edit/(.*)', EditHandler)
                              ], debug=True)

