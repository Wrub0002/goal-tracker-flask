from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# User model for authentication and user-specific data
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    # One user can have many goals
    goals = db.relationship('Goal', backref='user', cascade='all, delete')

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        # Hash and store password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Verify password against stored hash
        return check_password_hash(self.password_hash, password)

# Goal model represents a long-term objective
class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    priority = db.Column(db.String(10))
    created_at = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # One goal can have many tasks
    tasks = db.relationship('Task', backref='goal', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Goal {self.title} - {self.due_date} - {self.priority}>"

# Task model represents a single actionable step within a goal
class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'), nullable=False)

    def __repr__(self):
        return f"<Task {self.title} - {self.due_date} - {self.is_completed}>"