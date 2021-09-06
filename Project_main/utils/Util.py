import datetime as dt

def replace_quotes(s):
    return s.replace('"', '\"').replace("'", "\'")

def get_now_string():
    return dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')