from flask import Response,request,render_template
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from models.Predict import Predict as predictModel
from models.Predict import Standard_scale_table as Standard
import json
from utils.Util import replace_quotes
from utils.Util import get_now_string

from pandas import DataFrame

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler
from tensorflow.python.keras.models import load_model
from numpy import argmax
import os
print(os.path.realpath(__file__))
model = load_model('../seoul_housing.h5')
# JSON 페이지를 담당하는 클래스
class Predict(Resource):
    def get(self):
        # 조회 결과를 저장할 빈 변수
        rs = None
        
        try:
            # 전체 데이터 조회
            rs = predictModel.query.limit(5).all()
        except Exception as e:
            return {'rt': replace_quotes(str(e)), 'pubDate': get_now_string()}, 500
        
        # 전체 조회 결과가 리스트이고, 리스트의 각 원소가 departmentModel의 객체 타입이므로
        # JSON 출력을 위해 각 원소를 dict로 변환
        for i,v in enumerate(rs):
            rs[i] = v.to_dict()
        
        return {'rt': 'OK', 'item': rs, 'pubDate': get_now_string()}

    def post(self):
            
            rs = None
            value_1 = request.form['gu']
            value_2 = request.form['search']
            search = "%{}%".format(value_2)
            
            try:
                rs = Standard.query.filter(Standard.아파트명.like(search)).all()
            except Exception as e:
                return {'rt': replace_quotes(str(e)), 'pubDate':get_now_string()}, 500
            
            for i,v in enumerate(rs):
                rs[i] = v.to_dict()
            
            df = DataFrame(rs)
            df_copy = df.copy()

            x_test = df_copy.filter(['세대수',
                '초과세대수_135',
                '주거전용면적',
                'CCTV대수',
                '부대_복리시설',
                '인접초등학교수',
                '전용면적_제곱미터',
                '층',
                '건축년도',
                '역과의거리_km',
                '세대수당주차대수',
                '대형평수세대비율',
                '세대당CCTV대수'])
            value = 0

            yhat = model.predict(x_test)
            for i,v in enumerate(yhat):
                value = value + yhat[i][0]
            value = value/len(yhat)
            value = value_1 + ' ' + value_2 + '의 예상가격: ㎡당' + str(round(value,4)).replace('.','만') + '원 입니다.'
            return Response(render_template('index.html', value = value))