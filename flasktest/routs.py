import os.path
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flasktest.forms import RegistrationForm, LoginForm, ResumePasswordForm, UpdateUserAccount

from flasktest import app, db, bcrypt
from flasktest.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Simone Giuri',
        'title': 'First Post',
        'content': 'First Post Content',
        'date_posted': 'October 12, 2022',
    },
    {
        'author': 'Pinco Pallino',
        'title': 'Second Post',
        'content': 'Second Post Content',
        'date_posted': 'October 15, 2022',
    }
    ]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember)

            flash(f'Welcome back {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Wrong Username or Password!', 'warning')

    return render_template('login.html', title='Login', form=form)

@app.route("/register",methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome to our community {form.username.data}!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route("/reset-password",methods = ["GET", "POST"])
def reset_pwd():
    form = ResumePasswordForm()
    if form.validate_on_submit():
        flash(f'Email sent {form.email.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('reset-password.html', title='Reset Password', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    old_image_fn = current_user.image_file

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    f_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(f_path)
    if old_image_fn != 'default.jpg':
        old_f_path = os.path.join(app.root_path, 'static/profile_pic', old_image_fn)
        os.remove(old_f_path)
    return picture_fn

@app.route("/account", methods = ["GET", "POST"])
@login_required
def account():
    form = UpdateUserAccount()
    if form.validate_on_submit():
        if form.picture.data:
            file_pic = save_picture(form.picture.data)
            current_user.image_file = file_pic
        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash(f'Profile updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email



    image_file = url_for("static", filename= "profile_pic/" + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)