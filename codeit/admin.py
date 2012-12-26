from codeit.models import *
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'receipt_no',
        'first_name',
        'last_name',
        'total_points'
        )
    list_filter = (
        'total_points',
        )
    search_field = ('receipt_no',
        'first_name',
        'last_name'
        )
    ordering = (
        'total_points',
        )


admin.site.register(User, UserAdmin)
admin.site.register(Problem)
admin.site.register(Solution)


"""
class PostAdmin(admin.ModelAdmin):
    list_display = ['post_name', 'pub_date', 'was_published_recently']
    list_filter = ['pub_date']
    search_field = ['post_name']
    date_hierarchy = 'pub_date'
    fieldsets = [
    (None, {'fields':['post_name']}),
    ('Date information', {'fields':['pub_date'], 'classes':['collapse']}),
    ('Post Text', {'fields': ['post_text']}),
    ]

admin.site.register(Post, PostAdmin)
"""
