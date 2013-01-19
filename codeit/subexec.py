import commands
from django.utils import timezone
import subprocess
import resource
from django.core.files.storage import default_storage
import os


class Differ(object):
    """
    Checks difference between user output
    and standard_output
    """
    def __init__(self, output, standard_output):
        self.output = output
        self.standard_output = standard_output

    def result(self):
        content1 = self.output
        content2 = default_storage.open(self.standard_output).read()
        content1 = content1.replace("\n", "").replace(" ", "")
        content2 = content2.replace("\n", "").replace(" ", "")
        if content1 == content2:
            return 1
        else:
            return 0


def hsafelimits():
    """
    safe limits for c, c++
    """
    # RLIMIT_AS => Maximum area of address space which may be taken by the process
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
    # RLIMIT_CPU  => Maxium no of cpu time that processor can use.
    resource.setrlimit(resource.RLIMIT_CPU, (3, 3))
    # RLIMIT_NOFILE => Maxium no of file that process can open
    resource.setrlimit(resource.RLIMIT_NOFILE, (6, 6))
    # RLIMIT_NPROC => Maxium no of processes can be created
    # NPROC does nt work here
    resource.setrlimit(resource.RLIMIT_NPROC, (0, 0))


def lsafelimits():
    """
    safe limits for java, python, ruby
    """
    # RLIMIT_AS => Maximum area of address space which may be taken by the process
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
    # RLIMIT_CPU  => Maxium no of cpu time that processor can use.
    resource.setrlimit(resource.RLIMIT_CPU, (6, 6))
    # RLIMIT_NOFILE => Maxium no of file that process can open
    resource.setrlimit(resource.RLIMIT_NOFILE, (20, 20))
    # RLIMIT_NPROC => Maxium no of processes can be created
    # NPROC does nt work here
    # found value is 210
    resource.setrlimit(resource.RLIMIT_NPROC, (230, 230))


def cexec(code, standard_input, standard_output):
    """
    hsafelimits is used to set execution limits
    """
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
    print "returncode", p2.returncode
    if p2.returncode == 139:
        return "ML : Memory Limit Exceeded\n" + str(final)
    elif p2.returncode == 137:
        return "TL : Time Limited Exceeded\n" + str(final)
    elif p2.returncode == 143:
        return "RE : Runtime Error\n" + str(final)
    elif p2.returncode == -9:
        return "RC : Restriced Call\n" + str(final)
    differ = Differ(output, standard_output)
    result = differ.result()
    if result:
        return "AC : Accepted\n" + str(final)
    return "WS : Wrong Solution\n" + str(final)


def cppexec(code, standard_input, standard_output):
    """
    hsafelimits is used to set execution limits
    """
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
    print "returncode", p2.returncode
    if p2.returncode == 139:
        return "ML : Memory Limit Exceeded\n" + str(final)
    elif p2.returncode == 137:
        return "TL : Time Limited Exceeded\n" + str(final)
    elif p2.returncode == 143:
        return "RE : Runtime Error\n" + str(final)
    elif p2.returncode == -9:
        return "RC : Restriced Call\n" + str(final)
    differ = Differ(output, standard_output)
    result = differ.result()
    if result:
        return "AC : Accepted\n" + str(final)
    return "WS : Wrong Solution\n" + str(final)


def pythonexec(code, standard_input, standard_output):
    """
    This is final fuction that evaluated python code
    lsafelimits is used to set limits before process execution.
    """
    scommand = "cat " + standard_input
    p1 = subprocess.Popen([scommand], stdout=subprocess.PIPE, shell=True)
    os.chmod(str(code), 0775)
    start = timezone.now()
    p2 = subprocess.Popen(["python " + str(code)],
       stdin=p1.stdout, stdout=subprocess.PIPE,
        shell=True, preexec_fn=lsafelimits)
    final = timezone.now() - start
    output = p2.communicate()[0]
    print "returncode", p2.returncode
    if p2.returncode == 1:
        return "ML : Memory Limit Exceeded\n" + str(final)
    elif p2.returncode == 137:
        return "TL : Time Limited Exceeded\n" + str(final)
    elif p2.returncode == 143:
        return "RE : Runtime Error\n" + str(final)

    differ = Differ(output, standard_output)
    result = differ.result()
    if result:
        return "AC : Accepted\n" + str(final)
    return "WS : Wrong Solution\n" + str(final)


def javaexec(code, standard_input, standard_output):
    return """
    TODO :
    Java to be implemented
    """

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
