from google.appengine.ext import db
from BaseHandler import Handler
from Db import *
import cgi
class View(Handler):
	def get(self):
		itemQuery = db.GqlQuery("SELECT * FROM Gear")
		gear_items = itemQuery.fetch(limit=None)
		self.render("view.html", gear_items=gear_items)
