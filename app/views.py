from flask import render_template, redirect, url_for, flash, request, g
from flask_login import login_required, login_user, logout_user, current_user

from app import app, db, lm
from .forms import LoginForm, RegistrationForm
from .models import User

@app.route("/", methods = ['GET'])
@app.route("/index", methods = ['GET'])
@login_required
def index():
    return render_template('index.html',
                           title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('Username "%s" not found.' % (username))
            return redirect(url_for('login'))

        if not user.verify_password(form.password.data):
            flash('Incorrect Password.')
            return redirect(url_for('login'))

        login_user(user, remember = form.remember_me.data)

        flash('Logged in successfuly for {}.'.format(username))
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
        username = form.username.data
        if User.query.filter_by(username=username).first():
            flash('Username "%s" already exists.' % (username))
            return redirect(url_for('register'))

        user = User(
            username = username,
            email = form.email.data,
        )
        user.hash_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html',
                           title='Register',
                           form=form)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
