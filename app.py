from flask import *
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import pickle
import json
import numpy as np

app = Flask(__name__)
app.debug = True
app.secret_key = 'Ranuga D 2008'


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        model = pickle.load(open('model.pkl', 'rb'))
        day = request.form['D']
        day = day.replace('-','')
        day = int(day)
        with open('location_info.json', 'r') as json_file_location:
            info = json.load(json_file_location)
        country = request.form['C']
        country = info[country]
        array = np.array([day, country])
        df = pd.DataFrame(array)
        try:
            result = model.predict(df)
        except:
            result = model.predict(df.T)
        flash(f'Result : {result[0]}', 'success')
        return redirect('/')
    else:
        with open('location_info.json', 'r') as json_file_location:
            info = json.load(json_file_location)
        print(info)
        return render_template('index.html', countries=info.keys())


if __name__ == "__main__":
    app.run(host='192.168.1.9', port=2008)
