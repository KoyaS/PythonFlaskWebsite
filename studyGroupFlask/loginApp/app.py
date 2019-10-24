# app file
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['TESTING'] = False
app.config['SECRET_KEY'] = 'secretString'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/koya/Desktop/Projects/PythonFlaskWebsite/studyGroupFlask/loginApp/database.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), unique=True)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
	return(User.query.get(int(user_id)))

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
	logout_user()
	return(render_template('index.html'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
	 	existing_user = User.query.filter_by(username=form.username.data).first()
	 	
	 	if existing_user: # Checking that user exists
	 		
	 		if check_password_hash(existing_user.password, form.password.data):
	 			login_user(existing_user, remember=form.remember.data)
	 			return(redirect(url_for('dashboard')))
	 	
	 	return('<h1> incorrect username or password</h1>')
		# return('<h1>' + form.username.data + ' ' + form.password.data + '</h1>')
	
	return(render_template('login.html', form=form))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = RegisterForm()

	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data, method='sha256') # Hashes password before being passed to database
		new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()
		return("<h1>new user has been created</h1>")
		# return('<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>')
	
	return(render_template('signup.html', form=form))

@app.route('/dashboard')
@login_required
def dashboard():
	return(render_template('dashboard.html', name=current_user.username))

if __name__ == '__main__':
	app.run(debug=True)




