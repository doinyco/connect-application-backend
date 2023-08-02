from app import db

class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_type = db.Column(db.String(30))
    location = db.Column(db.String(50))
    date = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    user = db.relationship("User", back_populates="events")
