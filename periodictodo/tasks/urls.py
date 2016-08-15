from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list$', views.task_list, name='task_list'),
    url(r'^actions/mark-done/(?P<task_id>\d+)$', views.mark_done, name='mark_done'),
]
