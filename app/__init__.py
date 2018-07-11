from flask import Flask, render_template, request
import os
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

admin = Admin(app, name='Mporter', template_mode='bootstrap3')

# the values of those depend on your setup
DB_URL = os.environ['SQLALCHEMY_DATABASE_URI']

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)