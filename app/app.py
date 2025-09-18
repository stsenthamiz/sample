from flask import Flask, render_template, request, redirect
from tensorflow.keras.models import load_model
import os
from draw_traits import process_image

app = Flask(__name__)

# Model path
MODEL_PATH = '../model/mobilenetv2_cattle_buffalo.h5'
model = load_model(MODEL_PATH)

# Upload folder
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        processed_file_path, result = process_image(filepath, model)

        return render_template('index.html',
                               result=result,
                               original_file=file.filename,
                               processed_file=os.path.basename(processed_file_path))

if __name__ == "__main__":
    app.run(debug=True)