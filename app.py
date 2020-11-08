from flask import Flask, render_template, flash, request, redirect, url_for, make_response, abort, send_from_directory 
from PIL import Image, ImageCms
from werkzeug.utils import secure_filename
import uuid
import os
from pathlib import Path
import cmyk
import version

app = Flask(__name__)

app.config['UPLOAD_EXT'] = ['.jpg', '.png', '.jpeg']
app.config['UPLOAD_PATH'] = 'uploads'
app.config['MAX_SIZE'] = 1024 * 1024

@app.route('/')
def main_page():
        print(version.Version())
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

        # perform CMYK decomposition
        cmyk.Extract(app.config['UPLOAD_PATH'], client_id, file_ext)
    return redirect(url_for('main_page'))

@app.route('/uploads/<clientid>/<layer>')
def get_image_s(clientid,layer):
    print(layer)
    if layer is 'C':
        return send_from_directory(app.config['UPLOAD_PATH'],filename=clientid+str('_c.jpg'))
    elif layer is 'M':
        return send_from_directory(app.config['UPLOAD_PATH'],filename=clientid+str('_m.jpg'))
    elif layer is 'Y':
        return send_from_directory(app.config['UPLOAD_PATH'],filename=clientid+str('_y.jpg'))
    elif layer is 'K':
        return send_from_directory(app.config['UPLOAD_PATH'],filename=clientid+str('_k.jpg'))
    else:
        return send_from_directory(app.config['UPLOAD_PATH'],filename=clientid+str('_s.jpg'))

@app.route('/assert')
def critical_failure():
    return 'CRITICAL FAILURE :('
