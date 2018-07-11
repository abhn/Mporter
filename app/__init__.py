from flask import Flask, render_template, request
import os
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

app = Flask(__name__)

SECRET_KEY = os.environ['MPORTER_SECRET']

app.secret_key = SECRET_KEY

admin = Admin(app, name='Mporter', template_mode='bootstrap3')


# the values of those depend on your setup
DB_URL = os.environ['SQLALCHEMY_DATABASE_URI']

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

# initialize the db object
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# now import models to prevent cylic import errors,
# there has to be a better way to do this, sigh.
from .models import Task, Mentee, Mentor

# add the admin panel views
admin.add_view(ModelView(Task, db.session))
admin.add_view(ModelView(Mentor, db.session))
admin.add_view(ModelView(Mentee, db.session))

# create all the models
db.create_all()
db.session.commit()


# dummy route, TODO add a landing page
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)