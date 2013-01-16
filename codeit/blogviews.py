from codeit.models import *
from codeit.execute import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


@login_required
def blogindex(request):
    username = getuser(request.session["receipt_no"]).fullname()
    latest_post_list = Post.objects.all().order_by("-pub_date")[:5]
    return render_to_response("codeit/blogindex.html",
        {"latest_post_list": latest_post_list,
        "username": username,
        },
        context_instance=RequestContext(request))


@login_required
def blogdetail(request, post_id):
    username = getuser(request.session["receipt_no"]).fullname()
    p = get_object_or_404(Post, pk=post_id)
    return render_to_response("codeit/blogdetail.html",
        {"post": p,
        "username": username,
        },
        context_instance=RequestContext(request))


# 403.html
def my_custom_permission_denied_view(request):
    return render_to_response("error/403.html",
        {},
        context_instance=RequestContext(request)
        )


# 404.html
def my_custom_404_view(request):
    return render_to_response("error/404.html",
        {},
        context_instance=RequestContext(request)
        )


# 500.html
def my_custom_error_view(request):
    return render_to_response("error/500.html",
        {},
        context_instance=RequestContext(request)
        )