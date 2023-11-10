from app import db

class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    event_type = db.Column(db.String(80))
    location = db.Column(db.String(60))
    date = db.Column(db.String(50))
    description = db.Column(db.String(550))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"))
    user = db.relationship("User", back_populates="events")
    file_data = db.Column(db.LargeBinary)