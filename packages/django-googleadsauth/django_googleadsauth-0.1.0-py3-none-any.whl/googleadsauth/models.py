from django.db import models


class Token(models.Model):
    """
    Stores the OAuth token for Google Ads API.
    Only one token is stored at a time - when a new token is saved,
    all existing tokens are deleted.
    """

    token = models.CharField(
        max_length=255, help_text="Google Ads API OAuth refresh token"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When the token was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="When the token was last updated"
    )

    def save(self, *args, **kwargs):
        # Delete all existing entries before saving a new one
        Token.objects.all().delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Token created at {self.created_at}"

    class Meta:
        verbose_name = "Google Ads Token"
        verbose_name_plural = "Google Ads Tokens"


class CampaignStatus(models.Model):
    """
    Stores the status of Google Ads campaigns.
    Used to track which campaigns are enabled or disabled.
    """

    ENABLED = 2
    PAUSED = 3
    REMOVED = 4

    STATUS_CHOICES = (
        (ENABLED, "Enabled"),
        (PAUSED, "Paused"),
        (REMOVED, "Removed"),
    )

    campaign_id = models.CharField(
        max_length=255, unique=True, help_text="Google Ads campaign ID"
    )
    customer_id = models.CharField(
        max_length=255, help_text="Google Ads customer ID", blank=True, null=True
    )
    campaign_name = models.CharField(
        max_length=255, help_text="Campaign name", blank=True, null=True
    )
    status = models.IntegerField(choices=STATUS_CHOICES, help_text="Campaign status")

    def __str__(self):
        status_display = self.get_status_display()
        if self.campaign_name:
            return f"{self.campaign_name} ({self.campaign_id}) - {status_display}"
        return f"Campaign {self.campaign_id} - {status_display}"

    class Meta:
        verbose_name = "Campaign Status"
        verbose_name_plural = "Campaign Statuses"
