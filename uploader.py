import json, os, io

from flask import Flask, render_template, request
from PIL import Image

import checker, config, models, saver

from checker import check_extension, check_format, check_integrity, ALLOWED_EXTENSIONS
from config import app
from models import Img, Task, db
from saver import save_, picture_to_db


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """загружает файл"""
    if request.method == 'POST':
        file = request.files['file']
        if save_():
            check_format(), check_integrity()
            if check_format() is not True or check_integrity() is not True:
                return render_template('error.html'), os.remove('uploads/' + file.filename)
            else:
                return picture_to_db(filename=file.filename)
        else:
            return render_template('error.html')
    return render_template('index.html')


def list_id():
    objects = Img.query.all()
    id_list = []
    for object in objects:
        object = object.id
        id_list.append(object)
    return id_list


def ret_user_id():
    """Получает id, введённое пользователем"""
    user_id = int(request.form.get("id_file"))
    id_list = list_id()
    if user_id in id_list:
        return user_id
    else:
        return False, "There is no file with such id"


def object_creation():
    """Создаёт объект задачи"""
    user_id = ret_user_id()
    if ret_user_id():
        try:
            object = Img.query.get(user_id)
            name = str(object.name).rsplit('.', 1)[0]
            format = str(object.name).rsplit('.', 1)[1]
            height = int(request.form.get('height'))
            width = int(request.form.get('width'))
            task_path = object.path
            status = False
            task = Task(name=name, format=format, height=height,
                        width=width, task_path=task_path, status=status)
            db.session.add(task)
            db.session.commit()
            d_base = Task.query.order_by(Task.date).all()
            with open('tasks/tasks.json', 'w') as f:
                json.dump(str(d_base), f, indent=-2, ensure_ascii=False)
                f.close()
            return task
        except ValueError:
            return "There is no such object in the database"
        except ValueError:
            if width == "" or height == "":
                return "You did not enter a width or height value"
        except ValueError:
            if width <= 0:
                return "Width and height cannot be less than or equal to zero"
        except ValueError:
            if height > 9999 or width > 9999:
                return "Height and width cannot be greater than 9999"

    else:
        return "There is no file with such id"


def this_task():
    task_id = int(request.form.get('task_id'))
    task_base = Task.query.all()
    for i in task_base:
        if task_id == i.id:
            return i
        else:
            continue
    return i


def task_handler():
    task = this_task()
    print(task)
    path = str(task.task_path)
    dir_path = 'processed'
    image = Image.open(path)
    height = int(task.height)
    width = int(task.width)
    resize_img = image.resize((height, width), Image.ANTIALIAS)
    processed_img_name = str(task.id) + '_' + str(task.name) + '.' + str(task.format)
    file_path = os.path.join(dir_path, processed_img_name)
    resize_img.save(file_path)
    resize_img.show()














