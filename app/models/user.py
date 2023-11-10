from app import db
from flask_login import UserMixin 

class User(db.Model, UserMixin):
    __tablename__ = 'users' 
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(30))
    password = db.Column(db.String(300), nullable=False)
    events = db.relationship("Event", back_populates="user")

    def get_id(self):
        return str(self.user_id)