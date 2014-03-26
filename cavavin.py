#from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import os
import webapp2
import cgi

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    
    
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            user_name = "Logged in as: "+ users.get_current_user().nickname()
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            user_name = "Not logged in"

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'user_name': user_name
        }

        template = JINJA_ENVIRONMENT.get_template('formNewProducteur.html')
        self.response.write(template.render(template_values))

class NewProd(webapp2.RequestHandler):
    def post(self):
        template = JINJA_ENVIRONMENT.get_template('prod.html')
        template_values = {
            'nom': cgi.escape(self.request.get('nom')),
            'adresse': cgi.escape(self.request.get('adresse')),
            'tel': cgi.escape(self.request.get('tel')),
            'email': cgi.escape(self.request.get('email')),
            'remarques': cgi.escape(self.request.get('remarques')),
        }
        self.response.write(template.render(template_values))
#        self.response.write('<!doctype html><html><body>You wrote:<pre>')
#        self.response.write(cgi.escape(self.request.get('content')))
#        self.response.write('</pre></body></html>')


application = webapp2.WSGIApplication([
        ('/', MainPage),
        ('/newprod', NewProd)
        ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
