from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    username = db.Column(db.String(80), primary_key=True)  
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")

    plants = db.relationship('Plant', backref='owner', lazy=True)

    def get_id(self):
        return self.username  


class PlantCategory(db.Model):
    latin_name = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    watering_interval = db.Column(db.Integer, nullable=False)
    info = db.Column(db.Text)  

    plants = db.relationship('Plant', backref='category', lazy=True)



class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String(100), nullable=False)
    last_watering = db.Column(db.Date)
    next_watering = db.Column(db.Date)
    photo_path = db.Column(db.String(200))
    description = db.Column(db.Text)  

    username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    latin_name = db.Column(db.String(100), db.ForeignKey('plant_category.latin_name'), nullable=False)






    
