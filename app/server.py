from flask import *
from flask_cors import CORS

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from models.button_func import testFunc
from models.process_data import *
from models.all_models import *

app = Flask(__name__)

CORS(app)

glob_df = None
glob_X = None
glob_y = None
glob_models = None
glob_model = None
glob_score = None

@app.route("/", methods=['POST'])
def process_page():
    global glob_df
    global glob_X
    global glob_y
    global glob_models
    global glob_model
    global glob_score

    rdata = request.get_json()
    print('\n', 'Flask Received:', rdata, '\n')

    ### Loading the Data ###
    if rdata['phase'] == 1:
        if rdata['name'] == "Selected Iris":  # -> Iris Dataset
            filename = rdata['file']
            df = load_dataset(filename)
        elif rdata['name'] == "Selected Own Data":  # -> User Dataset
            filename = rdata['file']
            default_path = "../data/"
            df = load_dataset(default_path + filename)
        else:
            resp = "Phase 1 Huh? What is this?"

        glob_df = df
        column_names = get_column_names(df)
        first_rows = get_first_rows(df)

        resp = {'column_names': column_names, 'first_rows': first_rows}

    ### Confirming Features and Target ###
    elif rdata['phase'] == 2:
        if rdata['name'] == "Chose Features":  # -> Features
            X_names = rdata['features']
            glob_X = X_names
            resp = "Received Features at BACK."
        elif rdata['name'] == "Chose Target":  # -> Target
            y_name = rdata['target'][0]
            glob_y = y_name
            resp = "Received Target at BACK."
        else:
            resp = "Phase 2 Huh? What is this?"

    ### Selecting Prediction Type ###
    elif rdata['phase'] == 3:
        if rdata['name'] == "Chose Regress":  # -> Regression Prediction
            resp, glob_models = get_models(glob_X, glob_y, glob_df, regression=True)
        elif rdata['name'] == "Chose Classify":  # -> Classification Prediction
            type = "classification"
            resp, glob_models = get_models(glob_X, glob_y, glob_df, regression=False)
        else:
            resp = "Phase 3 Huh? What is this?"

    ### Selecting Prediction Model ###
    elif rdata['phase'] == 4:
        if rdata['name'] == "Chose Model":  # -> Model Selected
            glob_model = rdata['model']
            resp = "Model Received at BACK!"
        else:
            resp = "Phase 4 Huh? What is this?"

        glob_score = run_model(glob_model, glob_models)

    ### Training Prediction Model ###
    elif rdata['phase'] == 5:
        if rdata['name'] == "Model Status":  # -> Checking if Model is Trained
            resp = glob_score
        else:
            resp = "Phase 5 Huh? What is this?"

    ### Training Prediction Model ###
    elif rdata['phase'] == 6:
        if rdata['name'] == "Make Prediction":  # -> Request to Make Prediction
            predictThis = rdata['predictThis']
            resp = predict(predictThis, glob_model, glob_models)
            print("PREDICTION:", resp)
        else:
            resp = "Phase 6 Huh? What is this?"


    print('Sent to JavaScript:', resp, jsonify(resp), '\n')
    return jsonify(resp)

#############################

if __name__ == '__main__':
    app.run(host='localhost')
