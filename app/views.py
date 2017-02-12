from flask import render_template, redirect, url_for, flash, request, g
from flask_login import login_required, login_user, logout_user, current_user

from app import app, lm
from .forms import LoginForm, RegistrationForm
from .models import User

# TODO(steve): Add logout and proper index page
# TODO(steve): convert to using database and SQLAlchemy

@app.route("/", methods = ['GET'])
@app.route("/index", methods = ['GET'])
@login_required
def index():
    return render_template('index.html',
                           title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if User.verify_password(form.username.data, form.password.data):
            user = User(form.username.data, form.password.data)
            login_user(user)

            flash('Logged in successfuly for {}'.format(form.username.data))
            return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html',
                           title='Sign In',
                           form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = (form.username.data, form.password.data)
        User.user_database[form.username.data] = user
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html',
                           title='Register',
                           form=form)

@lm.user_loader
def load_user(id):
    return User.get(id)

@app.before_request
def before_request():
    g.user = current_user
