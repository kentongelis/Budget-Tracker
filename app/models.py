from app.extensions import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

class FormEnum(enum.Enum):
    """Helper class to make it easier to use enums with forms."""
    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)
    
class Plan(FormEnum):
    lenient = 'Lenient (30/60/10)'
    normal = 'Normal (50/30/20)'
    extreme = 'Extreme (40/20/40)'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable = False, unique=True)
    password = db.Column(db.String(200), nullable = False)
    name = db.Column(db.String(200), nullable=False)
    plan = db.Coulmn(db.Emum(Plan))
    savings = db.Column(db.Float(precision=2), nullable=False)
    paycheck = db.Column(db.Float(precision=2), nullable=True)
    posts = db.relationship('Post', back_populates='user', lazy=True)
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80, nullable = False))
    posts = db.relationship('Posts', back_populates='category', lazy=True)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(500), nullable=False)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='posts')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', back_populates='posts')
    