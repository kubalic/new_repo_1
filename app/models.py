from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    plants = db.relationship('Plant', backref='owner', lazy=True)

class PlantCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    latin_name = db.Column(db.String(100))
    watering_interval = db.Column(db.Integer)  

    plants = db.relationship('Plant', backref='category', lazy=True)
    
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100))
    last_watering = db.Column(db.Date)
    next_watering = db.Column(db.Date)
    photo_path = db.Column(db.String(200))  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('plant_category.id'), nullable=False)





    
