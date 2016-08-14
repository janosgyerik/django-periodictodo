from django.contrib import admin
from tasks.models import Task, TaskRecord


class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'period', 'name', 'count')
    list_display_links = ('name',)


class TaskRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'created_at')
    list_display_links = ('created_at',)


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskRecord, TaskRecordAdmin)
