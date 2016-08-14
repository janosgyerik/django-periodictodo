from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^pending$', views.pending_tasks, name='pending_tasks'),
    url(r'^actions/mark-done/(?P<task_id>\d+)$', views.mark_done, name='mark_done'),
]
