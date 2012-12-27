from codeit.forms import UserForm, FileUploadForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from codeit.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_control
from django.core.files.storage import default_storage


def login_required(function):
    def wrapped(*args, **kw):
        request = args[0]
        if 'username' in request.session:
            return function(*args, **kw)
        else:
            return redirect('/')
    return wrapped


def index(request):
    """
    This function validates user login ,
    manages whole user information.
    """
    #Check if user already started session
    if 'username' in request.session:
        return redirect('/home/')

    # If user posting data
    if request.method == "POST":
        form = UserForm(request.POST)
        #Check form field is valid or not
        if form.is_valid():
            #Extract data from form
            receipt_no = form.cleaned_data['receipt_no']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            first_name = first_name.capitalize()
            last_name = last_name.capitalize()
            year = request.POST['year']
            print year
            #Get all objects with that receipt no.
            temp = User.objects.filter(receipt_no=int(receipt_no))
            # Receipt no not found.
            if temp.count() == 0:
                return HttpResponse("""
                    You dont have right receipt no.<br>Contact server adminstrator.
                    <p><a href="/"><button>Back To Login</button></a></p>
                    """)
            # Receipt no duplcated.
            elif temp.count() > 1:
                return HttpResponse("""
                    Your receipt no is duplicated.<br>
                    Contact server adminstrator.
                    <p><a href="/"><button>Back To Login</button></a></p>
                    """)
            #Set first_name, last_name for user
            u = temp[0]
            u.first_name = first_name
            u.last_name = last_name
            u.year = year
            u.save()
            request.session['username'] = u
            return redirect('/home/')
        else:
            return render_to_response('codeit/index.html',
             {'userform': form},
             context_instance=RequestContext(request))
    else:
        return render_to_response('codeit/index.html',
            {'userform': UserForm()},
            context_instance=RequestContext(request)
            )


@cache_control(no_cache=True,
    must_revalidate=True,
    no_store=True,
    )
def home(request):
    """
    """
    if 'username' in request.session:
        username = request.session['username']
        problems = Problem.objects.all()
        return render_to_response('codeit/home.html',
            {'username': username,
            'problems': problems},
            context_instance=RequestContext(request))
    else:
        return redirect('/')


@login_required
def logout(request):
    """
    """
    # Check if request contains session var 'username'
    if 'username' in request.session:
        del request.session['username']
    # Return Wrong If session
    else:
        return HttpResponse("""
            <p> You have already logged out.</p>
            <p> Wrong call</p>
            """)
    return HttpResponseRedirect('/')


@cache_control(no_cache=True,
    must_revalidate=True,
    no_store=True,
)
@login_required
def ranking(request):
    """
    Decide ranking of users from points
    """
    if 'username' in request.session:
        username = request.session['username']
        userlist = User.objects.exclude(first_name='-').order_by('total_points').reverse()
        return render_to_response('codeit/ranking.html',
            {'userlist': userlist,
            'username': username,
            },
            context_instance=RequestContext(request)
            )
    else:
        userlist = User.objects.filter().order_by('total_points').reverse()
        return render_to_response('codeit/ranking.html',
            {'userlist': userlist,
            },
            )


@login_required
def problem(request, problem_id):
    problem = Problem.objects.get(pk=problem_id)
    return render_to_response('codeit/problem.html',
        {'problem': problem,
        'fileuploadform': FileUploadForm(),
        },
        context_instance=RequestContext(request)
        )


@login_required
def solution(request, problem_id):
    if request.method == 'POST':
        username = request.session['username']
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            language = form.cleaned_data.get('picked')
            language = language[0]
            user = getuser(username)
        if user:
            problem = Problem.objects.get(pk=problem_id)
            codefile = request.FILES['code']
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
            content = content.split('\n')
            return render_to_response('codeit/solution.html',
                {'content': content,
                },
                )
        else:
            return HttpResponse("User not found for solution submission")
    return redirect('/problem/' + problem_id)


def getuser(username):
    print type(username)
    username = str(username)
    username = username.split(' ')
    try:
        user = User.objects.get(first_name__exact=username[0])
        if user.last_name == username[1]:
            return user
        else:
            return 0
    except KeyError:
        print "Keyerror"
        return 0
