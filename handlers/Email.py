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
			destination_address = [g.holder.email, 'njoseph@college.harvard.edu', 'wbloxham@college.harvard.edu', 'rradovanovic@college.harvard.edu']
			subject = 'Overdue Gear'
			body = "You have a piece of gear that is overdue, " + g.number + ". Please return it as soon as possible."""
			mail.send_mail(sender_address, destination_address, subject, body)
