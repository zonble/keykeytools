#!/usr/bin/env python
# encoding: utf-8
#

import os
from google.appengine.api import users
from google.appengine.ext.webapp import template

class HTML():
	"""docstring for HTML"""
	def header(self, title=""):
		if len(title):
			title = u"輸入法工具箱 | " + title
		else:
			title = u"輸入法工具箱"
		template_values = {'title': title}
		path = os.path.join(os.path.dirname(__file__), '..', 'html', 'header.html')
		return template.render(path, template_values)
	def footer(self, url="/"):

		if users.get_current_user():
			login_link = '<a href="' + users.create_logout_url(url) + '">Logout</a>'
		else:
			login_link = '<a href="' + users.create_login_url(url) + '">&nbsp;</a>'
		template_values = {"login_link": login_link}
		path = os.path.join(os.path.dirname(__file__), '..', 'html', 'footer.html')
		return template.render(path, template_values)
	def toolbar(self):
		template_values = {}
		path = os.path.join(os.path.dirname(__file__), '..', 'html', 'toolbar.html')
		return template.render(path, template_values)

		pass
		
sharedHTML = HTML()