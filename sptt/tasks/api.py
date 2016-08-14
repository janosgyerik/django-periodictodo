from collections import namedtuple
from datetime import datetime
import tasks.models as impl


Stat = namedtuple('Stat', ['task', 'percentage'])


def record_task(user, task, date=None):
    if not date:
        date = datetime.now()
    impl.TaskRecord.objects.create(user=user, task=task, created_at=date)


def load_stats(user, period, tags=(), date=None):
    if not date:
        date = datetime.now()

    start = period.get_start()

    stats = []
    for rec in impl.TaskRecord.objects.filter(
            user=user, task__period=period, created_at__gte=start, created_at__lte=date):
        stats.append(Stat(rec.task, 1))
    return stats
