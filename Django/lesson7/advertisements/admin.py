from django.contrib import admin
from .models import Advertisement
# Register your models here.


@admin.register(Advertisement)
class AdvertismentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'status', 'creator', 'created_at', 'updated_at']