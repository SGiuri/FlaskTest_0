from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = 'f79649168b66944ccffaf0f15a84717b'

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
def hello_world():
    return render_template('home.html', posts=posts)

@app.route("/about")
def hello_about():
    return render_template('about.html', title='About')


if __name__=="__main__":
    app.run(debug=True)