# -*- coding:utf8 -*-

from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


def alarm(type):
    print '[%s Alarm] This alarm was scheduled at %s.' % (type, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# 定时执行
def corn_trigger():
    global SCHEDULER
    SCHEDULER.add_job(func=alarm, args=['cron'], trigger='cron', second='*/5', id='corn_job')


# 循环执行
def interval_trigger():
    global SCHEDULER
    SCHEDULER.add_job(func=alarm, args=['interval'], trigger='interval', seconds=5, id='interval_job')


# 一次执行
def date_trigger():
    global SCHEDULER
    SCHEDULER.add_job(func=alarm, args=['date'], trigger='date', run_date=datetime.now(), id='date_job')


SCHEDULER = BlockingScheduler()
if __name__ == '__main__':
    corn_trigger()
    interval_trigger()
    date_trigger()

    try:
        SCHEDULER.start()
    except (KeyboardInterrupt, SystemExit):
        SCHEDULER.shutdown()