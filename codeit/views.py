from codeit.forms import UserForm
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from codeit.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_control


def index(request):
    print "In Index"
    if 'username' in request.session:
        return redirect('/home/')
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            receipt_no = request.POST['receipt_no']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            """
            u = User.objects.create(receipt_no=receipt_no,
                first_name=first_name,
                last_name=last_name,
                total_points=0
                )
            u.save()
            print u
            """
            request.session['username'] = first_name + " " + last_name
            return redirect('/home/')
        else:
            form.full_clean()
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
    print "In home"
    if 'username' in request.session:
        username = request.session['username']
        return render_to_response('codeit/home.html',
            {'username': username},
            context_instance=RequestContext(request))
    else:
        return redirect('/')


def logout(request):
    print "In Logout"
    if 'username' in request.session:
        del request.session['username']
        print "session delete"
    else:
        return HttpResponse("Wrong call")
    return HttpResponseRedirect('/')
