from flask import Flask, render_template, flash, request, redirect, url_for, make_response
from PIL import Image, ImageCms
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)



@app.route('/')
def hello_world():
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

