from flask_sqlalchemy import SQLAlchemy

import config
from config import app
from models import Img, Task, db


db.create_all()
