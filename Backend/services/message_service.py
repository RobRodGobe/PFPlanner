from Backend.models import Message

class MessageService:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return Message.query.order_by(Message.created_at.desc()).all()

    def add(self, text):
        msg = Message(text=text)
        self.db.session.add(msg)
        self.db.session.commit()
        return msg
