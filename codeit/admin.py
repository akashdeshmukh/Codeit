from codeit.models import *
from django.contrib import admin


class PostAdmin(admin.ModelAdmin):
    """
    Class for showing Post in admin interface
    Diff field are registered
    TODO: Document properly.
    """
    list_display = ["post_name", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_field = ["post_name"]
    date_hierarchy = "pub_date"
    fieldsets = [
    (None, {"fields":["post_name"]}),
    ("Date information", {"fields":["pub_date"], "classes":["collapse"]}),
    ("Post Text", {"fields": ["post_text"]}),
    ]


class UserAdmin(admin.ModelAdmin):
    exclude = ("solved",)
    list_display = (
        "receipt_no",
        "first_name",
        "last_name",
        "total_points",
        "user_active"
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


class ProblemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "points",
        )


class SolutionAdmin(admin.ModelAdmin):
    list_display = (
        "problem",
        "user",
        "language",
        "points_obtained",
        )


class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        )

admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Solution, SolutionAdmin)
admin.site.register(Feedback, FeedbackAdmin)
