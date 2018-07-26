from .db import _db as db
from sqlalchemy.orm import validates
# from sqlalchemy.ext.declarative import declarative_base
from flask_security import UserMixin, RoleMixin


mentor_mentee = db.Table(
    'mentor_mentee',
    db.metadata,
    db.Column('mentor_id', db.Integer, db.ForeignKey('mentors.id')),
    db.Column('mentee_id', db.Integer, db.ForeignKey('mentees.id')),
)


class Mentors(db.Model):
    __tablename__ = 'mentors'

    id = db.Column(db.Integer, primary_key=True)
    mentor_name = db.Column(db.String(256), unique=True, nullable=False)
    mentor_email = db.Column(db.String(256), unique=True, nullable=False)

    mentee = db.relationship("Mentees", secondary=mentor_mentee)

    def __repr__(self):
        return '<Mentor {}>'.format(self.mentor_name)

    # vadidates from sqlalchemy - https://gist.github.com/matrixise/6417293
    # http://docs.sqlalchemy.org/en/latest/orm/mapped_attributes.html#simple-validators
    # only validating for @ symbol is sufficient
    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address


class Mentees(db.Model):
    __tablename__ = 'mentees'

    id = db.Column(db.Integer, primary_key=True)
    mentee_name = db.Column(db.String(64), unique=True, nullable=False)
    mentee_email = db.Column(db.String(256), nullable=True)

    mentor = db.relationship("Mentors", secondary=mentor_mentee)

    def __repr__(self):
        return '<Mentee {}>'.format(self.mentee_name)


class Tasks(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)

    # foreign key to mentee table plus a representational name
    # (https://stackoverflow.com/questions/16160507/flask-admin-not-showing-foreignkey-columns)
    mentee_id = db.Column(db.Integer, db.ForeignKey('mentees.id'), nullable=False)
    mentee = db.relationship('Mentees', backref=db.backref('Tasks', lazy='dynamic'))

    task = db.Column(db.String(1024), nullable=False)
    at_created = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    def __repr__(self):
        return '<Task {}>'.format(self.task)


# Flask-Security

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
