from __future__ import print_function
import webapp2
from webapp2_extras import routes
from sqlalchemy.orm import scoped_session, sessionmaker, aliased
from sqlalchemy import create_engine
from paste.urlparser import StaticURLParser
from paste.cascade import Cascade
import socket
import models
import json

engine = create_engine('sqlite:///foo.db')
session = scoped_session(sessionmaker(bind=engine))

def warning(*objs):
    print("WARNING: ", *objs, file=sys.stderr)

class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)

class DemoHandler(BaseHandler):
    def get(self):
        demos = session.query(models.Demo).all()
        self.response.write(json.dumps([demo.tojson() for demo in demos]))

    def post(self):
        val = self.request.get('val')
        session.add(models.Demo(val))
        session.commit()

app = webapp2.WSGIApplication([
    webapp2.Route(r'/api/demo', handler=DemoHandler,name='demo-list'),
], debug=True)

def main():
    from paste import httpserver
    httpserver.serve(app,host=socket.gethostbyname(socket.gethostname()), port='5353')

if __name__ == '__main__':
    main()
