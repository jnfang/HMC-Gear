from BaseHandler import Handler
from google.appengine.ext import db
from Db import Person
from datetime import datetime, timedelta
import re
import constants
class Input(Handler):
	def write_form(self, error = ""):
		self.render("input.html", error=error)
	#Renders the form with no error messages
	def get(self):
		self.write_form()
	#Deals with submitting the form
	def post(self):
		#Get information from the post request
		gearNums = self.request.get("number").upper().split(" ")
		EMAIL = re.compile(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$")
		gearNum = self.request.get("number").upper()
		email = self.request.get("holder").lower()
		if not EMAIL.match(email):
			self.write_form(error = 'This is not a valid email')
			return
		password = self.request.get('password')
		if password != constants.PASSWORD:
			self.write_form(error = 'Wrong password!')
			return
		numDays = int(self.request.get('days'))
		personQuery = db.GqlQuery("SELECT * FROM Person WHERE email = :1", email)
		person = Person(email = email)
		if personQuery.count() > 0:
			person = personQuery.get()

		for gearNum in gearNums:
			if not (gearNum[1:].isdigit() and gearNum[0].isalpha()):
				self.write_form(error = "Please enter a valid gear letter and number (e.g. G35)")
				return
			itemQuery = db.GqlQuery("SELECT * FROM Gear WHERE number = :1", gearNum)
			if itemQuery.count() > 0:
				person.put()
				item = itemQuery.get()
				item.holder = person
				item.holderName = person.email
				item.returnDate = datetime.now() + timedelta(days = numDays)
				item.put()
				self.redirect("/input")
			else:
				self.write_form(error = "The item number doesn't exist")
