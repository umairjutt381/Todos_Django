from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['task_name', 'user', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['task_name', 'user__username']
    readonly_fields = ['created_at']
