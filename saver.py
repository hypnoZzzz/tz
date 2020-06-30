import json, os, io
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from config import app
from checker import check_extension
from models import Img, Task, db


def save_():
    """Сохраняет файл на диск"""
    file = request.files['file']
    if file and check_extension(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return True
    else:
        return False


def picture_to_db(filename):
    """Получает имя файла, путь к файлу,
    сохраняет его в базе данных, сериализует данные из неё
    в json и отображает имя и id файла пользователю"""
    file = request.files['file']
    imgI = io.open("uploads/" + file.filename, 'rb')
    name = filename.rsplit('/', 1)[-1]
    path = imgI.name
    image = Img(name=name, path=path)

    try:
        db.session.add(image)
        db.session.commit()
        database = Img.query.order_by(Img.date).all()
        with open('tasks/database.json', 'w') as f:
            json.dump(str(database), f, indent=-2, ensure_ascii=False)
            f.close()
        return render_template('/uploads.html', image=image)
    except Exception:
        return "error adding to database"


