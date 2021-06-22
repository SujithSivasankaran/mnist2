
import requests,uuid
import matplotlib.image as mpimg

from flask import Flask, flash, request, redirect, url_for, render_template

from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = "secret key"

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png','jpg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        img = mpimg.imread(file)
        img = img / 255
        img = img.reshape(784)
        input_data = "{\"data\": [" + str(list(img)) + "]}"
        headers = {'Content-Type': 'application/json'}

        key = '9yqdKWb1llA06MBfdlO4KmU8MfGbDgKa'

        headers = {'Content-Type': 'application/json'}
        headers['Authorization'] = f'Bearer {key}'
        service = 'http://1101520b-7cac-4e8e-b29d-7ca073cc4561.centralus.azurecontainer.io/score'
        resp = requests.post(service, input_data, headers=headers)
        m = resp.text
        flash('The predicted number is: ' + m[1])
        return render_template('index.html')
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run()

