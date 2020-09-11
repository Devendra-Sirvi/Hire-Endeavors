from django.contrib import admin
from .models import orgjobpost, userjobpost
# Register your models here.

class panel(admin.ModelAdmin):
    list_display = ['Position_Name', 'created_by']


admin.site.register(orgjobpost, panel)
admin.site.register(userjobpost, panel)