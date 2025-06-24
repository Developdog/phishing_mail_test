from celery import Celery
from celery.utils.log import get_task_logger
from log_config import setup_logger
import pymysql
import datetime

celery = Celery(
    'celery_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)
celery.conf.worker_hijack_root_logger = False

# ✅ 로거 설정
base_logger = setup_logger('celery_tasks')
logger = get_task_logger(__name__)

# 핸들러 복제
if not logger.handlers:
    for h in base_logger.handlers:
        logger.addHandler(h)

def get_connection():
    return pymysql.connect(
        host='127.0.0.1', user='root', password='infac@1234',
        db='phishing_data', charset='utf8mb4', autocommit=True
    )

@celery.task
def track_mail_open(user_email):
    now = datetime.datetime.now()
    logger.info(f"[{now}] [Mail_OPEN] Celery - {user_email}")
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE phishing_log 
                SET open_mail_date = NOW() 
                WHERE Email = %s and open_mail_date IS NULL
            """, (user_email,))
            conn.commit()

@celery.task
def track_site_open(user_email):
    now = datetime.datetime.now()
    logger.info(f"[{now}] [Active1_OPEN] Celery - {user_email}")
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE phishing_log 
                SET open_login_date = NOW() 
                WHERE Email = %s and open_login_date IS NULL
            """, (user_email,))
            conn.commit()

@celery.task
def track_login(user_email, groupware_id, groupware_pw):
    now = datetime.datetime.now()
    logger.info(f"[{now}] [Active2_LOGIN] Celery - {user_email}")
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE phishing_log 
                SET login_date = NOW(), login_ID = %s, login_PW = %s
                WHERE Email = %s and login_date IS NULL
            """, (groupware_id, groupware_pw, user_email))
            conn.commit()

@celery.task
def track_download(user_email):
    now = datetime.datetime.now()
    logger.info(f"[{now}] [Active3_Click] Celery - {user_email}")
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE phishing_log 
                SET download_date = NOW()
                WHERE Email = %s and download_date IS NULL
            """, (user_email,))
            conn.commit()