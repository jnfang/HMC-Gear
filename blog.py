import os
import webapp2
import jinja2
import validation
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

###########################################################################
#######                       Database Classes:                     #######
###########################################################################

#Table for blog entires
class Entry(db.Model):
	title = db.StringProperty(required = True)
	blog = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
#Table for users
class User(db.Model):
	username = db.StringProperty(required=True)
	pass_hash = db.StringProperty(required=True)
	email = db.StringProperty(required=False)
	created = db.DateTimeProperty(auto_now_add=True)

###########################################################################
#######                       Handler Classes:                      #######
###########################################################################

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Login(Handler):
	def write_form(self, username="", error=""):
		self.render("login.html",  username=username, error=error)

	#Renders the form with no error messages
	def get(self):
		self.write_form()

	#Deals with submitting the form
	def post(self):
		#Get information from the post request
		username = self.request.get('username')
		password = self.request.get('password')
		userQuery = db.GqlQuery("SELECT * FROM User WHERE username='%s'" % str(username)) #Does Query
		if userQuery.count()>0: #if the user exists
			user = userQuery.get()
			if validation.valid_pw(user.username, password, user.pass_hash): #checks if the username and password are valid
				user_id = user.key().id()
				#Makes and adds the cookie
				self.response.headers['Content-Type'] = 'text/plain'
				cookie_val = validation.make_secure_val(str(user_id))
				self.response.headers.add_header('Set-Cookie',str('user=%s; Path=/' % cookie_val))
				self.redirect("welcome")
			else:
				self.write_form(error="Invalid Password", username=username)
		else:
			self.write_form(error="User doesn't exist", username=username)

class Logout(Handler):
	def get(self):
		self.response.headers.add_header('Set-Cookie', str('user=; Path=/'))
		self.redirect("signup")
class NewEntry(Handler):
	def render_front(self, title="", blog="", error=""):
		self.render("newEntry.html", title=title, blog=blog, error=error)
	def get(self):
		self.render_front()
	def post(self):
		title = self.request.get("subject")
		blog = self.request.get("content")
		if title and blog:
			entry = Entry(title = title, blog = blog)
			user_id = entry.put().id()

			self.redirect("/%d" %user_id)
		else:
			error = "we need both a title and a blog post!"
			self.render_front(title, blog, error)
class Permalink(Handler):
	def get(self, blog_id):
		post = Entry.get_by_id(int(blog_id))
		self.render("permalink.html", title=post.title, blog=post.blog)
class Signup(Handler):
	def write_form(self, userError = "", passError = "", verifyError = "", emailError = "", username = "", email=""):
		self.render("signup.html", userError= userError, passError= passError, verifyError= verifyError, emailError= emailError, username= username, email= email)
	def get(self):
		self.write_form()
	def post(self):
		user_username = self.request.get('username')
		user_password = self.request.get('password')
		user_verify = self.request.get('verify')
		user_email = self.request.get('email')	

		username = validation.username(user_username)
		password = validation.password(user_password)
		verify = validation.verify(user_verify, user_password)
		email = validation.email(user_email)


		userError=""
		passError=""
		verifyError=""
		emailError=""
		if not username:
			userError = "That's not a valid username."
		if not password:
			passError = "That wasn't a valid password."
		if not verify:
			verifyError = "Your passwords didn't match."
		if not email:
			emailError = "That's not a valid email."

		if username and password and verify and email:
			pass_hash = validation.make_pw_hash(username, password)
			if email == "No Email":
				user = User(username = username, pass_hash = pass_hash)
			else:
				user= User(username = username, pass_hash = pass_hash, email = email)
			u = User.all().filter('username =', username).get()
			if u:
				self.write_form("That username is already taken.", passError, verifyError, emailError, username, email)
				return
			user_id = user.put().id()
			self.response.headers['Content-Type'] = 'text/plain'
			cookie_val = validation.make_secure_val(str(user_id))
			self.response.headers.add_header('Set-Cookie',str('user=%s; Path=/' % cookie_val))
			self.redirect("/welcome")
		else:
			self.write_form(userError, passError, verifyError, emailError, username, email)
class Welcome(Handler):
	def get(self):
		cookie = validation.check_secure_val(self.request.cookies.get('user'))
		if cookie:
			user_id = cookie.split("|")[0]
			username = User.get_by_id(int(user_id)).username
			self.write("Welcome, %s" % username)
		else:
			self.redirect("/signup")
class MainPage(Handler):
	def render_front(self, title="", blog="", error=""):
		blogs = db.GqlQuery("SELECT * FROM Entry ORDER BY created DESC")
		self.render("front.html", title=title, blog=blog, error=error, blogs = blogs)
	def get(self):
		self.render_front()
application = webapp2.WSGIApplication([ ('/', MainPage),
										('/newpost', NewEntry),
										('/(\d+)', Permalink),
										('/signup', Signup),
										('/welcome', Welcome),
										('/login', Login),
										('/logout', Logout)
										], debug = True)

