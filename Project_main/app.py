# package import
import os
import sys
from flask import Flask, render_template, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
# registration modul path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# controller class import
from controllers.Predict import Predict as predictController

# Flask object create
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:1234567890@izen.cxppaurfujpc.ap-northeast-2.rds.amazonaws.com:3306/project1?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# restful object create
api = Api(app)

@app.route('/', methods=['GET'])
def page():
    return render_template('index.html')

# controller url mapping
api.add_resource(predictController, '/predict', endpoint='predict', methods=['GET'])
api.add_resource(predictController, '/post', endpoint='/post', methods=['POST'])

# application activate
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9901, debug=True) 