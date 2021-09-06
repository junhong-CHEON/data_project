from flask import Response,request,render_template
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from models.Predict import Predict as predictModel
import json
from utils.Util import replace_quotes
from utils.Util import get_now_string

from pandas import DataFrame

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler

db = SQLAlchemy()

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
                rs = predictModel.query.filter(predictModel.명칭_단지코드.like(search)).all()
            except Exception as e:
                return {'rt': replace_quotes(str(e)), 'pubDate':get_now_string()}, 500
            
            for i,v in enumerate(rs):
                rs[i] = v.to_dict()
            
            df = DataFrame(rs)

            df_copy = df.copy()

            drop_list = ['명칭_단지코드','사용승인일','버스정류장','도로명주소','편의시설','복도유형','법정동주소','K_apt_가입일','관리사무소연락처_FAX','도로명','시공사_시행사','건물구조',
                    '경비관리','관리방식','단지분류','소독관리','수전용량','세대전기계약방식','승강기관리형태','일반관리','전기안전관리자법정선임여부','청소관리','홈페이지주소','번지','본번','부번',
                    '화재수신반방식','경도','위도','호선','역','level_0','급수방식','난방방식','분양형태','주차관제_홈네트워크','단지명','계약일','계약년월','승강기대수']
            for i in drop_list:
                df_copy = df_copy.drop(i, axis = 1)
            
            df_copy['연면적'] = df_copy['연면적'].str.replace('㎡', '')
            df_copy['주거전용면적'] = df_copy['주거전용면적'].str.replace('㎡', '')
            df_copy['연면적'] = df_copy['연면적'].str.replace(',', '')
            df_copy['주거전용면적'] = df_copy['주거전용면적'].str.replace(',', '')
            df_copy['동수_세대수'] = df_copy['동수_세대수'].str.replace('세대', '')
            df_copy['면적별_세대현황'] = df_copy['면적별_세대현황'].str.replace(' 세대', '')
            df_copy['면적별_세대현황'] = df_copy['면적별_세대현황'].str.replace('-', '0')

            colon_tok = df_copy['주차대수'].str.rfind(':')
            dea_tok = df_copy['주차대수'].str.rfind('대')

            for i in range(0, len(colon_tok)):
                df_copy['주차대수'][i] = df_copy['주차대수'][i][colon_tok[i] + 1:dea_tok[i]]

            tok = df_copy['동수_세대수'].str.rfind('/')

            for i in range(0, len(tok)):
                df_copy['동수_세대수'][i] = df_copy['동수_세대수'][i][tok[i] + 1:]

            tmp_list = df_copy['부대_복리시설'].str.split(',')
            for i in range(0, len(tmp_list)):
                df_copy['부대_복리시설'][i] = len(tmp_list[i])

            tok = df_copy['면적별_세대현황'].str.rfind('\n')

            for i in range(0, len(tok)):
                df_copy['면적별_세대현황'][i] = df_copy['면적별_세대현황'][i][tok[i] + 1:]

            tok = df_copy['지하철'].str.find('(')

            for i in range(0, len(tok)):
                df_copy['지하철'][i] = len(df_copy['지하철'][i][:tok[i]].split(','))

            tok_1 = df_copy['교육시설'].str.find('(')
            tok_2 = df_copy['교육시설'].str.find(')')
            for i in range(0, len(tok)):
                df_copy['교육시설'][i] = len(df_copy['교육시설'][i][tok_1[i] + 1:tok_2[i]].split(','))

            df_copy.rename(columns={'동수_세대수':'세대수','면적별_세대현황':'135초과세대수','지하철':'인접지하철수','교육시설':'인접초등학교수' }, inplace = True)

            df_copy['시군구'] = df_copy['시군구'].astype('category').cat.rename_categories({string : i for i,string in enumerate(df_copy['시군구'].unique())})

            df_copy['세대수'] = df_copy['세대수'].astype('float64')
            df_copy['135초과세대수'] = df_copy['135초과세대수'].astype('float64')
            df_copy['연면적'] = df_copy['연면적'].astype('float64')
            df_copy['주거전용면적'] = df_copy['주거전용면적'].astype('float64')
            df_copy['주차대수'] = df_copy['주차대수'].astype('float64')
            df_copy['인접지하철수'] = df_copy['인접지하철수'].astype('float64')
            df_copy['인접초등학교수'] = df_copy['인접초등학교수'].astype('float64')

            df_copy['세대수당주차대수'] = df_copy['주차대수'] / df_copy['세대수']
            df_copy['제곱미터당_가격'] = df_copy['거래금액_만원'] / df_copy['전용면적_제곱미터']
            df_copy = df_copy.drop('주차대수', axis = 1)
            df_copy = df_copy.drop('거래금액_만원', axis = 1)

            x_train_set = df_copy.filter(['세대수', '135초과세대수', '연면적', '주거전용면적', 'CCTV대수', '부대_복리시설', '인접지하철수',
                '인접초등학교수', '시군구', '전용면적_제곱미터', '층', '건축년도', '역과의거리_km',
                '세대수당주차대수'])
            print(x_train_set)
            scaler = StandardScaler()
            std_x_test = DataFrame(scaler.transform(x_train_set), columns=x_train_set.columns)
            print(std_x_test)


            value = str(value_1) + ' ' + str(value_2)
            print(value)
            return Response(render_template('index.html', value = value))