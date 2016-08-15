from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from tasks import api
from tasks import periods
from tasks.models import Task


def add_pending_done(progress_list):
    enriched = []
    for item in progress_list:
        enriched.append({
            'task': item.task,
            'count': item.count,
            'pending': range(item.task.count - item.count),
            'done': range(item.count),
        })
    return enriched


@login_required
def pending_tasks(request):
    daily_list = add_pending_done(api.load_progress(request.user, periods.DAILY))
    weekly_list = add_pending_done(api.load_progress(request.user, periods.WEEKLY))

    context = {
        'daily_list': daily_list,
        'weekly_list': weekly_list,
    }
    return render(request, 'tasks/pending.html', context)


@login_required
def mark_done(request, task_id):
    api.record_task(request.user, Task.objects.get(pk=task_id))
    return redirect('pending_tasks')
