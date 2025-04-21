from django.contrib import admin
from .models import Token, CampaignStatus


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("token",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(CampaignStatus)
class CampaignStatusAdmin(admin.ModelAdmin):
    list_display = ("campaign_name", "campaign_id", "customer_id", "status_display")
    list_filter = ("status",)
    search_fields = ("campaign_id", "campaign_name", "customer_id")

    def status_display(self, obj):
        return obj.get_status_display()

    status_display.short_description = "Status"
