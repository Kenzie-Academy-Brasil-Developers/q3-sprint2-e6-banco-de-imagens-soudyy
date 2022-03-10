from http.client import REQUEST_ENTITY_TOO_LARGE
import os
from http import HTTPStatus
from fileinput import filename
from pathlib import Path
from werkzeug.security import safe_join
from app.kenzie.image import get_file_path, upload_files
from flask import Flask, jsonify, request, safe_join, send_file

app = Flask(__name__)

PATH = os.getenv('FILES_DIRECTORY')
EXTENSION = os.getenv("ALLOWED_EXTENSIONS").split(',')
IMAGE_DIRECTORY = os.getenv('IMAGE_DIRECTORY')
FILES_DIRECTORY = os.getenv('FILES_DIRECTORY')
ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS')
MAX_CONTENT_LENGTH = os.getenv('MAX_CONTENT_LENGTH')


if not os.path.isdir(PATH):
    os.mkdir(PATH)
    for item in EXTENSION:
        file_path = os.path.join(PATH,EXTENSION)
        os.mkdir(file_path)

@app.post('/upload')
def upload():
    size = request.content_length
    files_list = request.files  
    if size > int(MAX_CONTENT_LENGTH):
        return {'msg': 'file too large'} ,HTTPStatus.REQUEST_ENTITY_TOO_LARGE
    for file in files_list.values():   
        file_size = file.content_length 
        print(file_size)
        filename = file.filename
        path = os.path.abspath(FILES_DIRECTORY)
        file_extension = filename.split('.')[1]
        dir_path = safe_join(path,file_extension)
        file_path = safe_join(dir_path,filename)
        allowed = ALLOWED_EXTENSIONS.split(',')
    
        if not allowed.__contains__(file_extension):
            return {'msg':'Some files are not supported'},HTTPStatus.UNSUPPORTED_MEDIA_TYPE  

        if os.path.isfile(file_path):
            return {'msg':'This file already exist'},HTTPStatus.CONFLICT

        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)

        upload_files(file,dir_path)
    return {'msg': "Image uploaded"}, HTTPStatus.CREATED


@app.get('/files')
def list_files():
    *_,files_list = next(os.walk(IMAGE_DIRECTORY))
    return {'msg': files_list}, HTTPStatus.OK

@app.get('/files/<extension>')
def list_files_by_extension(extension):
    *_,files_list = next(os.walk(IMAGE_DIRECTORY))
    chosen_format = []
    if EXTENSION.__contains__(extension):
        for item in files_list:
            if item.split('.')[1] == extension:
                chosen_format.append(item)
        return {'msg': chosen_format}
    return {'msg': 'Format not Found'},HTTPStatus.NOT_FOUND

@app.get('/download/<filename>')
def download(filename: str):
    extension = filename.split('.')[1]
    if EXTENSION.__contains__(extension):
        filepath = get_file_path(filename)
        return send_file(filepath, as_attachment=True),HTTPStatus.OK
    return {'msg': 'Format not Found'},HTTPStatus.NOT_FOUND
    

@app.get('/download-zip')
def download_dir_as_zip():
    extension = request.args.get('file_extension')
    compression = request.args.get('compression_ratio')
    folder_to_record = f'/tmp/{extension}.zip'
    if EXTENSION.__contains__(extension):               
        command = f"zip -r {compression} {folder_to_record} {FILES_DIRECTORY} "
        os.system(command)
        return send_file(folder_to_record,as_attachment=True),HTTPStatus.OK
    return {'msg': 'Format not Found'},HTTPStatus.NOT_FOUND

