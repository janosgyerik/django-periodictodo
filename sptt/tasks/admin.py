from django.contrib import admin
from tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'period', 'name', 'count')


admin.site.register(Task, TaskAdmin)
