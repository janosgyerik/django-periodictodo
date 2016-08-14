from itertools import groupby
from datetime import datetime

from collections import namedtuple
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

    records = impl.TaskRecord.objects \
        .filter(user=user, task__period=period, created_at__gte=start, created_at__lte=date)

    stats = []
    for key, group in groupby(records, lambda x: x.task.pk):
        records = list(group)
        task = records[0].task
        percentage = len(records) / task.count
        stats.append(Stat(task, percentage))
    return stats
