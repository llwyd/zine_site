from flask import Flask, render_template, flash, request, redirect, url_for, make_response, abort
from PIL import Image, ImageCms
from werkzeug.utils import secure_filename
import uuid
import os
from pathlib import Path

app = Flask(__name__)

app.config['UPLOAD_EXT'] = ['.jpg', '.png', '.jpeg']
app.config['UPLOAD_PATH'] = 'uploads'
app.config['MAX_SIZE'] = 1024 * 1024

@app.route('/')
def main_page():
        client_id = request.cookies.get('client_id')
        if client_id is None:
            # create new uuid
            client_id = str(uuid.uuid4())
            print("New User")
            resp = make_response(render_template('index.html',client_id=client_id))
            resp.set_cookie('client_id',client_id)
            return resp
        else:
            return render_template('index.html',client_id=client_id)

@app.route('/',methods=['POST'])
def upload_image():
    # Retrieve client id
    client_id = request.cookies.get('client_id')
    if client_id is None:
        # should never reach here
        return redirect(url_for('critical_failure'))
    print(client_id)
    
    # Process incoming file
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = Path(filename).suffix
        print(file_ext)
        if file_ext not in app.config['UPLOAD_EXT']:
            abort(400)
        fpn = app.config['UPLOAD_PATH'] + '/' + client_id
        uploaded_file.save( fpn + str('_s') + file_ext)

    return redirect(url_for('main_page'))

@app.route('/assert')
def critical_failure():
    return 'CRITICAL FAILURE :('
