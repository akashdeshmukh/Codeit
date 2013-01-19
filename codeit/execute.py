from codeit.models import *
import os
import commands
import subprocess
import resource
from django.shortcuts import redirect
from django.utils import timezone
from codeit.models import Differ


def hsafelimits():
    # RLIMIT_AS => Maximum area of address space which may be taken by the process
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
    # RLIMIT_CPU  => Maxium no of cpu time that processor can use.
    resource.setrlimit(resource.RLIMIT_CPU, (3, 3))
    # RLIMIT_NOFILE => Maxium no of file that process can open
    resource.setrlimit(resource.RLIMIT_NOFILE, (6, 6))
    # RLIMIT_NPROC => Maxium no of processes can be created
    # NPROC does nt work here
    #resource.setrlimit(resource.RLIMIT_NPROC, (20, 20))


def lsafelimits():
    # RLIMIT_AS => Maximum area of address space which may be taken by the process
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
    # RLIMIT_CPU  => Maxium no of cpu time that processor can use.
    resource.setrlimit(resource.RLIMIT_CPU, (6, 6))
    # RLIMIT_NOFILE => Maxium no of file that process can open
    resource.setrlimit(resource.RLIMIT_NOFILE, (6, 6))
    # RLIMIT_NPROC => Maxium no of processes can be created
    # NPROC does nt work here
    #resource.setrlimit(resource.RLIMIT_NPROC, (20, 20))


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
    spath = os.path.abspath(text)
    if 'media' in spath:
        pass
    else:
        spath = spath.split("CJ")
        spath = spath[0] + "CJ/media" + spath[1]
    return spath


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
    """
    TODO :
    Accepted (AC)
    Wrong Answer (WA)
    Compile Error (CE)
    Runtime Error (RE)
    Time Limit Exceeded (TL)
    Memory Limit Exceeded (ML)
    Output Limit Exceeded (OL)
    Submission Error (SE)
    Restricted Function (RF)
    Can't Be Judged (CJ)
    """

    code = mediapath(sol.text.name)
    standard_input = mediapath(problem.standard_input.name)
    standard_output = mediapath(problem.standard_output.name)
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


def cexec(code, standard_input, standard_output):
    #start = timezone.now()

    out = str(code).split(".")[0]
    scommand = "gcc -o " + out + " " + str(code)
    status, output = commands.getstatusoutput(scommand)
    if status != 0:
        return """\nCE:\tCompile Error.\n"""

    scommand = 'cat ' + standard_input
    p1 = subprocess.Popen([scommand], stdout=subprocess.PIPE, shell=True)
    scommand = '/' + out
    start = timezone.now()
    p2 = subprocess.Popen([scommand], stdin=p1.stdout, shell=True, stdout=subprocess.PIPE, preexec_fn=hsafelimits)
    output = p2.communicate()[0]
    print dir(p2)
    final = timezone.now() - start
    print "Final Time", final
    print output
    if p2.returncode == 139:
        return "ML : Memory Limit Exceeded\n" + str(final)
    elif p2.returncode == 137:
        return "TL : Time Limited Exceeded\n" + str(final)

    """
    scommand = "/" + out + " < " + standard_input + " > " + out + ".txt"
    scommands.append(scommand)
    for scommand in scommands:
        status, output = commands.getstatusoutput(scommand)
        if status != 0:
            return -1

    differ = Differ(out + ".txt", standard_output)
    result = differ.result()
    print result
    content = default_storage.open(out + ".txt").read()
    total = timezone.now() - start
    print "server time for c", total
    return content
    """
    return output


def cppexec(code, standard_input, standard_output):
    scommands = []
    start = timezone.now()
    out = str(code).split(".")[0]

    scommand = "g++ -o " + out + " " + str(code)
    scommands.append(scommand)
    scommand = "/" + out + " < " + standard_input + " > " + out + ".txt"
    scommands.append(scommand)
    for scommand in scommands:
        status, output = commands.getstatusoutput(scommand)
        if status != 0:
            return -1
    differ = Differ(out + ".txt", standard_output)
    result = differ.result()
    print result
    content = default_storage.open(out + ".txt").read()
    total = timezone.now() - start
    print "server time for cpp", total
    return content


def javaexec(code, standard_input, standard_output):
    return "Java to be implemented"
    """
    scommands = []
    start = timezone.now()
    out = str(code).split(".")[0]
    javatemp = os.path.expanduser("~/javatemp")
    if os.path.exists(javatemp):
        os.chdir(javatemp)
    else:
        os.makedirs(javatemp)
        os.chdir(javatemp)

    scommand = "javac" + out + " " + str(code)
    scommands.append(scommand)
    scommand = "/" + out + " < " + standard_input + " > " + out + ".txt"
    scommands.append(scommand)
    for scommand in scommands:
        status, output = commands.getstatusoutput(scommand)
        if status != 0:
            return -1
    differ = Differ(out + ".txt", standard_output)
    result = differ.result()
    print result
    content = default_storage.open(out + ".txt").read()
    total = timezone.now() - start
    print "server time for cpp", total
    return content
    """


def pythonexec(code, standard_input, standard_output):
    scommands = []
    start = timezone.now()
    out = str(code).split(".")[0]
    scommand = "python " + str(code) + " < " + standard_input + " > " + out + ".txt"
    scommands.append(scommand)
    print scommand
    for scommand in scommands:
        status, output = commands.getstatusoutput(scommand)
        if status != 0:
            return -1

    differ = Differ(out + ".txt", standard_output)
    result = differ.result()
    print result
    content = default_storage.open(out + ".txt").read()
    total = timezone.now() - start
    print "server time constrait for python", total
    return content
