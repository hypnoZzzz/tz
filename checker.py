from flask import Flask, request
from PIL import Image

ALLOWED_EXTENSIONS = set(['png', 'jpg'])
magic_numbers_png = {'png': bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])}
magic_numbers_jpg = {'jpg': bytes([0xFF, 0xD8, 0xFF])}


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
