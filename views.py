# не пойму, как сделать проверку, что пользователь не отправил пустую строку
import json
import os
import io

from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from werkzeug.utils import secure_filename

# сохраняем "магические байты" нужных форматов
magic_numbers_png = {'png': bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])}
magic_numbers_jpg = {'jpg': bytes([0xFF, 0xD8, 0xFF])}

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# файл не должен весить больше
app.config['MAX_CONTENT_LENGTH'] = 30*1024*1024  # 30 МБ
# app.config['MAX_CONTENT_LENGTH'] = 1*1024*1024  # 1 МБ
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(150), nullable=False)
    height = db.Column(db.Integer, default=1)
    width = db.Column(db.Integer, default=1)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    img_id = db.Column(db.Integer, db.ForeignKey('img.id'))

    def __repr__(self):
        return '<Task %r>' % self.id


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    path = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return r"{"+'"id": "{}", "name": "{}", "path": "{}", "date": "{}"'.format(self.id, self.name, self.path, self.date)+r"}"


def check_extension(filename):
    """проверяет, что расширение файла допустимо"""

    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def check_format():
    """Проверяет формат файла"""
    file = request.files['file']
    with open('uploads/' + file.filename, 'rb') as fd:
        file_head = fd.read()
        if file_head.startswith(magic_numbers_jpg['jpg']) or file_head.startswith(magic_numbers_png['png']):
            return True

        else:
            fd.close()

    return check_format


def check_integrity():
    """Проверяет целостность файла"""
    file = request.files['file']
    if check_format() is True:
        img = Image.open('uploads/' + file.filename)
        try:
            img.verify()
            return True
        except Exception:
            return False


def save_():
    """Сохраняет файл"""
    file = request.files['file']
    if file and check_extension(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """загружает файл"""
    if request.method == 'POST':
        file = request.files['file']
        save_(), check_format(), check_integrity()
        if check_format() is not True or check_integrity() is not True:
            return render_template('error.html'), os.remove('uploads/' + file.filename)
        else:
            return save_to_database(filename=file.filename)
    return render_template('index.html')


@app.route('/uploads.html')
def save_to_database(filename):
    """Получает имя файла, путь к файлу,
    сохраняет его в базе данных, сериализует данные из неё
    в json и отображает имя и id файла пользователю"""
    file = request.files['file']
    img = io.open("uploads/" + file.filename, 'rb')
    name = filename.rsplit('/', 1)[-1]
    path = img.name
    image = Img(name=name, path=path)

    try:
        db.session.add(image)
        db.session.commit()
        database = Img.query.order_by(Img.date).all()  # хранит объект сессии в виде списка словарей
        with open('tasks/database.json', 'w') as f:
            json.dump(str(database), f, indent=2, ensure_ascii=False)

            f.close()
        return render_template('/uploads.html', image=image)
    except Exception:
        return "error adding to database"


@app.route('/enter_id/')
def enter_id():
    """Переводит пользователя на страницу поиска по id"""
    return render_template("enter_id.html")


@app.route('/enter_id/', methods=['GET', 'POST'])
def search_by_id():
    if request.method == 'POST':
        file_id = request.form.get('id_file')
        with open('tasks/database.json') as database:

            if file_id not in database:
                return "There is no file with such id"
    return render_template('change_data.html', database=database)


if __name__ == '__main__':
    app.run()
