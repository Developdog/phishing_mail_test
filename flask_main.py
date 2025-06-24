import base64, datetime
from flask import Flask, request, send_file, render_template
from celery_tasks import track_mail_open, track_site_open, track_login, track_download

# from log_config import setup_logger

app = Flask(__name__)
# logger = setup_logger('flask')
# app.register_blueprint(routesBp)

@app.route('/')
def index():
    return 'Phishing Simulation Server is running.'

# 메일 열람 시 테스트용 이미지
@app.route('/Mail_open')
def mail_tracker():
    try:
        encoded_text = request.args.get("user_email")
        decoded_bytes = base64.b64decode(encoded_text)
        user_email = decoded_bytes.decode('utf-8')
        # print("Calling track_mail_open with:", user_email)
        track_mail_open.delay(user_email)
    except Exception as e:
        print("❌ base64 디코딩 실패:", e)
    return send_file("tracker.png", mimetype="image/png")

# 피싱 사이트 클릭 시
@app.route('/Site_open')
def site_open():
    try:
        encoded_text = request.args.get("user_email")
        decoded_bytes = base64.b64decode(encoded_text)
        user_email = decoded_bytes.decode('utf-8')
        # print("Calling track_site_open with:", user_email)
        track_site_open.delay(user_email)
    except Exception as e:
        print("❌ base64 디코딩 실패:", e)
        user_email = ""
    return render_template('smartbill_invoice.html', user_email=user_email)

# 피싱 사이트 정보 입력 후 파일 다운로드 창
@app.route('/Login_Finish', methods=['POST'])
def site_login():
    user_email = request.form.get("user_email")
    track_login.delay(user_email)
    return render_template('404_error.html', user_email=user_email)


@app.route('/Download_Click', methods=['POST'])
def update_login():
    user_email = request.form.get("user_email")
    track_download.delay(user_email)
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)