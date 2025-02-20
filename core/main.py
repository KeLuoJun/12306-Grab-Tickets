# 主函数，实现定时运行购票程序，并发送邮件提醒
import sys
import os

# 添加项目根目录到 sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config.settings import TIME
from core.by import Byticket
from utils.sendemail import mail
from apscheduler.schedulers.blocking import BlockingScheduler

by = Byticket()

def job_callback(sched):
    try:
        result = by.start()
        if result:
            mail("12306抢票成功", "车票已成功抢到，请尽快支付！")
        else:
            mail("购票失败", "未能成功抢到车票，请检查日志或稍后再试。")
        
        # 关闭调度器并确保其完全关闭
        sched.shutdown(wait=True)
        print("调度器已关闭")

        # 显式退出程序
        sys.exit(0)

    except Exception as e:
        sched.shutdown(wait=True)
        sys.exit(1)

def main():
    by.login()
    sched = BlockingScheduler(timezone='Asia/Shanghai')
    sched.add_job(
        job_callback,
        'date',
        run_date=TIME,
        args=[sched]
    )
    sched.start()


if __name__ == '__main__':
    main()
