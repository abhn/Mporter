from . import db

mentor_mentee = db.Table('mentor_mentee', db.metadata,
    db.Column('mentor_id', db.Integer, db.ForeignKey('mentor.id')),
    db.Column('mentee_id', db.Integer, db.ForeignKey('mentee.id')),
)


class Mentor(db.Model):
    __tablename__ = 'mentor'

    id = db.Column(db.Integer, primary_key=True)
    mentor_name = db.Column(db.String(64), unique=True, nullable=False)

    mentee = db.relationship("Mentee", secondary=mentor_mentee)


class Mentee(db.Model):
    __tablename__ = 'mentee'

    id = db.Column(db.Integer, primary_key=True)
    mentee_name = db.Column(db.String(64), unique=True, nullable=False)

    mentor = db.relationship("Mentor", secondary=mentor_mentee)


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('mentee.id'), nullable=False)
    task = db.Column(db.String(1024), unique=True, nullable=False)
    at_created = db.Column(db.Integer, nullable=False)

    # def __init__(self, user_id, task, at_created=math.floor(time.time())):
    #     self.user_id = user_id
    #     self.task = task
    #     self.at_created = at_created
    #     super(Task, self).__init__()
    #
    # def __repr__(self):
    #     return '<Task %r>' % self.task