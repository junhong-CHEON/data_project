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

            rs2 = None
            
            try:
                rs2 = predictModel.query.filter(predictModel.명칭_단지코드.like(search)).all()
            except Exception as e:
                return {'rt': replace_quotes(str(e)), 'pubDate':get_now_string()}, 500
            
            for i,v in enumerate(rs2):
                rs2[i] = v.to_dict()
            
            df2 = DataFrame(rs2)
            df2_copy = df2.copy()

            #실거래가 chart.js 필요한 변수
            x_df1 = df2_copy.filter(["전용면적_제곱미터","거래금액_만원"])
            x_df1=x_df1.sort_values(by=["전용면적_제곱미터"])
            x_df1 = x_df1.reset_index(drop=True)
 
            x_value = []
            y_value = []
            for i in range(0,len(x_df1)):
                x_value.append(x_df1["전용면적_제곱미터"][i])
                y_value.append(x_df1["거래금액_만원"][i])     

            #아파트정보 필요한 변수
            ta_df1 = df2.copy()
            ta_df1 = ta_df1.filter(["단지명","도로명","면적별_세대현황","사용승인일","동수_세대수","연면적","주거전용면적","주차대수","CCTV대수","위도","경도"])
            ta1 = ta_df1["단지명"][0]
            ta2 = ta_df1["도로명"][0]
            ta3 = ta_df1["면적별_세대현황"][0]
            ta4 = ta_df1["사용승인일"][0]
            ta5 = ta_df1["동수_세대수"][0]
            ta6 = ta_df1["연면적"][0]
            ta7 = ta_df1["주거전용면적"][0]
            ta8 = ta_df1["주차대수"][0]
            ta9 = ta_df1["CCTV대수"][0]
            map_1 = "%f" % ta_df1["위도"][0]
            map_2 = "%f" % ta_df1["경도"][0]
             

            return Response(render_template('indexpost.html', value = value, x_value = x_value, y_value=y_value, search=search,
             ta1=ta1, ta2=ta2, ta3=ta3, ta4=ta4, ta5=ta5, ta6=ta6, ta7=ta7, ta8=ta8, ta9=ta9, map_1=map_1, map_2=map_2))