from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, ResumePasswordForm


app = Flask(__name__)

app.config['SECRET_KEY'] = 'f79649168b66944ccffaf0f15a84717b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) # lazy: sqlalchemy carica i dati solo quando
                                                                    # necessario in un unico momento

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # user e' il nome di default della tabella creata
                                                                # dalla classe User

    def __repr__(self):
        return f"post('{self.title}', '{self.date_posted}')"


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
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "dummy_user@email.it" and form.password.data == "dummy":

            flash(f'Welcome back {form.email.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Wrong Username and Password!', 'warning')

    return render_template('login.html', title='Login', form=form)

@app.route("/register",methods = ["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Welcome to our community {form.username.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route("/reset-password",methods = ["GET", "POST"])
def reset_pwd():
    form = ResumePasswordForm()
    if form.validate_on_submit():
        flash(f'Email sent {form.email.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('reset-password.html', title='Reset Password', form=form)



if __name__=="__main__":
    app.run(debug=True)