from flask import Flask,render_template,request,session
from werkzeug.utils import secure_filename
import os
import cv2
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
SKETCH_FOLDER = os.path.join('static', 'sketches')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SKETCH_FOLDER'] = SKETCH_FOLDER

def imgToSketch(img,disp=False,show_orig = False,edge=False,thres=100):
    image = cv2.imread(img)
    if show_orig: cv2.imshow(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,100,200)
    if edge: cv2.imshow(255-edges)
    _, shade = cv2.threshold(gray, thres, 255, cv2.THRESH_BINARY)
    shade[shade<100] = 50
    sketch = cv2.subtract(shade,edges)
    if disp: cv2.imshow(sketch)
    return sketch

@app.route("/",methods=['POST','GET'])
def home():
    if request.method=='POST':
        image = request.files['image']
        img_filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        img = imgToSketch(path)
        print(img)
        sketch = os.path.join(app.config['SKETCH_FOLDER'], img_filename)
        print(sketch)
        cv2.imwrite(sketch,img)

        return render_template('index.html',img = sketch)
    return render_template("index.html")

app.run(debug=True)