#!/usr/bin/env python
# encoding: utf-8
#

import os
import sys
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext.webapp import template

path = os.path.dirname(__file__)
sys.path.append(path)

import html

class OneKeyItem(db.Model):
	user = db.UserProperty()
	service_name = db.StringProperty()
	title = db.StringProperty()
	place_holder_encoding = db.StringProperty()
	action = db.StringProperty()
	action_url = db.StringProperty()
	input_prompt = db.StringProperty()
	input_prompt_description = db.StringProperty()
	tracker = db.StringProperty()

class ItemList():
	def html_list(self):
		items = OneKeyItem.all()
		html = u"<ul>"
		for item in items:
			title = item.title
			item_html = u'<li class="draggable">' + title + u'</li>\n'
			html = html + item_html
		html = html + u"</ul>"
		return html


class OneKeyItemListHandler(webapp.RequestHandler):
	def get(self):
		template_values = {}
		path = os.path.join(os.path.dirname(__file__), '..', 'html', 'onekey_itemlist.html')
		self.response.out.write(html.sharedHTML.header())
		self.response.out.write(template.render(path, template_values))
		self.response.out.write(html.sharedHTML.toolbar())
		self.response.out.write(html.sharedHTML.footer())
		
class AddOneKeyItemHandler(webapp.RequestHandler):
	def get(self):	
		template_values = {}
		path = os.path.join(os.path.dirname(__file__), '..', 'html', 'onekey_add.html')
		self.response.out.write(html.sharedHTML.header())
		self.response.out.write(template.render(path, template_values))
		self.response.out.write(html.sharedHTML.toolbar())
		self.response.out.write(html.sharedHTML.footer())
	def post(self):
		service_name = self.request.get("service_name")
		title = self.request.get("title")
		action = self.request.get("action")
		action_url = self.request.get("action_url")
		place_holder_encoding = self.request.get("place_holder_encoding")
		input_prompt = self.request.get("input_prompt")
		input_prompt_description = self.request.get("input_prompt_description")
		
		item = OneKeyItem()
		item.service_name = service_name
		item.title = title
		item.action = action
		item.action_url = action_url
		item.place_holder_encoding = place_holder_encoding
		item.input_prompt = input_prompt
		item.input_prompt_description = input_prompt_description
		item.put()
		self.redirect("/onekey/items/add")
		pass
		

class MainHandler(webapp.RequestHandler):
	def get(self):
		item_list = ItemList()
		html_list = item_list.html_list().encode('utf-8')
		template_values = {
			'html_list': html_list,
		}
		path = os.path.join(os.path.dirname(__file__), '..', 'html', 'onekey.html')
		self.response.out.write(html.sharedHTML.header(u"一點通編輯程式"))
		self.response.out.write(template.render(path, template_values))
		self.response.out.write(html.sharedHTML.toolbar())
		self.response.out.write(html.sharedHTML.footer())

def main():
	application = webapp.WSGIApplication([
			('/onekey', MainHandler),
			('/onekey/items', OneKeyItemListHandler),
			('/onekey/items/add', AddOneKeyItemHandler),
		], debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()
