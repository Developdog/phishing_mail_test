from celery import Celery
from celery.utils.log import get_task_logger  # ✅ Celery 전용 로거
import pymysql
import datetime
from log_config import setup_logger
import logging

logger = get_task_logger(__name__)  # Celery 전용 logger

# 직접 file handler 추가 (한 번만)
if not logger.handlers:
    base_logger = setup_logger('celery_tasks')
    for handler in base_logger.handlers:
        logger.addHandler(handler)


# setup_logger('celery')  # ✅ 전역 설정
# logger = get_task_logger(__name__)  # ✅ Celery가 사용하는 방식

celery = Celery(
    'celery_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery.conf.worker_hijack_root_logger = False

logger.info("=== Celery 로그 설정 테스트 ===")

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
                WHERE Email = %s
            """, (user_email,))
            conn.commit()

@celery.task
def track_site_open(user_email):
    now = datetime.datetime.now()
    logger.info(f"[{now}] [Site_OPEN] Celery - {user_email}")
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE phishing_log 
                SET open_login_date = NOW() 
                WHERE Email = %s
            """, (user_email,))
            conn.commit()

@celery.task
def track_login(user_email, groupware_id, groupware_pw):
    now = datetime.datetime.now()
    logger.info(f"[{now}] [Site_LOGIN] Celery - {user_email}")
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
    logger.info(f"[{now}] [Download_Click] Celery - {user_email}")
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE phishing_log 
                SET download_date = NOW()
                WHERE Email = %s and download_date IS NULL
            """, (user_email,))
            conn.commit()