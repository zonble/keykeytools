#!/usr/bin/env python
# encoding: utf-8
#
import os
import sys

import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

import codecs

path = os.path.dirname(__file__)
sys.path.append(path)

import html

class MainHandler(webapp.RequestHandler):
	def get(self):
		error = self.request.get("error")
		error_msg = ""
		if error:
			error_msg = u"您所上傳的檔案不正確！"
		template_values = {
			'error_msg' : error_msg,
		}
		path = os.path.join(os.path.dirname(__file__), '..', 'html', 'mskkconverter.html')
		self.response.out.write(html.sharedHTML.header(u"好打注音輸入法匯入微軟新注音自訂詞庫工具"))
		self.response.out.write(template.render(path, template_values))
		self.response.out.write(html.sharedHTML.toolbar())
		self.response.out.write(html.sharedHTML.footer(self.request.url))

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
		file = self.request.get("uploadedfile", default_value='')
		try:
			file = unicode(file, encoding='utf-16', errors='replace')
		except:
			pass
		if len(file) == 0:
			self.redirect("/mskkconverter?error=1")
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
