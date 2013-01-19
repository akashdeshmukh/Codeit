import commands
from django.utils import timezone
import subprocess
from codeit.models import Differ
import resource


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


def cexec(code, standard_input, standard_output):
    #start = timezone.now()
    out = str(code).split(".")[0]
    scommand = "gcc -o " + out + " " + str(code)
    status, output = commands.getstatusoutput(scommand)
    if status != 0:
        return "CE: Compile Error.\n"
    scommand = 'cat ' + standard_input
    p1 = subprocess.Popen([scommand], stdout=subprocess.PIPE, shell=True)
    scommand = '/' + out
    start = timezone.now()
    p2 = subprocess.Popen([scommand], stdin=p1.stdout, shell=False, stdout=subprocess.PIPE, preexec_fn=hsafelimits)
    final = timezone.now() - start
    output = p2.communicate()[0]
    if p2.returncode == 139:
        return "ML : Memory Limit Exceeded\n" + str(final)
    elif p2.returncode == 137:
        return "TL : Time Limited Exceeded\n" + str(final)
    differ = Differ(output, standard_output)
    result = differ.result()
    if result:
        return "AC : Accepted\n" + str(final)
    return "WS : Wrong Solution\n" + str(final)


def cppexec(code, standard_input, standard_output):
    out = str(code).split(".")[0]
    scommand = "g++ -o " + out + " " + str(code)
    status, output = commands.getstatusoutput(scommand)
    if status != 0:
        return "CE: Compile Error.\n"
    scommand = 'cat ' + standard_input
    p1 = subprocess.Popen([scommand], stdout=subprocess.PIPE, shell=True)
    scommand = '/' + out
    start = timezone.now()
    p2 = subprocess.Popen([scommand], stdin=p1.stdout, shell=False, stdout=subprocess.PIPE, preexec_fn=hsafelimits)
    final = timezone.now() - start
    output = p2.communicate()[0]
    if p2.returncode == 139:
        return "ML : Memory Limit Exceeded\n" + str(final)
    elif p2.returncode == 137:
        return "TL : Time Limited Exceeded\n" + str(final)
    differ = Differ(output, standard_output)
    result = differ.result()
    if result:
        return "AC : Accepted\n" + str(final)
    return "WS : Wrong Solution\n" + str(final)


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
