from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


def task_one():
    print "I am task one."


def task_two():
    print "I am task two."


def task_three():
    print "I am task three."

sched.add_job(task_one, trigger='interval', seconds=2)
sched.add_job(task_two, trigger='interval', seconds=5)
sched.add_job(task_three, trigger='interval', seconds=10)

def main():
    sched.start()

if __name__ == '__main__':
    main()
