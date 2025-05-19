user_id = "youtaek.oh"

html_contents = f"""
<html>
  <body>
    <h2 style="color:blue;">안녕하세요!</h2>
    <p>이것은 <b>HTML 형식</b>의 메일 본문입니다.</p>
    <p>링크: <a href="https://checkuser.duckdns.org/Site_open?user_id={user_id}">여기를 클릭하세요</a></p>
<img src="https://checkuser.duckdns.org/Mail_open?user_id={user_id}"/><br>
"""


f = open("google_password.txt", "r")
google_password = f.read()
f.close()

import yagmail
yag = yagmail.SMTP( user={"infactesting@gmail.com" : "hometaxadmin@hometax.go.kr"}, password=google_password, host='smtp.gmail.com')

to = f'{user_id}@infac.com'
subject = '국세청에서 전자발행문서[세금납부]가 도착하였습니다.'
html = html_contents
# img = 'djangoimg.png'

# yag.send(to = to, subject = subject, contents = [body, html, img])
yag.send(to = to, subject = subject, contents = [html])