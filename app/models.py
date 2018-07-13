from . import db
from sqlalchemy.orm import validates

mentor_mentee = db.Table('mentor_mentee', db.metadata,
    db.Column('mentor_id', db.Integer, db.ForeignKey('mentor.id')),
    db.Column('mentee_id', db.Integer, db.ForeignKey('mentee.id')),
)


class Mentor(db.Model):
    __tablename__ = 'mentor'

    id = db.Column(db.Integer, primary_key=True)
    mentor_name = db.Column(db.String(256), unique=True, nullable=False)
    mentor_email = db.Column(db.String(256), unique=True, nullable=False)

    mentee = db.relationship("Mentee", secondary=mentor_mentee)

    def __repr__(self):
        return '<Mentor %r>' % self.mentor_name

    # vadidates from sqlalchemy - https://gist.github.com/matrixise/6417293
    # http://docs.sqlalchemy.org/en/latest/orm/mapped_attributes.html#simple-validators
    # only validating for @ symbol is sufficient
    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address


class Mentee(db.Model):
    __tablename__ = 'mentee'

    id = db.Column(db.Integer, primary_key=True)
    mentee_name = db.Column(db.String(64), unique=True, nullable=False)

    mentor = db.relationship("Mentor", secondary=mentor_mentee)

    def __repr__(self):
        return '<Mentee %r>' % self.mentee_name


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)

    # foreign key to mentee table plus a representational name
    # (https://stackoverflow.com/questions/16160507/flask-admin-not-showing-foreignkey-columns)
    mentee_id = db.Column(db.Integer, db.ForeignKey('mentee.id'), nullable=False)
    mentee = db.relationship('Mentee', backref=db.backref('Tasks', lazy='dynamic'))

    task = db.Column(db.String(1024), nullable=False)
    at_created = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.task