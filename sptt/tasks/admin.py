from django.contrib import admin
from tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'period', 'name', 'count')
    list_display_links = ('name',)


admin.site.register(Task, TaskAdmin)
