#!/usr/bin/env python
# encoding: utf-8
#
import os

import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

import codecs

class MainHandler(webapp.RequestHandler):
	def get(self):
		template_values = {
			# 'url': url,
			# 'url_linktext': url_linktext,
		}
		path = os.path.join(os.path.dirname(__file__), '..', 'html', 'mskkconverter.html')
		self.response.out.write(template.render(path, template_values))

	def converter(self, text):
		new_text = "MJSR version 1.0.0\n"
		for line in text:
			parts = line.partition(u'  ')
			if (len(parts)):
				phrase = parts[0]
				phonetic = parts[2]
				replaced_string = phonetic.strip()
				replaced_string = replaced_string.replace(u'ˉ', u',')
				replaced_string = replaced_string.replace(u'ˊ', u'ˊ,')
				replaced_string = replaced_string.replace(u'ˇ', u'ˇ,')
				replaced_string = replaced_string.replace(u'ˋ', u'ˋ,')
				replaced_string = replaced_string.replace(u' ', u'')
				replaced_string = replaced_string.replace(u'　', u'')
				replaced_string = replaced_string.replace(u'  ', u'')
				if replaced_string.endswith(','):
					replaced_string = replaced_string[:len(replaced_string) - 1]
				line = phrase + u"\t" + replaced_string + u"\t-1.0\t0.0\n"
				new_text = new_text + line
		return new_text

	def post(self):
		file = self.request.get("uploadedfile")
		file = unicode(file, encoding='utf-16', errors='replace')
		if len(file) == False:
			self.redirect("/mskkconverter")
		self.response.headers['Content-Type'] = 'text/plain; charset=utf-8'
		self.response.headers['Content-Disposition'] = 'attachment; filename=phrase.txt'
		
		text = file.split(u'\n')
		new_text = self.converter(text)
		self.response.out.write(new_text)
		pass

def main():
	application = webapp.WSGIApplication([('/mskkconverter', MainHandler)], debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()
