from codeit.models import *
import os
import commands
from django.utils import timezone
from codeit.models import Differ


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
    start = timezone.now()
    code = mediapath(sol.text.name)
    standard_input = mediapath(problem.standard_input.name)
    standard_output = mediapath(problem.standard_output.name)
    language = sol.language
    print language
    scommands = []

    if language == 'c':
        out = str(code).split(".")[0]
        #scommand = "gcc -c " + str(code)
        #scommands.append(scommand)
        scommand = "gcc -o " + out + " " + str(code)
        scommands.append(scommand)
        scommand = "/" + out + " < " + standard_input + " > " + out + ".txt"
        scommands.append(scommand)
        for scommand in scommands:
            status, output = commands.getstatusoutput(scommand)
            if status != 0:
                return -1
        differ = Differ(out + ".txt", standard_output)
        result = differ.result()
        content = default_storage.open(out + ".txt").read()
        total = timezone.now() - start
        print "server time for cpp", total
        return content

    elif language == 'cpp':
        out = str(code).split(".")[0]
        #scommand = "g++ -c " + str(code)
        #scommands.append(scommand)
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
        content = default_storage.open(out + ".txt").read()
        total = timezone.now() - start
        print "server time for cpp", total
        return content

    elif language == 'java':
        print 'Java language'

    elif language == 'py':
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

    else:
        return -1


"""
Your program will be compiled and run in our system, and the automatic judge will test it with some inputs and outputs,
or perhaps with a specific judge tool. After some seconds or minutes, you'll receive by e-mail (or you'll see in the web)
one of these answers

In Queue (QU): The judge is busy and can't attend your submission. It will be judged as soon as possible.

Accepted (AC): OK! Your program is correct! It produced the right answer in reasoneable time and within
the limit memory usage. Congratulations!

Presentation Error (PE): Your program outputs are correct but are not presented in the correct way.
Check for spaces, justify, line feeds...

Wrong Answer (WA): Correct solution not reached for the inputs. The inputs and outputs that we use to test
the programs are not public so you'll have to spot the bug by yourself (it is recomendable to get accustomed to a true
contest dynamic ;-)). If you truly think your code is correct, you can contact us using the link on the left.
Judge's ouputs are not always correct...

Compile Error (CE): The compiler could not compile your program. Of course, warning messages are not error messages.
The compiler output messages are reported you by e-mail.

Runtime Error (RE): Your program failed during the execution (segmentation fault, floating point exception...). The exact cause
is not reported to the user to avoid hacking. Be sure that your program returns a 0 code to the shell. If you're using Java,
please follow all the submission specifications.

Time Limit Exceeded (TL): Your program tried to run during too much time; this error doesn't allow you to know
if your program would reach the correct solution to the problem or not.

Memory Limit Exceeded (ML): Your program tried to use more memory than the judge allows. If you are sure that
such problem needs more memory, please contact us.

Output Limit Exceeded (OL): Your program tried to write too much information. This usually occurs if it goes
into a infinite loop.

Submission Error (SE): The submission is not sucessful. This is due to some error during the
submission process or data corruption.

Restricted Function (RF): Your program is trying to use a function that we considered harmful to the system.
 If you get this verdict you probably know why...

Can't Be Judged (CJ): The judge doesn't have test input and outputs for the selected problem. While choosing
a problem be careful to ensure that the judge will be able to judge it!

"""
