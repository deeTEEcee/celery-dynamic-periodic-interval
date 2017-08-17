from celery import Celery
# from celery.schedules import crontab
from celery.schedules import schedule, schedstate
from celery.utils.time import maybe_timedelta

from database import Schedule

app = Celery(broker='amqp://localhost')

app.conf.task_always_eager = True



class DynamicSchedule(schedule):
    def is_due(self, last_run_at):
        db_run_every = maybe_timedelta(Schedule.get(Schedule.id==1).interval)
        changed = db_run_every != self.run_every
        if changed:
            print 'changed. refreshing'
            self.run_every = db_run_every
            return schedstate(is_due=False, next=self.seconds)
        else:
            print 'doing default'
            return super(DynamicSchedule, self).is_due(last_run_at)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(DynamicSchedule(run_every=5.0), test.s('hello'), name='add every 10')

@app.task
def test(arg):
    print 'test task run with {}'.format(arg)
