from BaseHandler import Handler
from google.appengine.ext import db
import constants
class Return(Handler):
	def write_form(self, error = ""):
		self.render("return.html", error=error)
	#Renders the form with no error messages
	def get(self):
		self.write_form()
	#Deals with submitting the form
	def post(self):
		#Get information from the post request
		gearNums = self.request.get("number").upper().split(" ")
		password = self.request.get('password')
		if password != constants.PASSWORD:
			self.write_form(error = "Wrong password!")
			return
		for gearNum in gearNums:
			itemQuery = db.GqlQuery("SELECT * FROM Gear WHERE number = :1", gearNum)
			if itemQuery.count() > 0:
				item = itemQuery.get()
				item.holder = None
				item.holderName = None
				item.returnDate = None
				item.put()
				self.redirect('return')
			else:
				self.write_form(error = "The item number doesn't exist")

