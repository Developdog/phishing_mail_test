import yagmail
import base64
import pymysql
import pandas as pd

def get_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='infac@1234',
        db='phishing_data',
        charset='utf8mb4',
        autocommit=False  # 수동 커밋
    )

# -------------------------- SQL
print("메일 주소 SQL 열람중")

with get_connection() as conn :
    table_name = "phishing_log"
    query = (f"SELECT Email FROM {table_name}")
    df = pd.read_sql(query, conn)
    column_email = df['Email'].tolist()


# wb = xw.Book('mail_list.xlsx')
# sheet = wb.sheets[0]  # 첫 번째 시트 사용

# column_email = sheet.range('B1').expand('down').value
# # combined = list(zip(column_name, column_email)) # 리스트 합쳐서 배열로 변경
# wb.close()

print("메일 주소 SQL 열람 완료")
# --------------------------

# html_template = """
# <!DOCTYPE html>
# <html lang="ko">
# <head>
#   <meta charset="UTF-8">
# </head>
# <body style="font-family: '맑은 고딕', sans-serif; background-color: #ffffff; color: #333; margin: 0; padding: 0;">
#   <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 700px; margin: auto; border: 1px solid #ccc;">
#     <tr>
#       <td style="background-color: #005bac; padding: 10px 20px;">
#         <img src="https://i.imgur.com/33q0wYM.jpegM" alt="국세청 홈택스 로고" style="height: 40px;">
#       </td>
#     </tr>
#     <tr>
#       <td style="background-color: #e7f1f9; padding: 20px; font-size: 20px; font-weight: bold;">
#         국세청 전자[세금]계산서입니다.
#         <div style="margin-top: 10px; font-size: 14px; color: #666;">📧 본 메일은 <span style="color: red;">보안메일</span> 입니다.</div>
#       </td>
#     </tr>
#     <tr>
#       <td style="padding: 20px; font-size: 14px; line-height: 1.7;">
#         본 메일은 국세청 홈택스를 이용하여 전자세금계산서를 발급하고 발송한 메일입니다.
        
#         ▸ <strong>발급일자 : 2025년 05월 23일</strong>
#         *메일 내용을 확인하기 위해서는 <a href="https://checkuser.duckdns.org/Site_open?user_email={user_email}">여기</a>를 클릭하세요

#         <strong>전자(세금)계산서 첨부파일이 열리지 않을 시 조치 방법</strong>
#         1. 첨부파일을 사용자 PC에 저장
#         2. 저장한 첨부파일을 오른쪽 마우스 클릭 후 연결프로그램에서 [Internet Explorer] 선택
#       </td>
#     </tr>
#     <tr>
#       <td style="font-size: 12px; color: #777; text-align: center; padding: 15px; border-top: 1px solid #ccc;">
#         세종특별자치시 국세청로 8-14 국세청(정부세종청사 국세청동) (우편번호 30128)
#         Copyrightⓒ National Tax Service. All rights reserved.
#       </td>
#     </tr>
#   </table>
#   <img src="https://checkuser.duckdns.org/Mail_open?user_email={user_email}"/>
# </body>
# </html>
# """

html_template = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>비밀번호 변경 안내</title>
</head>
<body style="margin:0; padding:0; font-family: 'Arial', sans-serif; background-color: #f4f4f4;">
  <table width="100%" cellpadding="0" cellspacing="0" style="padding: 40px 0;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; padding: 40px; box-shadow: 0 0 10px rgba(0,0,0,0.05);">
          <tr>
            <td style="text-align: center;">
              <h2 style="color: #333;">인팩 비밀번호 변경 요청</h2>
              <p style="color: #555; font-size: 16px;">보안 정책 강화에 따라 비밀번호 변경이 필요합니다.</p>
              <p style="color: #555; font-size: 16px;">아래 버튼을 클릭하여 새 비밀번호를 설정해 주세요.</p>
              <a href="https://checkuser.duckdns.org/Site_open?user_email={user_email}" 
                 style="display: inline-block; margin-top: 20px; padding: 14px 24px; background-color: #00aaff; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">
                비밀번호 변경하기
              </a>
              <p style="color: #999; font-size: 12px; margin-top: 40px;">
                본 메일은 시스템에서 자동 발송되었으며, 회신하지 마십시오.<br>
                문의: helpdesk@daouoffice.com
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
  <img src="https://checkuser.duckdns.org/Mail_open?user_email={user_email}"/>
</body>
</html>
"""

f = open("google_password.txt", "r")
google_password = f.read()
f.close()

yag = yagmail.SMTP( user={"infactesting@gmail.com" : "hometaxadmin@hometax.go.kr"}, password=google_password, host='smtp.gmail.com')

for email_row in column_email :

    # 제목 및 보낼 메일 지정
    print(f"{email_row} 메일 보내는 중")
    to = email_row
    subject = '[안내] 비밀번호 변경 필요'
    
    # 이메일 값 링크 암호화
    byte_text = email_row.encode('utf-8')
    encoded_text = base64.b64encode(byte_text)
    html = html_template.format(user_email=encoded_text.decode('utf-8'))

    # yag.send(to = to, subject = subject, contents = [body, html, img])
    yag.send(to = to, subject = subject, contents = [html])

print("전체 송신 완료")