from http import HTTPStatus
import os
from flask import request, safe_join
from werkzeug.utils import secure_filename
from datetime import datetime as dt


PATH = os.getenv('FILES_DIRECTORY')
IMAGE_DIRECTORY = os.getenv('IMAGE_DIRECTORY')
FILES_DIRECTORY = os.getenv('FILES_DIRECTORY')

def get_file_path(filename: str):
    abs_path = os.path.abspath(IMAGE_DIRECTORY)
    filepath = safe_join(abs_path,filename)
    return filepath


def upload_files(file,path): 
    filename = file.filename
    file_path = safe_join(path,filename)
    file.save(file_path)
    return file_path