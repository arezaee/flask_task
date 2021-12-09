from app import db
import enum


class StatusType(enum.Enum):
    TODO = 1
    INPROGRESS = 2
    DONE = 3

    def __str__(self):
        return self.name


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String)
    description = db.Column(db.String)
    status = db.Column(db.Enum(StatusType), default=StatusType.TODO)
    due_date = db.Column(db.Date)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "status": str(self.status),
            "due_date": str(self.due_date.strftime('%d-%m-%Y'))
        }


class MyUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "password": self.password,
        }
