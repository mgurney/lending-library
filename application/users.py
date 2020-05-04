"""
User handling :
                    signup
                    login
                    password_reset
                    reset_with_token
                    load_user
                    unauthorized
                    logout
"""

from datetime import datetime

from flask import current_app as app
from flask import render_template, redirect
from flask import request, flash, url_for
from flask_login import current_user
from flask_login import login_user, login_required, logout_user
from itsdangerous import URLSafeTimedSerializer

from application import login_manager
from application.forms import LoginForm, SignupForm, ResetForm, PasswordForm
from application.models import db, User
from application.send_email import send_email


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

@app.route('/password_reset', methods=['GET', 'POST'])
def password_reset():

    form = ResetForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first_or_404()
        except:
            flash('Invalid email address!', 'error')
            return render_template('password_reset_form.html', form=form)


        send_email(user.email, "Lending Library - Password Reset")
        flash('Please check your email for a password reset link.', 'success')

        return redirect(url_for('login'))

    return render_template('password_reset_form.html', form=form)

@app.route('/reset_with_token/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt='93kjng02', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('login'))

    form = PasswordForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=email).first_or_404()
        except:
            flash('Invalid email address!', 'error')
            return redirect(url_for('login'))

        password = form.password.data
        user.set_password(password)
        db.session.commit()
        db.session.close()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password_with_token.html', form=form, token=token)


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

@app.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    db.session.close()
    logout_user()
    return redirect(url_for('login'))