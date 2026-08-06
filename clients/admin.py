from django.contrib import admin

from .models import ClientSite


@admin.register(ClientSite)
class ClientSiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']