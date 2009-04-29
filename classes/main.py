#!/usr/bin/env python
# encoding: utf-8
#

import os
import sys
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

path = os.path.dirname(__file__)
sys.path.append(path)

import html

class MainHandler(webapp.RequestHandler):
	def get(self):
		template_values = {}
		path = os.path.join(os.path.dirname(__file__), '..', 'html', 'main.html')
		self.response.out.write(html.sharedHTML.header())
		self.response.out.write(template.render(path, template_values))
		self.response.out.write(html.sharedHTML.footer())
		
class IMRemovalHandler(webapp.RequestHandler):
	def get(self):
		template_values = {}
		path = os.path.join(os.path.dirname(__file__), '..', 'html', 'imremoval.html')
		self.response.out.write(html.sharedHTML.header(u"Mac OS X 輸入法移除工具"))
		self.response.out.write(template.render(path, template_values))
		self.response.out.write(html.sharedHTML.toolbar())
		self.response.out.write(html.sharedHTML.footer())

def main():
	application = webapp.WSGIApplication([
		('/', MainHandler),
		('/imremoval', IMRemovalHandler),
		], debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()
