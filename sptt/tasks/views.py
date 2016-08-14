from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tasks import api
from tasks import periods


@login_required
def pending_tasks(request):
    daily_list = api.load_progress(request.user, periods.DAILY)
    context = {
        'daily_list': daily_list,
    }
    return render(request, 'tasks/pending.html', context)
