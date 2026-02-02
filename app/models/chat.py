
# app/models/chat.py
from datetime import datetime
from app import db

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('Message', backref='chat', lazy='dynamic')
    
    def get_last_message(self):
        from app.models.message import Message
        return self.messages.order_by(Message.timestamp.desc()).first()
    
    def get_other_user(self, user_id):
        from app.models.user import User
        if int(user_id) == self.user1_id:
            return User.query.get(self.user2_id)
        return User.query.get(self.user1_id)
    
    def __repr__(self):
        return f'<Chat {self.id} between {self.user1_id} and {self.user2_id}>'
