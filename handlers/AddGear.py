from BaseHandler import Handler
from google.appengine.ext import db
from Db import Gear
import constants
class AddGear(Handler):
	def write_form(self, error = ""):
		self.render("addGear.html", error=error)
	#Renders the form with no error messages
	def get(self):
		self.write_form()
	#Deals with submitting the form
	def post(self):
		#Get information from the post request
		gearNum = self.request.get("number")
		if not (gearNum[1:].isdigit() and gearNum[0].isalpha):
			self.write_form(error = "Please put in a letter and number")
			return
		description = self.request.get("description")
		password = self.request.get('password')
		# if password != constants.PASSWORD:
		# 	self.write_form(error = "Wrong password!")
		# 	return
		itemQuery = db.GqlQuery("SELECT * FROM Gear WHERE number = :1", gearNum)
		if itemQuery.count() == 0:
			item = Gear(number=gearNum, description=description)
			item.put()
			self.redirect("/addGear")
		else:
			self.write_form(error = "The item number is taken")
