from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks import api
from tasks import periods


@login_required
def pending_tasks(request):
    daily_list = api.load_progress(request.user, periods.DAILY)
    weekly_list = api.load_progress(request.user, periods.WEEKLY)

    context = {
        'daily_list': daily_list,
        'weekly_list': weekly_list,
    }
    return render(request, 'tasks/pending.html', context)
