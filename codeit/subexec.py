import commands
from django.utils import timezone
import subprocess
import resource
from django.core.files.storage import default_storage
import os
import tempfile
import shutil

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
        #print content1
        #print content2
        a = ["\n", "\r", "\t", " "]
        for i in a:
            print i
            content1 = content1.replace(i, "")
            content2 = content2.replace(i, "")
        if content1 == content2:
            print "content match"
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
    resource.setrlimit(resource.RLIMIT_CPU, (2, 2))
    # RLIMIT_NOFILE => Maxium no of file that process can open
    resource.setrlimit(resource.RLIMIT_NOFILE, (6, 6))
    # RLIMIT_NPROC => Maxium no of processes can be created
    # NPROC does nt work here
    resource.setrlimit(resource.RLIMIT_NPROC, (290, 290))


def lsafelimits():
    """
    java limits
    """
    # RLIMIT_AS => Maximum area of address space which may be taken by the process
    resource.setrlimit(resource.RLIMIT_AS, (1024 * 1024 * 1024, 1024 * 1024 * 1024))
    # RLIMIT_CPU  => Maxium no of cpu time that processor can use.
    resource.setrlimit(resource.RLIMIT_CPU, (3, 3))
    # RLIMIT_NOFILE => Maxium no of file that process can open
    resource.setrlimit(resource.RLIMIT_NOFILE, (20, 20))
    # RLIMIT_NPROC => Maxium no of processes can be created
    # NPROC does nt work here
    # found value is 210
    resource.setrlimit(resource.RLIMIT_NPROC, (350, 350))


def jsafelimits():
    """
    python limits
    """
    # RLIMIT_AS => Maximum area of address space which may be taken by the process
    resource.setrlimit(resource.RLIMIT_AS, (128 * 1024 * 1024 * 1024, 128 * 1024 * 1024 * 1024))
    # RLIMIT_CPU  => Maxium no of cpu time that processor can use.
    resource.setrlimit(resource.RLIMIT_CPU, (3, 3))
    # RLIMIT_NOFILE => Maxium no of file that process can open
    resource.setrlimit(resource.RLIMIT_NOFILE, (20, 20))
    # RLIMIT_NPROC => Maxium no of processes can be created
    # NPROC does nt work here
    # found value is 210
    resource.setrlimit(resource.RLIMIT_NPROC, (350, 350))


def cexec(code, standard_input, standard_output):
    """
    hsafelimits is used to set execution limits
    """
    out = str(code).split(".")[0]
    scommand = "gcc -o " + out + " " + str(code) + " -lm "
    status, output = commands.getstatusoutput(scommand)
    if status != 0:
        return "Compilation error."
    scommand = 'cat ' + standard_input
    p1 = subprocess.Popen([scommand], stdout=subprocess.PIPE, shell=True)
    scommand = '/' + out
    p2 = subprocess.Popen([scommand], stdin=p1.stdout, shell=True, stdout=subprocess.PIPE, preexec_fn=hsafelimits)
    output = p2.communicate()[0]
    print "returncode", p2.returncode
    if p2.returncode == 139:
        return "Sorry, program is not acceptable."
    elif p2.returncode == 137:
        return "Sorry, program is not acceptable."
    elif p2.returncode == 143:
        return "Sorry, program is not acceptable."
    differ = Differ(output, standard_output)
    result = differ.result()
    if result:
        return "Congratulations, your solution has been accepted."
    if p2.returncode == int(-9) or p2.returncode == 127:
        return "Sorry, program is not acceptable."
    return "Sorry, program is not acceptable."


def cppexec(code, standard_input, standard_output):
    """
    hsafelimits is used to set execution limits
    """
    out = str(code).split(".")[0]
    scommand = "g++ -o " + out + " " + str(code) + " -lm "
    status, output = commands.getstatusoutput(scommand)
    if status != 0:
        return "Compilation error."
    scommand = 'cat ' + standard_input
    p1 = subprocess.Popen([scommand], stdout=subprocess.PIPE, shell=True)
    scommand = '/' + out
    p2 = subprocess.Popen([scommand], stdin=p1.stdout, shell=True, stdout=subprocess.PIPE, preexec_fn=hsafelimits)
    output = p2.communicate()[0]
    print output
    print "returncode", p2.returncode
    if p2.returncode == 139:
        return "Sorry, program is not acceptable."
    elif p2.returncode == 137:
        return "Sorry, program is not acceptable."
    elif p2.returncode == 143:
        return "Sorry, program is not acceptable."
    differ = Differ(output, standard_output)
    result = differ.result()
    if result:
        return "Congratulations, your solution has been accepted."
    if p2.returncode == int(-9) or p2.returncode == 127:
        return "Sorry, program is not acceptable."
    return "Sorry, program is not acceptable."


def javaexec(code, standard_input, standard_output):
    javadir = tempfile.mkdtemp()
    shutil.copy(code, javadir)
    orig = os.path.abspath(os.curdir)
    os.chdir(javadir)
    jclass = code.split("-")[-1].split(".")[0].split("_")[0]
    os.rename(code.split("/")[-1], jclass + ".java")
    scommand = "javac " + jclass + ".java"
    status, output = commands.getstatusoutput(scommand)
    if status != 0:
        return "Compilation error."
    scommand = "cat " + standard_input
    p1 = subprocess.Popen([scommand], stdout=subprocess.PIPE, shell=True)
    scommand = "java " + jclass
    p2 = subprocess.Popen([scommand], stdin=p1.stdout, shell=True,
        stdout=subprocess.PIPE, preexec_fn=jsafelimits)
    output = p2.communicate()[0]
    os.chdir(orig)
    shutil.rmtree(javadir)
    print "returncode", p2.returncode
    if p2.returncode == 139:
        return "Sorry, program is not acceptable."
    elif p2.returncode == 137:
        return "Sorry, program is not acceptable."
    elif p2.returncode == 143:
        return "Sorry, program is not acceptable."
    elif p2.returncode == -9:
        return "Sorry, program is not acceptable."
    differ = Differ(output, standard_output)
    result = differ.result()
    if result:
        return "Congratulations, your solution has been accepted."
    return "Sorry, program is not acceptable."


def pythonexec(code, standard_input, standard_output):
    """
    lsafelimits is used to set limits before process execution.
    """
    p2 = subprocess.Popen(["python " + str(code) + " < " + str(standard_input)],
        stdout=subprocess.PIPE,
        shell=True, preexec_fn=lsafelimits)
    output = p2.communicate()[0]
    print output
    print "returncode", p2.returncode
    if p2.returncode == 1:
        return "Sorry, program is not acceptable."
    elif p2.returncode == 137:
        return "Sorry, program is not acceptable."
    elif p2.returncode == 143:
        return "Sorry, program is not acceptable."
    differ = Differ(output, standard_output)
    result = differ.result()
    if result:
        return "Congratulations, your solution has been accepted."
    return "Sorry, program is not acceptable."
