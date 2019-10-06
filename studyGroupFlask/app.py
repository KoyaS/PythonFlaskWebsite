# app file
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretString'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/koya/Desktop/Projects/PythonFlaskWebsite/studyGroupFlask/database.db'
Bootstrap(app)
db = SQLAlchemy(app)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), unique=True)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(80))

class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])
	remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])
	
@app.route('/')
def index():
	return(render_template('index.html'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
	 	existing_user = User.query.filter_by(username=form.username.data).first()
	 	
	 	if existing_user: # Checking that user exists
	 		
	 		if existing_user.password == form.password.data:
	 			return('<h1>Welcome {}<h1>'.format(form.username.data))
	 	
	 	return('<h1> incorrect username or password</h1>')
		# return('<h1>' + form.username.data + ' ' + form.password.data + '</h1>')
	
	return(render_template('login.html', form=form))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = RegisterForm()

	if form.validate_on_submit():
		new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
		db.session.add(new_user)
		db.session.commit()
		return("<h1>new user has been created</h1>")
		# return('<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>')
	
	return(render_template('signup.html', form=form))

if __name__ == '__main__':
	app.run(debug=True)

print ("REACHED END")
