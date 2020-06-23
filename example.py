# не пойму, как сделать проверку, что пользователь не отправил пустую строку
# позже функции проверки и сохранения вынесу в отдельный модуль
import os

from flask import Flask, render_template, request
from PIL import Image
from werkzeug.utils import secure_filename

magic_numbers_png = {'png': bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])}
magic_numbers_jpg = {'jpg': bytes([0xFF, 0xD8, 0xFF])}

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
            print('Valid image')  # пока оставлю принт, чтобы видеть, что работает
            return True
        except Exception:
            print('Invalid image')  # пока оставлю принт, чтобы видеть, что работает
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
            return render_template('uploads.html')
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
