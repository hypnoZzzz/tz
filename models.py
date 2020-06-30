from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import app

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    format = db.Column(db.String())
    height = db.Column(db.Integer, default=1)
    width = db.Column(db.Integer, default=1)
    status = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    task_path = db.Column(db.Text)

    def __repr__(self):
        return r"{" + '"id": "{}", "name": "{}", "format": "{}", "height": "{}", ' \
                      '"width": "{}", "date": "{}"'.format(self.id, self.name, self.format,
                                                                           self.height, self.width, self.date) + r"}"


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    path = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return r"{" + '"id": "{}", "name": "{}", "path": "{}", "date": "{}"'.format(self.id, self.name, self.path,
                                                                                    self.date) + r"}"
