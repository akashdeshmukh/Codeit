from codeit.forms import UserForm, FileUploadForm
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from codeit.models import *
from django.views.decorators.cache import cache_control
from django.core.files.storage import default_storage
from django.conf import settings
from codeit.models import Post


def blogindex(request):
    latest_post_list = Post.objects.all().order_by("-pub_date")[:5]
    return render_to_response("codeit/blogindex.html",
        {"latest_post_list": latest_post_list},
        context_instance=RequestContext(request))


def blogdetail(request, post_id):
    p = get_object_or_404(Post, pk=post_id)
    return render_to_response("codeit/blogdetail.html",
        {"post": p},
        context_instance=RequestContext(request))


def getuser(receipt_no):
    """
    @receipt_no : Receipt no to be searched
    Get user from receipt_no
    Just search receipt_no as its primary key.
    """
    receipt_no = str(receipt_no)
    try:
        # Get user with exact receipt no
        user = User.objects.get(receipt_no__exact=receipt_no)
        if user:
            return user
        else:
            print "getuser function=>User not found line no. 23"
            return 0
    except KeyError:
        print "Error"
        return 0


def login_required(function):
    """
    @function : function passed for validation
    Decorator checks before function execution
    if user have session or not.
    """
    def wrapped(*args, **kw):
        request = args[0]
        if "receipt_no" in request.session:
            return function(*args, **kw)
        else:
            return redirect("/")
    return wrapped


def index(request):
    """
    This function validates user login ,
    manages whole user information.
    """
    #Check if user already started session
    if "receipt_no" in request.session:
        return redirect("/home/")

    # If user posting data
    if request.method == "POST":
        form = UserForm(request.POST)
        #Check form field is valid or not
        if form.is_valid():
            #Extract data from form
            receipt_no = form.cleaned_data["receipt_no"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            try:
                year = request.POST["year"]
            except:
                return render_to_response("error/error.html",
                    {"message": message,
                    })
            first_name = first_name.capitalize()
            last_name = last_name.capitalize()

            #Get all objects with that receipt no.
            temp = User.objects.filter(receipt_no=int(receipt_no))
            # Receipt no not found.
            if temp.count() == 0:
                message = """
                    You dont have right receipt no.
                    Contact server adminstrator.
                    Back To Login
                    """
                return render_to_response("error/error.html",
                    {"message": message,
                    },
                    context_instance=RequestContext(request),
                    )
            # Receipt no duplcated.
            elif temp.count() > 1:
                # This is never going to happen :-( Still
                message = """
                     Your receipt no is duplicated.<br>
                    Contact server adminstrator.
                    """
                return render_to_response("error/error.html",
                    {"message": message,
                    },
                    context_instance=RequestContext(request),
                    )
            #Set first_name, last_name for user
            u = temp[0]
            if u.isactive == False:
                u.first_name = first_name
                u.last_name = last_name
                u.year = year
                u.isactive = True
                u.save()
                request.session["receipt_no"] = u.receipt_no
                return redirect("/home/")
            else:
                return redirect("/")
        else:
            return render_to_response("codeit/index.html",
             {"userform": form},
             context_instance=RequestContext(request))
    else:
        userform = UserForm()
        return render_to_response("codeit/index.html",
            {"userform": userform},
            context_instance=RequestContext(request)
            )


@cache_control(no_cache=True,
    must_revalidate=True,
    no_store=True,
    )
def home(request):
    """
    """
    if "receipt_no" in request.session:
        receipt_no = request.session["receipt_no"]
        user = getuser(receipt_no)
        username = user.fullname()
        if user.year == "fe" or user.year == "se":
            problems = Problem.objects.filter(year__lt=4).order_by("year")
        else:
            problems = Problem.objects.filter(year__gt=3).order_by("year")
        return render_to_response("codeit/home.html",
            {"username": username,
            "problems": problems},
            context_instance=RequestContext(request))
    else:
        return redirect("/")


@login_required
def logout(request):
    """
    """
    # Check if request contains session var "username"
    if "receipt_no" in request.session:
        receipt_no = request.session["receipt_no"]
        user = getuser(receipt_no)
        user.isactive = False
        user.save()
        del request.session["receipt_no"]
    # Return Wrong If session
    else:
        message = """
            <p> You have already logged out.</p>
            <p> Wrong call</p>
            """
        return render_to_response("error/error.html",
            {"message": message,
            })
    return redirect("/")


@cache_control(no_cache=True,
    must_revalidate=True,
    no_store=True,
)
@login_required
def ranking(request):
    """
    Decide ranking of users from points
    """
    if "receipt_no" in request.session:
        receipt_no = request.session["receipt_no"]
        user = getuser(receipt_no)
        username = user.fullname()
        userlist = User.objects.exclude(first_name="-").order_by("total_points").reverse()
        return render_to_response("codeit/ranking.html",
            {"userlist": userlist,
            "username": username,
            },
            context_instance=RequestContext(request)
            )
    else:
        userlist = User.objects.filter().order_by("total_points").reverse()
        return render_to_response("codeit/ranking.html",
            {"userlist": userlist,
            },
            )


@login_required
def problem(request, problem_id):
    try:
        problem = Problem.objects.get(pk=problem_id)
    except KeyError:
        message = "Problem not found with given problem_id"
        return render_to_response("error/error.html",
            {"message": message,
            })
    return render_to_response("codeit/problem.html",
        {"problem": problem,
        "fileuploadform": FileUploadForm(),
        },
        context_instance=RequestContext(request)
        )


@login_required
def solution(request, problem_id):
    if request.method == "POST":
        receipt_no = request.session["receipt_no"]
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            language = form.cleaned_data.get("picked")
            language = language[0]
            user = getuser(receipt_no)
            if user:
                try:
                    problem = Problem.objects.get(pk=problem_id)
                except KeyError:
                    message = "Problem not found with given problem id"
                    return render_to_response("error/error.html",
                        {"message": message,
                        })
                if "code"in request.FILES:
                        codefile = request.FILES["code"]
                else:
                    message = "Codefile not found in post"
                    return render_to_response("error/error.html",
                        {"message": message,
                        })
                sol = Solution.objects.create(
                    text=codefile,
                    problem=problem,
                    user=user,
                    language=language,
                    points_obtained=problem.points
                    )
                sol.save()
                user.total_points = user.total_points + problem.points
                user.save()
                content = default_storage.open(sol.text).read()
                result = "This is result."
                return render_to_response("codeit/solution.html",
                    {"content": content,
                     "result": result,
                    },
                    context_instance=RequestContext(request)
                    )
            else:
                message = "User not found for solution submission"
                return render_to_response("error/error.html",
                    {"message": message,
                    })
        else:
            user = getuser(receipt_no)
            if user:
                language = request.POST["picked"]
                content = request.POST["soltext"]
                try:
                    problem = Problem.objects.get(pk=problem_id)
                except KeyError:
                    message = "Problem not found with given problem id"
                    return render_to_response("error/error.html",
                        {"message": message,
                        })
                path = "/".join([settings.MEDIA_ROOT, "documents", str(user.receipt_no), problem.name + "." + language])
                temp = open(path, "w+")
                temp.write(content)
                temp.close()
                sol = Solution()
                sol.text.name = path
                sol.problem = problem
                sol.user = user
                sol.language = language
                sol.points_obtained = problem.points
                sol.save()
                user.total_points = user.total_points + problem.points
                user.save()
                content = default_storage.open(sol.text).read()
                result = "This is result."
                return render_to_response("codeit/solution.html",
                    {"content": content,
                    "result": result,
                    },
                    context_instance=RequestContext(request)
                    )
            else:
                message = "File not submitted user not found"
                return render_to_response("error/error.html",
                    {"message": message,
                    })
    return redirect("/problem/" + problem_id)


def contact(request):
    return render_to_response("codeit/contact.html",
        {},
        context_instance=RequestContext(request)
        )


def about(request):
    return render_to_response("codeit/about.html",
        {},
        context_instance=RequestContext(request)
        )


def demo(request):
    return render_to_response("codeit/demo.html",
        {},
        context_instance=RequestContext(request),
        )
