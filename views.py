import glob
import os

from flask import Flask, request, redirect, url_for, send_from_directory
from PIL import Image
from werkzeug.utils import secure_filename

magic_numbers_png = {'png': bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])}
magic_numbers_jpg = {'jpg': bytes([0xFF, 0xD8, 0xFF])}

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """проверяет, что расширение файла допустимо"""

    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """загружает файл, проверяет действителен ли формат
     и перенаправляет пользователя на URL с загруженным файлом"""
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.chdir('uploads')
            with open(file.filename, 'rb') as fd:
                file_head = fd.read()
            if file_head.startswith(magic_numbers_jpg['jpg']) or file_head.startswith(magic_numbers_png['png']):
                return redirect(url_for('uploaded_file',
                                        filename=filename))
            else:
                os.remove(file.filename)
                return "Error 302. Invalid file format. Add image format 'jpg' or 'png'. File deleted"
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """обслуживание загруженных файлов"""
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run()
