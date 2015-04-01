import os
import sys
import webapp2
import jinja2
import json
import time
import logging
from google.appengine.ext import db
from google.appengine.api import memcache
sys.path.append('handlers')
sys.path.append('db')
from Input import Input
from View import View
from Return import Return
from AddGear import AddGear
from Email import Email

application = webapp2.WSGIApplication([('/input', Input),
								('/return', Return),
                                ('/view', View),
								('/addGear', AddGear),
                                ('/', Input),
								('/email', Email)
                                ],
                                debug=True)
