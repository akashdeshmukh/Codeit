from codeit.models import *
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "receipt_no",
        "first_name",
        "last_name",
        "total_points"
        )
    list_filter = (
        "total_points",
        )
    search_field = ("receipt_no",
        "first_name",
        "last_name"
        )
    ordering = (
        "receipt_no",
        )


admin.site.register(User, UserAdmin)
admin.site.register(Problem)
admin.site.register(Solution)
