from codeit.forms import UserForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from codeit.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_control


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
def ranking(request):
    """
    Decide ranking of users from points
    """
    if 'username' in request.session:
        username = request.session['username']
        userlist = User.objects.all().order_by('total_points').reverse()
        return render_to_response('codeit/ranking.html',
            {'userlist': userlist,
            'username': username,
            },
            )
    else:
        userlist = User.objects.all().order_by('total_points').reverse()
        return render_to_response('codeit/ranking.html',
            {'userlist': userlist,
            },
            )


def problem(request, problem_id):
    return HttpResponse("You want to solve" + problem_id)
