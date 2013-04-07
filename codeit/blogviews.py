from codeit.models import *
from codeit.execute import *
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from codeit.forms import FeedbackForm


@login_required
def blogindex(request):
    username = getuser(request.session["receipt_no"]).fullname()
    latest_post_list = Post.objects.all().order_by("-pub_date")[:5]
    return render_to_response("codeit/blogindex.html",
        {"latest_post_list": latest_post_list,
        "username": username,
        },
        context_instance=RequestContext(request)
    )


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


@login_required
def feedback(request):
    if request.method == "POST":
        fd = FeedbackForm(request.POST)
        if fd.is_valid():
            resp = Feedback()
            resp.name = getuser(request.session["receipt_no"])
            resp.fdproblems = fd.cleaned_data["fdproblem"]
            resp.fdsoft = fd.cleaned_data["fdsoft"]
            resp.fdsugg = fd.cleaned_data["fdsugg"]
            resp.save()
            return redirect("/home/")
        else:
            msg = "Please fill all fields."
            return render_to_response("codeit/feedback.html",
            {"fd": fd,
              "msg": msg,
            },
            context_instance=RequestContext(request)
            )

    else:
        return render_to_response("codeit/feedback.html",
            {"fd": FeedbackForm(),
            },
            context_instance=RequestContext(request)
            )
