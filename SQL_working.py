import pandas as pd
import pymysql
import openpyxl
import datetime
import traceback
from pymysql.err import IntegrityError # pymysql 에러메세지 출력작업


def get_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='infac@1234',
        db='phishing_data',
        charset='utf8mb4',
        autocommit=False  # 수동 커밋
    )

table_name = "phishing_log"

def save_SQL_execl():
    """
        DB 데이터를 엑셀 파일로 가져옵니다.
    """
    try :
        with get_connection() as conn:
            print("DB 데이터 가져오는 중...")
            dt = datetime.datetime.now()
            query = (f"SELECT * FROM {table_name}")
            df = pd.read_sql(query, conn)
            timestamp = dt.strftime("%Y%m%d_%H%M%S")
            df.to_excel(f"./SQL_backup/SQL_output_{timestamp}.xlsx", index=False)
            print(f"\n✅ SQL_output_{timestamp} 저장 완료")

    except IntegrityError as e:
        print(f"\n⚠️ DB 오류: {e}")
    except Exception as e:
        print(f"\n❌ 알 수 없는 오류 발생: {e}")

def upload_execl_SQL():
    """
        엑셀 파일에 작성되어 있는 내용을 DB에 업로드합니다.
    """
    try :

        print("엑셀 읽어오는 중...")
        df = pd.read_excel("mail_list.xlsx", usecols=[0, 1])  # A열, B열, 2행부터 읽어옴
        df.columns = ['name', 'email']  # 컬럼명 지정

        print("엑셀 데이터 DB 업로드 중...")
        insert_sql = "INSERT INTO phishing_log (Name, Email) VALUES (%s, %s)"

        with get_connection() as conn :
            with conn.cursor() as cursor :
                for row in df.itertuples(index=False):
                    cursor.execute(insert_sql, (row.name, row.email))
                conn.commit()

        print("\n✅ 데이터 업로드 완료")

    except IntegrityError as e:
        print(f"\n⚠️ DB 오류: {e}")
    except Exception as e:
        print(f"\n❌ 알 수 없는 오류 발생: {e}")

def delete_SQL():
    """
        mysql에 작성되어 있는 모든 데이터를 백업 후 삭제합니다.
    """
    try :

        print("\nDB 백업 중...")
        save_SQL_execl()
        print("\nDB 삭제 중...")

        with get_connection() as conn :
            with conn.cursor() as cursor :
                cursor.execute("SET FOREIGN_KEY_CHECKS=0")
                cursor.execute(f"TRUNCATE TABLE {table_name}")
                cursor.execute("SET FOREIGN_KEY_CHECKS=1")
            conn.commit()

        print("\n✅ DB 삭제 완료")

    except IntegrityError as e:
        print(f"\n⚠️ DB 오류: {e}")
    except Exception as e:
        print(f"\n❌ 알 수 없는 오류 발생: {e}")

if __name__=='__main__':

    while True :
        process_num = ""

        print("\n1. 엑셀 데이터 DB 업로드")
        print("2. DB 데이터 엑셀로 가져오기")
        print("3. DB 데이터 삭제")
        print("4. 종료")
        process_num = input("\n실행할 작업을 선택하십시오 : ")

        if process_num == '1' :
            upload_execl_SQL()
        elif process_num == '2' :
            save_SQL_execl()
        elif process_num == '3' :
            delete_SQL()
        elif process_num == '4' :
            break
        else :
            print("\n번호를 다시 입력하세요.")

    print("종료합니다.")