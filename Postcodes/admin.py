from django.contrib import admin

from .models import Postcode


@admin.register(Postcode)
class PostcodesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "postcode")
    ordering = ["name"]
