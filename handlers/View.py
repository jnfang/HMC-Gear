from google.appengine.ext import db
from BaseHandler import Handler
from Db import *
class View(Handler):
	def get(self, pagename):
		page = db.GqlQuery('SELECT * FROM Page WHERE name=:pagename', pagename=pagename).get()
		if page:
			self.render("wikiPage.html", text=page.text)
		else:
			self.redirect('/_edit'+pagename)
