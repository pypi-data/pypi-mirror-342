from django.contrib import admin
from django.urls import path
from .models import PipFreezeSnapshot, RequirementsCheck
from .views import pip_manager_view, reqcheck_view



@admin.register(PipFreezeSnapshot)
class PipFreezeSnapshotAdmin(admin.ModelAdmin):
    list_display = ("created", "note")
    ordering = ("-created",)
    readonly_fields = ("created", "raw_data")

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path("", self.admin_site.admin_view(pip_manager_view), name="pupdater_freeze"),
        ]
        return custom + urls

    def changelist_view(self, request, extra_context=None):
        return pip_manager_view(request)

@admin.register(RequirementsCheck)
class RequirementsCheckAdmin(admin.ModelAdmin):
    list_display = ("id", "note")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("", self.admin_site.admin_view(reqcheck_view), name="pupdater_requirements"),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        return reqcheck_view(request)

