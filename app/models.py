from . import db, mash
from werkzeug.security import check_password_hash, generate_password_hash
import datetime


# User class
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False, index=True)
    email = db.Column(db.String(30), unique=True, nullable=False, index=True)
    password = db.Column(db.String())
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    # Add record
    def insert_record(self):
        db.session.add(self)
        db.session.commit()
        return self

    # fetch user by username
    @classmethod
    def fetch_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    # fetch user by id
    @classmethod
    def fetch_user_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    # fetch user by email
    @classmethod
    def fetch_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    # Fetch all users
    @classmethod
    def fetch_all_users(cls):
        return cls.query.all()

    # update by name
    @classmethod
    def update_user_by_name(cls, name, username=None, email=None):
        record = cls.query.filter_by(username=name).first()
        if record:
            if username:
                record.username = username
            if email:
                record.email = email
            db.session.commit()
        return cls.query.filter_by(id=id).first()

    # delete by name
    @classmethod
    def delete_user_by_username(cls, username):
        record = cls.query.filter_by(username=username)
        if record.first():
            record.delete()
            db.session.commit()
            return True
        return False

    # check if username exists
    @classmethod
    def check_username(cls, username):
        # Try and fetch the user
        user = cls.query.filter_by(username=username).first()

        if user:
            return True
        return False

    # check if email exists
    @classmethod
    def check_email(cls, email):
        # Try and fetch the user
        user = cls.query.filter_by(email=email).first()

        if user:
            return True
        return False

    # hash password
    @classmethod
    def set_password_hash(cls, password):
        return generate_password_hash(password)

    # check password
    @classmethod
    def validate_user(cls, username, password):
        user = cls.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            return True
        return False


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False, unique=False)
    description = db.Column(db.String(400), nullable=False, unique=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    date_started = db.Column(db.DateTime)
    date_completed = db.Column(db.DateTime)
    date_cancelled = db.Column(db.DateTime)
    status = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Crud Operations
    # Create new record
    def insert_record(self):
        db.session.add(self)
        db.session.commit()
        return self

    # update record by id
    @classmethod
    def update_by_id(cls, id, title=None, description=None, status=None):
        # status filed codes
        # 0=todo, 1=ongoing, 2=completed, 3=cancelled

        # fetch the record
        record = cls.query.filter_by(id=id).first()
        current_status = record.status

        if record:
            if title:
                record.title = title
            if description:
                record.description = description
            if status == current_status:
                pass
            else:
                if status == 0:
                    record.status = status
                    record.date_cancelled = record.date_completed = record.date_started = None
                elif status == 1:
                    record.date_started = datetime.now()
                    record.status = status
                    record.date_cancelled = record.date_completed = None
                elif status == 2:
                    record.date_completed = datetime.now()
                    record.status = status
                    record.date_cancelled = None
                elif status == 3:
                    record.date_cancelled = datetime.now()
                    record.status = status
                    record.date_completed = None
                else:
                    pass

            db.session.commit()
        return cls.query.filter_by(id=id).first()

    # delete by id
    @classmethod
    def delete_by_id(cls, id):
        record = cls.query.filter_by(id=id)
        if record.first():
            record.delete()
            db.session.commit()
            return True
        return False

    # fetch all tasks
    @classmethod
    def fetch_tasks(cls):
        tasks = cls.query.all()
        return tasks


# Task schema for serializing
class TaskSchema(mash.Schema):
    class Meta:
        model = Task


# Task schema for serializing
class UserSchema(mash.ModelSchema):
    class Meta:
        model = User
