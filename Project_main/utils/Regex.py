import re

class Regex:
    # 값의 존재 여부를 검사한다.
    def value(self, v, err = '내용이 없습니다.'):
        if not v or not str(v).strip():
            raise Exception(err)
        return True
    
    # 입력값이 지정된 글자수를 초과했는지 검사한다.
    def max_length(self, v, lim, err = '문자열이 지정된 길이를 초과했습니다.'):
        if len(str(v).strip()) > lim:
            raise Exception(err)
        return True
    
    # 입력값이 지정된 글자수 미만인지 검사한다.
    def min_length(self, v, lim, err = '문자열이 지정된 길이 보다 작습니다.'):
        if len(str(v).strip()) < lim:
            raise Exception(err)
        return True
    
    # 두 문자열의 값이 동일한지 검사한다.
    def compare_to(self, v1, v2, err = '두 문자열의 내용이 동일하지 않습니다.'):
        if str(v1).strip() != str(v2).strip():
            raise Exception(err)
        return True
    
    # 입력값이 정규표현식을 충족하는지 검사한다.
    def field(self, v, r, err = '주어진 문자열이 지정된 형식을 만족하지 않습니다.'):
        # v의 내용이 없을 경우, 정규표현식 검사 자체를 수행하지 못하므로 
        # 입력값의 존재 여부를 먼저 검사해야 한다.
        self.value(v, err)
        
        # 주어진 정규표현식을 식별한다.
        p = re.compile(r)
        
        # v의 내용이 정규표현식(r)을 충족하지 않을 경우
        if p.match(v) is None:
            raise Exception(err)
        
        return True
    
    def num(self, v, err = '숫자 형식이 아닙니다.'):
        return self.field(v, "^[0-9]*$", err)

    # 영문으로만 이루어 졌는지 검사
    def eng(self, v, err = '영어로만 구성되어 있지 않습니다.'):
        return self.field(v, "^[a-zA-Z]*$", err)

    # 한글로만 이루어 졌는지 검사
    def kor(self, v, err = '한글로만 구성되어 있지 않습니다.'):
        return self.field(v, "^[ㄱ-ㅎ가-힣]*$", err)

    # 영문과 숫자로 이루어 졌는지 검사
    def eng_num(self, v, err = '영문과 숫자로만 구성되어 있지 않습니다.'):
        return self.field(v, "^[a-zA-Z0-9]*$", err)

    # 한글과 숫자로만 이루어 졌는지 검사
    def kor_num(self, v, err = '한글과 숫자로만 구성되어 있지 않습니다.'):
        return self.field(v, "^[ㄱ-ㅎ가-힣0-9]*$", err)

    # 이메일주소 형식인지 검사
    def email(self, v, err = '이메일 형식이 아닙니다.'):
        return self.field(v, "^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$", err)

    # 핸드폰 번호 형식인지 검사
    def cellphone(self, v, err = '핸드폰 번호 형식이 아닙니다.'):
        return self.field(v, "^01(?:0|1|[6-9])(?:\d{3}|\d{4})\d{4}$", err)

    # 집전화 형식인지 검사
    def telphone(self, v, err = '집전화번호 형식이 아닙니다.'):
        return self.field(v, "^\d{2,3}\d{3,4}\d{4}$", err)
    
    # 주민번호 형식인지 검사
    def jumin(self, v, err = '주민번호 형식이 아닙니다.'):
        return self.field(v, "^\d{6}[1-4]\d{6}", err)

    # 핸드폰번호 형식과 집전화 번호 형식 둘중 하나를 충족하는지 검사
    def phone(self, v, err = '핸드폰 혹은 집전화 번호 형식이 아닙니다.'):
        check1 = "^01(?:0|1|[6-9])(?:\d{3}|\d{4})\d{4}$"
        check2 = "^\d{2,3}\d{3,4}\d{4}$"
        
        p1 = re.compile(check1)
        p2 = re.compile(check2)
        
        if p1.match(v) is None and p2.match(v) is None:
            raise Exception(err)
        
        return True
    
    # 입력값 숫자인 경우 주어진 범위 안에서만 허용
    def between(self, v, min_value, max_value, err = '문자열이 지정된 길이를 초과했습니다.'):
        self.value(v, err)
        self.num(v, err)
        
        n = int(v)
        if n < min_value or n > max_value:
            raise Exception(err)
        return True
        
        

# 이 소스가 import되지 않을 때(직접 실행될 경우)만 실행하는 블록
if __name__ == "__main__":
    regex = Regex()
    msg = "010sdfsd12342345"
    
    try:
        print(regex.phone(msg))
    except Exception as e:
        print(e)