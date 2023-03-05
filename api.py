from time import time
from flask import Flask, request,send_file
from inference import vits_inference
import os

class ModelNotFoundError(RuntimeError):
    def __init__(self, model_name):
        self.model_name = model_name
        self.message = f"Model [ {self.model_name} ] Not Found!"

def load_model(model_name):
    if not model_name in model_list:
        raise ModelNotFoundError(model_name)
    if not model_name in models:
        models[model_name] = vits_inference(model_name)

def release_model(model_name):
    if model_name in models:
        del models[model_name]

model_list = ["paimon","atri","ljs"]
models = {}

app = Flask(__name__)

@app.route('/')
def index():
    return "VITS API"

@app.route('/synthesis', methods=['GET', 'POST'])
def synthesis():
    model_name = request.args.get('model_name',type=str)
    target_text = request.args.get('target_text',type=str)
    speaker_id = request.args.get('speaker_id',default=-1,type=int)
    output_file = os.path.join("output",str(time()) + ".wav")
    if not model_name in models:
        try:
            load_model(model_name)
        except ModelNotFoundError as e:
            return e.message
        except:
            return "Model loading failed"
    try:
        models[model_name].synthesis(output_file,target_text,speaker_id)
        return send_file(output_file)
    except:
        return "Synthesis failed"

@app.route("/load",methods=['GET', 'POST'])
def load():
    model_name = request.args.get('model_name')
    try:
        load_model(model_name)
        return "Model Loaded"
    except ModelNotFoundError as e:
        return e.message
    except:
        return "Model loading failed"

@app.route("/release",methods=['GET', 'POST'])
def release():
    model_name = request.args.get('model_name')
    release_model(model_name)
    return "Model released"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5123)