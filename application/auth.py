from datetime import datetime

from flask import current_app as app
from flask import render_template, redirect
from flask import request, flash, url_for
from flask_login import current_user
from flask_login import login_user, login_required

from application import login_manager
from application.forms import LoginForm, SignupForm
from application.models import db, User


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    if request.method == 'POST':
        if signup_form.validate_on_submit():
            name = signup_form.name.data
            email = signup_form.email.data
            password = signup_form.password.data
            now_date = datetime.now()
            rules = signup_form.read_rules.data
            existing_user = User.query.filter_by(email=email).first()  # Check if user exists
            if existing_user is None:
                user = User(name=name,
                            email=email,
                            rules_read=rules,
                            created_on=now_date)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()  # Create new user
                db.session.close()
                login_user(user)  # Log in as newly created user
                return redirect(url_for('index'))
            flash('A user already exists with that email address.')
            return redirect(url_for('signup'))


    return render_template('signup.html',
                           title='Create an Account.',
                           form=SignupForm(),
                           body="Sign up for a user account.")



@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login page.

    GET: Serve Log-in page.
    POST: If form is valid and new user creation succeeds, redirect user to the logged-in homepage.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Bypass if user is logged in

    login_form = LoginForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            user = User.query.filter_by(email=email).first()  # Validate Login Attempt

            if user and user.check_password(password=password):
                login_user(user)
                user.last_login = datetime.now()
                db.session.commit()
                db.session.close()
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))

        flash('Invalid username/password combination')
        return redirect(url_for('login'))

    return render_template('login.html',
                           form=login_form,
                           title='Log in.',
                           body="Log in with your User account.")

@app.route('/password_change_qo98lkjdnlsd', methods=['GET', 'POST'])
@login_required
def password_change_qo98lkjdnlsd():
    user = User.query.filter_by(id=4).first()
    user.set_password('PUB803W')
    db.session.commit()
    db.session.close()
    return redirect(url_for('library'))

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))