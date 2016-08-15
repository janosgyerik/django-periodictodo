from itertools import groupby
from datetime import datetime

from collections import namedtuple
import tasks.models as impl

Progress = namedtuple('Progress', ['task', 'count'])


def record_task(user, task, date=None):
    if not date:
        date = datetime.now()
    impl.TaskRecord.objects.create(user=user, task=task, created_at=date)


def load_progress(user, period, tags=(), date=None):
    if not date:
        date = datetime.now()

    tasks = impl.Task.objects.filter(user=user, period=period.name).order_by('pk')

    start = period.get_start()

    records = impl.TaskRecord.objects \
        .filter(user=user, task__period=period.name, created_at__gte=start, created_at__lte=date) \
        .order_by('task')

    counts = dict([(task.id, 0) for task in tasks])
    for key, group in groupby(records, lambda x: x.task.pk):
        records = list(group)
        task_id = records[0].task.id
        counts[task_id] = len(records)
    return [Progress(task, counts[task.id]) for task in tasks]
