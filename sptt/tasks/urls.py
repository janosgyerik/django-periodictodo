from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^pending$', views.pending_tasks, name='pending_tasks'),
]
