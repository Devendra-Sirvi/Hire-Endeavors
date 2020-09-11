from django.contrib import admin
from .models import org
# Register your models here.

class panel(admin.ModelAdmin):
    list_display = ['orgname', 'user', 'managed_by']

    
admin.site.register(org, panel)