from app import db

class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    event_type = db.Column(db.String(50))
    location = db.Column(db.String(50))
    date = db.Column(db.String(20))
    description = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    user = db.relationship("User", back_populates="events")


