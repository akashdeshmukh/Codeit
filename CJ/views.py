from django.shortcuts import render_to_response
from django.template import RequestContext
# importing render_to_response method


# 403.html
def my_custom_permission_denied_view(request):
    return render_to_response("error/403.html",
        {},
        context_instance=RequestContext(request),
        )


# 404.html
def my_custom_404_view(request):
    return render_to_response("error/404.html",
        {},
        context_instance=RequestContext(request),
        )


# 500.html
def my_custom_error_view(request):
    return render_to_response("error/500.html",
        {},
        context_instance=RequestContext(request),
        )
