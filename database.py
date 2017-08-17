import peewee

database = peewee.PostgresqlDatabase('celery')

class Schedule(peewee.Model):
    interval = peewee.IntegerField()
    class Meta:
        database = database

print Schedule.get(Schedule.id==1).interval