from flask import Flask, render_template, request, redirect, session
import pymysql
from datetime import datetime

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = '시크릿 키'

db = pymysql.connect(
    host='호스트',
    user='유저',
    password='패스워드',
    db='디비',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)

def check_user_authentication(user_id, user_pw):
    with db.cursor() as cursor:
        sql = "SELECT * FROM member WHERE user_id=%s AND user_pw=%s"
        cursor.execute(sql, (user_id, user_pw))
        result = cursor.fetchone()

    if result:
        return True  # 인증 성공
    else:
        return False  # 인증 실패


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/join/', methods=['GET','POST'])
def join():
    if request.method == 'GET':
        return render_template('join.html')
    elif request.method == 'POST':
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        user_name = request.form['user_name']
        email = request.form['email']

        # 현재 시간을 등록일시로 설정
        reg_date = datetime.now()

        try:
            # 데이터베이스 연결 상태 확인
            if not db.open:
                db.connect()

            # 데이터베이스에 데이터 삽입
            with db.cursor() as cursor:
                sql = "INSERT INTO `member` (user_id, user_pw, user_name, email, reg_date) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (user_id, user_pw, user_name, email, reg_date))
                db.commit()

            return redirect('/')

        except Exception as e:
            return str(e)

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']

        # 데이터베이스 연결 상태 확인
        if not db.open:
            db.connect()

        # DB에서 사용자 인증 확인 로직
        if check_user_authentication(user_id, user_pw):
            session['logged_in'] = True  # 로그인 성공 시 세션에 로그인 상태 저장
            return redirect('/')
        else:
            session['logged_in'] = False  # 로그인 실패 시 세션에 로그인 상태 저장
            return render_template('login.html')

    return render_template('login.html', logged_in=session.get('logged_in', False))

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)  # 세션에서 로그인 상태 제거
    return redirect('/')

if __name__ == '__main__':
    app.run()