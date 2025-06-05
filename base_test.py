# import base64
# import datetime

# # 원본 문자열
# original_text = "youtaek.oh@infac.com"

# # 문자열 -> 바이트로 인코딩
# byte_text = original_text.encode('utf-8')

# # Base64 인코딩
# encoded_text = base64.b64encode(byte_text)
# print("🔐 인코딩 결과:", encoded_text.decode('utf-8'))

# encoded_text = base64.b64encode(original_text.encode('utf-8'))
# print("🔐 인코딩 결과:", encoded_text)

# # Base64 디코딩
# decoded_bytes = base64.b64decode('eW91dGFlay5vaEBpbmZhYy5jb20=')
# decoded_text = decoded_bytes.decode('utf-8')
# print("🔓 디코딩 결과:", decoded_text)


# print((datetime.datetime.now()).date())

import pandas as pd

# 엑셀 파일에서 A열(0), B열(1)만 읽기
df = pd.read_excel("mail_list.xlsx", usecols=[0, 1])

# 컬럼명 지정 (예: A열 → name, B열 → email)
df.columns = ['name', 'email']

# A열과 B열 값이 모두 존재하는 행만 남기기
df = df.dropna(subset=['name', 'email'])

# 전체 값 출력
print(df.to_string(index=False))