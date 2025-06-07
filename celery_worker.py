import celery_tasks

celery = celery_tasks.celery

if __name__ == '__main__':
    celery.worker_main()