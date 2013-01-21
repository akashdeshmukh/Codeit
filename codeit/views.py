from django.shortcuts import render_to_response, redirect
from django.views.decorators.cache import cache_control
from django.core.files.storage import default_storage
from codeit.forms import UserForm, FileUploadForm
from django.template import RequestContext
from django.conf import settings
from codeit.models import *
from codeit.execute import *
from django.utils import timezone
import os
from django.core import serializers
from django.http import HttpResponse


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
                path = "/".join([settings.MEDIA_ROOT, "documents", str(u.receipt_no) + "/"])
                if not os.path.exists(path):
                    os.makedirs(path)
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
@login_required
def home(request):
    """
    """
    user = getuser(request.session["receipt_no"])
    username = user.fullname()
    if user.year == "fe" or user.year == "se":
        problems = Problem.objects.filter(year__lt=4).order_by("year")
    else:
        problems = Problem.objects.filter(year__gt=3).order_by("year")
    return render_to_response("codeit/home.html",
        {"username": username,
        "problems": problems},
        context_instance=RequestContext(request))


def questions(request, ptype):
    """
    Chaged url in urls.py for passing type.
    We pass type here and get Problems for that type
    Now just testing for 1,2,3.
    Eg. url will be http://127.0.0.1:8000/questions/1/"
    Will return json objets
    """
    content_type = "application/json"
    format = "json"
    user = getuser(request.session["receipt_no"])
    if user.year == "fe" or user.year == "se":
        pass
    else:
        if ptype == "1":
            ptype = "4"
        elif ptype == "2":
            ptype = "5"
        elif ptype == "3":
            ptype = "6"

    if ptype == "1":
        problems = Problem.objects.filter(year__exact=1)
    elif ptype == "2":
        problems = Problem.objects.filter(year__exact=2)
    elif ptype == "3":
        problems = Problem.objects.filter(year__exact=3)
    elif ptype == "4":
        problems = Problem.objects.filter(year__exact=4)
    elif ptype == "5":
        problems = Problem.objects.filter(year__exact=5)
    elif ptype == "6":
        problems = Problem.objects.filter(year__exact=6)
    else:
        return -1

    # Return json data
    data = serializers.serialize(format, problems)
    return HttpResponse(data, mimetype=content_type)


@login_required
def logout(request):
    """
    """
    # Check if request contains session var "username"
    user = getuser(request.session["receipt_no"])
    user.isactive = False
    user.save()
    del request.session["receipt_no"]
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
    username = getuser(request.session["receipt_no"]).fullname()
    userlist = User.objects.exclude(first_name="-").order_by("-total_points")
    return render_to_response("codeit/ranking.html",
        {"userlist": userlist,
        "username": username,
        },
        context_instance=RequestContext(request)
        )


@login_required
def problem(request, problem_id):
    username = getuser(request.session["receipt_no"]).fullname()
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
        "username": username,
        },
        context_instance=RequestContext(request)
        )


@login_required
def solution(request, problem_id):
    if 'lastsubtime' in request.session:
        diff = timezone.now() - request.session['lastsubtime']
        # Time For execution is temp. 30 should be changed to 120 sec.
        limit = 5
        if diff.seconds < limit:
            message = """
            You have submitted solution recently.
            Submit solution again after ..."""
            diff = str(limit - diff.seconds) + " seconds"
            return render_to_response("error/error.html",
                {'message': message,
                'diff': diff,
                },
                context_instance=RequestContext(request)
                )
        else:
            request.session['lastsubtime'] = timezone.now()
    else:
        request.session['lastsubtime'] = timezone.now()

    user = getuser(request.session["receipt_no"])
    if user:
        username = user.fullname()
    else:
        message = """
        You are using wrong receipt_no
        Contact server adminstrator
        """
        return render_to_response('error/error',
            {'message': message,
            },
            context_instance=RequestContext(request)
            )

    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            language = form.cleaned_data.get("picked")
            if user:
                try:
                    problem = Problem.objects.get(pk=problem_id)
                except KeyError:
                    message = "Problem not found with given problem id"
                    return render_to_response("error/error.html",
                        {"message": message,
                        })
                if problem in user.solved.all():
                    return HttpResponse("Alread solved this problem")
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
                    points_obtained=0
                    )
                sol.save()
                content = default_storage.open(sol.text).read()
                result = str(final_ex(sol, problem))
                print result
                if result.startswith("AC"):
                    sol.points_obtained = problem.points
                    sol.save()
                    user.total_points = user.total_points + problem.points
                    user.solved.add(problem)
                    user.save()
                return render_to_response("codeit/solution.html",
                    {"content": content,
                     "result": result,
                     "username": username,
                    },
                    context_instance=RequestContext(request)
                    )
            else:
                message = "User not found for solution submission"
                return render_to_response("error/error.html",
                    {"message": message,
                    })
        else:
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
                if problem in user.solved.all():
                    return HttpResponse("already solved this problem")
                path = "/".join([settings.MEDIA_ROOT, "documents", str(user.receipt_no), problem.name + "." + language])
                path = path.replace(" ", "")
                temp = open(path, "w+")
                temp.write(content)
                temp.close()
                sol = Solution()
                sol.text.name = path
                sol.problem = problem
                sol.user = user
                sol.language = language
                sol.points_obtained = 0
                sol.save()
                content = default_storage.open(sol.text).read()
                result = str(final_ex(sol, problem))
                print result
                if result.startswith("AC"):
                    sol.points_obtained = problem.points
                    sol.save()
                    user.total_points = user.total_points + problem.points
                    user.solved.add(problem)
                    user.save()
                return render_to_response("codeit/solution.html",
                    {"content": content,
                    "result": result,
                    "username": username,
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
    if "receipt_no" in request.session:
        username = getuser(request.session["receipt_no"]).fullname()
        return render_to_response("codeit/contact.html",
            {"username": username,
            },
            context_instance=RequestContext(request)
            )
    return render_to_response("codeit/contact.html",
        {},
        context_instance=RequestContext(request)
        )


def about(request):
    if "receipt_no" in request.session:
        username = getuser(request.session["receipt_no"]).fullname()
        return render_to_response("codeit/about.html",
            {"username": username,
            },
            context_instance=RequestContext(request)
            )
    return render_to_response("codeit/about.html",
        {},
        context_instance=RequestContext(request)
        )


def demo(request):
    return render_to_response("codeit/demo.html",
        {},
        context_instance=RequestContext(request),
        )


@login_required
def submission(request, receipt_no):
    username = getuser(request.session["receipt_no"]).fullname()
    solver = getuser(receipt_no).fullname()
    solutions = Solution.objects.filter(user__receipt_no__exact=receipt_no)
    return render_to_response('codeit/submission.html',
        {"solutions": solutions,
        "username": username,
        "solver": solver,
        },
        context_instance=RequestContext(request)
        )
