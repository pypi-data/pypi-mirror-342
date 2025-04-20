from django.contrib import admin

from .models import BackupCode, TOTPDevice, TrustedDevice


class TOTPDeviceAdmin(admin.ModelAdmin):
    list_display = ("user", "confirmed", "secret_key", "digits", "algorithm")
    search_fields = ["user__username"]


class BackupCodeAdmin(admin.ModelAdmin):
    list_display = ("device__user__username", "code", "used")
    search_fields = ["device__user__username", "code"]


class TrustedDeviceAdmin(admin.ModelAdmin):
    list_display = ("device__user__username", "device_identifier", "expires_at")
    search_fields = ["device__user__username", "device_identifier"]



TOTPDevice._meta.verbose_name = "Admin 2FA Device"
TOTPDevice._meta.verbose_name_plural = "Admin 2FA Devices"


BackupCode._meta.verbose_name = "Admin Backup Code"
BackupCode._meta.verbose_name_plural = "Admin Backup Codes"

TrustedDevice._meta.verbose_name = "Admin Trusted Device"
TrustedDevice._meta.verbose_name_plural = "Admin Trusted Devices"

admin.site.register(TOTPDevice, TOTPDeviceAdmin)
admin.site.register(BackupCode, BackupCodeAdmin)
admin.site.register(TrustedDevice, TrustedDeviceAdmin)
