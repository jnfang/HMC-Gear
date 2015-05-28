from BaseHandler import Handler
from google.appengine.ext import db
from Db import Person, Gear
from datetime import datetime, timedelta
import constants
from google.appengine.api import mail
class Email(Handler):
	def get(self):
		overdueGear = [g for g in Gear.all() if g.returnDate and datetime.now() > g.returnDate]
		for g in overdueGear:
			sender_address = 'overduegear@hmc-gear.appspotmail.com'
			destination_address = [g.holder.email, 'rorybrown@college.harvard.edu', 'danielbridgwater@college.harvard.edu', 'njoseph@college.harvard.edu']
			subject = 'Overdue Gear'
			body = "You have a piece of gear that is overdue, " + g.number + ". Please return it at the next meeting. If you can't make it please email one of the gear czars to find a time."""
			mail.send_mail(sender_address, destination_address, subject, body)
