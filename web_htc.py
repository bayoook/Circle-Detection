from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import sys
import cv2 as cv
import numpy as np

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, template_folder='template/', static_folder='static/assets',)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def redir():
    return redirect('https://min4tozaki.me')

@app.route('/sismul', methods=['GET', 'POST'])
def upload_file():
    def image_image(img):
        filename = img
        # Loads an image
        src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_COLOR)
        # Check if image is loaded fine
        if src is None:
            print ('Error opening image!')
            print ('Usage: hough_circle.py [image_name -- default ' + default_file + '] \n')
            return -1
        gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
        gray = cv.medianBlur(gray, 5)
        rows = gray.shape[0]
        param0 = int(20 if rows / 8 < 20 else 50 if rows / 12 > 50 else rows / 12)
        param1 = int(100 if rows * 1.5 < 100 else 500 if rows * 1.5 > 500  else rows * 1.5)
        param2 = int(20 if rows / 12 < 20 else 45 if rows / 12 > 45 else rows / 12)
        circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, param0,
                                param1=param1, param2=param2,
                                minRadius=0, maxRadius=int(rows / 4.5))
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv.circle(src, center, 1, (0, 100, 100), 3)
                # circle outline
                radius = i[2]
                cv.circle(src, center, radius, (255, 0, 255), 3)
        # cv.imshow("detected circles", src)
        # cv.waitKey(0)
        img = img.replace('uploads/', '')
        cv.imwrite('static/assets/circle/' + img, src)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_image('uploads/' + filename)
            return redirect(url_for('upload_file', filename=filename))
    return render_template('index.html')

if __name__ == "__main__":
    app.secret_key = 'min4tozaki_sana'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(host='0.0.0.0', port='80')

