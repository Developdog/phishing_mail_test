import datetime
import base64
import pymysql
from flask import Flask, request, send_file, render_template
from flask import Blueprint, send_from_directory

routesBp = Blueprint('routes', __name__)

# @routesBp.route('/.well-known/acme-challenge/<path:filename>')
# def serve_acme_challenge(filename):
#     return send_from_directory('static/.well-known/acme-challenge', filename)

#--------------------------- sql 

def get_connection():
    return pymysql.connect(
        host='127.0.0.1', user='root', password='infac@1234',
        db='phishing_data', charset='utf8mb4', autocommit=True
    )

#---------------------------

app = Flask(__name__)
app.register_blueprint(routesBp)

@app.route('/')
def index():
    return 'Phishing Simulation Server is running.'

# 메일 열람 시 테스트용 이미지
@app.route('/Mail_open') # 디코드 필요요
def mail_tracker():
    try:
        encoded_text = request.args.get("user_email")
        decoded_bytes = base64.b64decode(encoded_text)
        user_email = decoded_bytes.decode('utf-8')
    except Exception as e:
        print("❌ base64 디코딩 실패:", e)

    now = datetime.datetime.now()
    print(f"[{now}] [Mail_OPEN] TRACKED - user_email : {user_email}")

    with get_connection() as conn :
        with conn.cursor() as cursor :
            cursor.execute("""
            UPDATE phishing_log 
            SET open_mail_date = NOW() 
            WHERE Email = %s;
            """, (user_email,))
            conn.commit()

    # and open_login_date IS NULL

    # 실제 PNG 이미지로 응답
    return send_file("tracker.png", mimetype="image/png")

# 피싱 사이트 클릭 시
@app.route('/Site_open') # 디코드 필요
def site_open():
    try:
        encoded_text = request.args.get("user_email")
        decoded_bytes = base64.b64decode(encoded_text)
        user_email = decoded_bytes.decode('utf-8')
    except Exception as e:
        print("❌ base64 디코딩 실패:", e)
    now = datetime.datetime.now()
   
    print(f"[{now}] [Site_OPEN] TRACKED - user_email : {user_email}")

    with get_connection() as conn :
        with conn.cursor() as cursor :
            cursor.execute("""
            UPDATE phishing_log
            SET open_login_date = NOW()
            WHERE Email = %s;
            """, (user_email,))
            conn.commit()

    return render_template('login_page.html', user_email = user_email)

# 피싱 사이트 정보 입력 후 파일 다운로드 창
@app.route('/Login_Finish', methods=['POST']) # 디코드 불필요
def site_login():
    user_email = request.form.get("user_email")
    groupware_id = request.form.get('groupware_id')
    groupware_pw = request.form.get('groupware_pw')
    now = datetime.datetime.now()

    print(f"[{now}] [Site_LOGIN] TRACKED - user_email : {user_email} groupware_id : {groupware_id} groupware_pw : {groupware_pw}")

    with get_connection() as conn :
        with conn.cursor() as cursor :
            cursor.execute("""
            UPDATE phishing_log
            SET login_date = NOW(), login_ID = %s, login_PW = %s
            WHERE Email = %s and login_date IS NULL
            """, (groupware_id, groupware_pw, user_email,))
            conn.commit()

    return render_template('download_page.html', user_email = user_email,
    groupware_id = groupware_id, groupware_pw = groupware_pw)


@app.route('/Download_Click', methods=['POST']) # 디코드 불필요
def update_login():
    user_email = request.form.get("user_email")
    now = datetime.datetime.now()

    print(f"[{now}] [Download_Click] TRACKED - user_email : {user_email}")

    with get_connection() as conn :
        with conn.cursor() as cursor :
            cursor.execute("""
                UPDATE phishing_log
                SET download_date = NOW()
                WHERE Email = %s and download_date IS NULL
            """, (user_email,))
            conn.commit()

    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)