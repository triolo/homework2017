from apscheduler.schedulers.blocking import BlockingScheduler
from main import *
# Start the scheduler
sched = BlockingScheduler()

@sched.scheduled_job('cron', hour="9,12", minute="5")
def job_function():
    main()

sched.start()