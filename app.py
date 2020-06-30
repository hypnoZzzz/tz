import json, os, io

from flask import Flask, render_template, request
# from functools import lru_cache
# from flask_sqlalchemy import SQLAlchemy
# from PIL import Image
# from werkzeug.utils import secure_filename

import checker, config, models, saver, uploader

from checker import check_extension, check_format, check_integrity, ALLOWED_EXTENSIONS
from config import app
from models import Img, Task, db
from saver import save_, picture_to_db
from uploader import upload_file, object_creation, \
    ret_user_id, list_id, this_task, task_handler


@app.route('/', methods=['GET', 'POST'])
def index():
    upload_file()
    return render_template('index.html')


@app.route('/enter_id/')
def enter_id():
    """Переводит пользователя на страницу поиска по id"""
    return render_template("enter_id.html", )


@app.route('/enter_id/', methods=['GET', 'POST'])
def saved():
    task = object_creation()
    return render_template('change_data.html', task=task)


@app.route('/search_task/', methods=['GET', 'POST'])
def answer():
    return render_template('search_task')


@app.route('/processing/', methods=['GET', 'POST'])
def processing():
    this_task()
    task_handler()
    return render_template('processing.html')


if __name__ == '__main__':
    app.run(debug=True)
