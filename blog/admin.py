from blog.models import Post
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

admin.site.register(Post, PostAdmin)
