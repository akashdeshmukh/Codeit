from codeit.models import *
from django.shortcuts import redirect
from codeit.subexec import *


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


def mediapath(text):
    return "/home/tripples/codeit/CJ/media/" + text
    """
    if 'media' in spath:
        pass
    else:
        spath = spath.split("CJ")
        spath = spath[0] + "CJ/media" + spath[1]
    """


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


def final_ex(sol, problem):
    code = mediapath(sol.text.name)
    print "Code", code
    standard_input = mediapath(problem.standard_input.name)
    print "standard_input", standard_input
    standard_output = mediapath(problem.standard_output.name)
    print "standard_output", standard_output
    language = sol.language
    print language
    if language == 'c':
        return cexec(code, standard_input, standard_output)
    elif language == 'cpp':
        return cppexec(code, standard_input, standard_output)
    elif language == 'java':
        return javaexec(code, standard_input, standard_output)
    elif language == 'py':
        return pythonexec(code, standard_input, standard_output)
    else:
        return "Language Not Found"
