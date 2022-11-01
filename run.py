from flasktest import app

"""Per inizializzare il database
from flasktest import app
from flasktest import db
from flasktest.models import User, Post
with app.app_context():
    db.create_all()
"""


if __name__=="__main__":
    app.run(debug=True)