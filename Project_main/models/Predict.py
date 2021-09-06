from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

# 클래스 선언시 괄호 안에 들어 가는 내용은 해당 기능을 그대로 상속 받겠다는 의미
class Predict(db.Model, SerializerMixin):
    __tablename__ = 'add_distance_fix'
    level_0 = db.Column(db.Integer, primary_key=True, autoincrement=True)
    명칭_단지코드 = db.Column(db.String, nullable=False)
    사용승인일 = db.Column(db.String, nullable=False)
    동수_세대수 = db.Column(db.String, nullable=False)
    면적별_세대현황 = db.Column(db.String, nullable=False)
    연면적 = db.Column(db.String, nullable=False)
    주거전용면적 = db.Column(db.String, nullable=False)
    주차대수 = db.Column(db.String, nullable=False)
    CCTV대수 = db.Column(db.Float, nullable=False)
    승강기대수 = db.Column(db.Integer, nullable=False)
    시공사_시행사 = db.Column(db.String, nullable=False)
    도로명주소 = db.Column(db.String, nullable=True)
    법정동주소 = db.Column(db.String, nullable=False)
    부대_복리시설 = db.Column(db.String, nullable=False)
    지하철 = db.Column(db.String, nullable=False)
    버스정류장 = db.Column(db.String, nullable=False)
    교육시설 = db.Column(db.String, nullable=False)
    편의시설 = db.Column(db.String, nullable=False)
    K_apt_가입일 = db.Column(db.String, nullable=False)
    건물구조 = db.Column(db.String, nullable=True)
    경비관리 = db.Column(db.String, nullable=False)
    관리방식 = db.Column(db.String, nullable=False)
    관리사무소연락처_FAX = db.Column(db.String, nullable=True)
    급수방식 = db.Column(db.String, nullable=False)
    난방방식 = db.Column(db.String, nullable=False)
    단지분류 = db.Column(db.String, nullable=False)
    복도유형 = db.Column(db.String, nullable=False)
    분양형태 = db.Column(db.String, nullable=False)
    세대전기계약방식 = db.Column(db.String, nullable=False)
    소독관리= db.Column(db.String, nullable=False)
    수전용량 = db.Column(db.String, nullable=True)
    승강기관리형태 = db.Column(db.String, nullable=False)
    일반관리 = db.Column(db.String, nullable=True)
    전기안전관리자법정선임여부 = db.Column(db.String, nullable=False)
    주차관제_홈네트워크 = db.Column(db.String, nullable=False)
    청소관리 = db.Column(db.String, nullable=True)
    홈페이지주소 = db.Column(db.String, nullable=False)
    화재수신반방식 = db.Column(db.String, nullable=False)
    시군구 = db.Column(db.String, nullable=False)
    번지 = db.Column(db.String, nullable=False)
    본번 = db.Column(db.Float, nullable=False)
    부번 = db.Column(db.Float, nullable=False)
    단지명 = db.Column(db.String, nullable=False)
    전용면적_제곱미터 = db.Column(db.Float, nullable=True)
    계약년월 = db.Column(db.Float, nullable=False)
    계약일 = db.Column(db.Float, nullable=False)
    거래금액_만원 = db.Column(db.Float, nullable=False)
    층 = db.Column(db.Float, nullable=False)
    건축년도 = db.Column(db.Float, nullable=False)
    도로명 = db.Column(db.String, nullable=True)
    경도 = db.Column(db.Float, nullable=True)
    위도 = db.Column(db.Float, nullable=False)
    역과의거리_km = db.Column(db.Float, nullable=False)
    호선 = db.Column(db.String, nullable=False)
    역 = db.Column(db.String, nullable=False)
    
    # 자동증가를 제외한 항목들을 파라미터로 받아서 멤버변수에 맵핑
    def __init__(self, 명칭_단지코드, 사용승인일,동수_세대수, 면적별_세대현황, 연면적, 주거전용면적, 주차대수, CCTV대수,
    승강기대수, 시공사_시행사,도로명주소,법정동주소,부대_복리시설,지하철,버스정류장,교육시설,편의시설,K_apt_가입일,
    건물구조,경비관리,관리방식,관리사무소연락처_FAX,급수방식,난방방식,단지분류,복도유형,분양형태,
    세대전기계약방식,소독관리,수전용량,승강기관리형태,일반관리,전기안전관리자법정선임여부,주차관제_홈네트워크,
    청소관리,홈페이지주소,화재수신반방식,시군구,번지,본번,부번,단지명,전용면적_제곱미터,계약년월,계약일,거래금액_만원,
    층,건축년도,도로명,경도,위도,역과의거리_km,호선,역):
    
        self.명칭_단지코드 = 명칭_단지코드
        self.사용승인일 = 사용승인일
        self.동수_세대수 = 동수_세대수
        self.면적별_세대현황 = 면적별_세대현황
        self.연면적 = 연면적
        self.주거전용면적 = 주거전용면적
        self.주차대수 = 주차대수
        self.CCTV대수 = CCTV대수
        self.승강기대수 = 승강기대수
        self.시공사_시행사 = 시공사_시행사
        self.도로명주소 = 도로명주소
        self.법정동주소 = 법정동주소
        self.부대_복리시설 = 부대_복리시설
        self.지하철 = 지하철
        self.버스정류장 = 버스정류장
        self.교육시설 = 교육시설
        self.편의시설 = 편의시설
        self.K_apt_가입일 = K_apt_가입일
        self.건물구조 = 건물구조
        self.경비관리 = 경비관리
        self.관리방식 = 관리방식
        self.관리사무소연락처_FAX = 관리사무소연락처_FAX
        self.급수방식 = 급수방식
        self.난방방식 = 난방방식
        self.단지분류 = 단지분류
        self.복도유형 = 복도유형
        self.분양형태 = 분양형태
        self.세대전기계약방식 = 세대전기계약방식
        self.소독관리 = 소독관리
        self.수전용량 = 수전용량
        self.승강기관리형태 = 승강기관리형태
        self.일반관리 = 일반관리
        self.전기안전관리자법정선임여부 = 전기안전관리자법정선임여부
        self.주차관제_홈네트워크 = 주차관제_홈네트워크
        self.청소관리 = 청소관리
        self.홈페이지주소 = 홈페이지주소
        self.화재수신반방식 = 화재수신반방식
        self.시군구 = 시군구
        self.번지 = 번지
        self.본번 = 본번
        self.부번 = 부번
        self.단지명 = 단지명
        self.전용면적_제곱미터 = 전용면적_제곱미터
        self.계약년월 = 계약년월
        self.계약일 = 계약일
        self.거래금액_만원 = 거래금액_만원
        self.층 = 층
        self.건축년도 = 건축년도
        self.도로명 = 도로명
        self.경도 = 경도
        self.위도 = 위도
        self.역과의거리_km = 역과의거리_km
        self.호선 = 호선
        self.역 = 역