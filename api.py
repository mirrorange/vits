from crypt import methods
from pyexpat import model
from time import time
from flask import Flask, request,send_file
from inference import vits_inference
import os
import time
from threading import Timer

def load_model(model_name):
    if not model_name in model_list:
        model_list[model_name] = vits_inference(model_name)

def release_model(model_name):
    if not model_name in model_list:
        del model_list[model_name]

model_list = {}

app = Flask(__name__)

@app.route('/')
def index():
    return "VITS API"

@app.route('/synthesis', methods=['GET', 'POST'])
def synthesis():
    model_name = request.args.get('model_name')
    target_text = request.args.get('target_text')
    speaker_id = request.args.get('speaker_id')
    output_file = os.path.join("output",str(time.time()) + ".wav")
    if not model_name in model_list:
        load_model(model_name)
    try:
        model_list[model_name].synthesis(output_file,target_text,speaker_id)
        return send_file(output_file)
    except:
        return "Synthesis failed"

@app.route("/load",methods=['GET', 'POST'])
def load():
    model_name = request.args.get('model_name')
    try:
        load_model(model_name)
        return "Model Loaded"
    except:
        return "Model loading failed"

@app.route("/release",methods=['GET', 'POST'])
def release():
    model_name = request.args.get('model_name')
    release_model(model_name)
    return "Model released"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5123)