# -*- coding:utf8 -*-

import MySQLdb
import time
import logging

from datetime import datetime
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log.txt',
                    filemode='a')


def query(host, port, user, password, db):
    conn = MySQLdb.connect(host=host, port=port, user=user, passwd=password, db=db)
    cr = conn.cursor()
    cr.execute('select * from score')
    conn.commit()
    res = cr.fetchall()
    print res
    with open(r'rs.txt', 'a') as f:
        f.write(str(res) + '\n')


if __name__ == '__main__':
    url = 'mysql://root:123456@localhost:3306/work'

    jobstores = {
        'default': SQLAlchemyJobStore(url=url)
    }
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)
    # scheduler.add_jobstore('sqlalchemy', url=url)

    start = datetime.strptime('2017-07-22 11:32:00', '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime('2017-07-22 11:34:00', '%Y-%m-%d %H:%M:%S')
    scheduler.add_job(func=query, args=('127.0.0.1', 3306, 'root', '123456', 'test'),
                      trigger='cron', start_date=start, end_date=end, second='*/5', id='query')

    try:
        scheduler.start()
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()