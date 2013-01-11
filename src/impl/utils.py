# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os
import fnmatch
import sys
import subprocess
import stat
import time

def printer(s):
    s = "".join([s, "\n"])
    sys.stdout.write(str(s))


def locate(pattern, root=os.curdir):
    '''Locate all files matching supplied filename pattern
    in and below supplied root directory.'''
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)


def executePoll(execution_list):
    try:
        execute = subprocess.check_call(execution_list, shell=False,)
    except Exception,e:
        printer("Process Execution Error:")
        printer(e)
        sys.exit(1)

def execute_and_return_output(execution_list):
    output = subprocess.Popen(execution_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text = output.communicate()
    return text[0]

def singleton(cls):
    __instances = {}
    def getinstance():
        if cls not in __instances:
            __instances[cls] = cls()
        return __instances[cls]
    return getinstance


def timethis(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        print func, end-start
        return r
    return wrapper


def fileFinder(base_dir, target_file):
    matches = []
    for root, dirnames, filenames in os.walk(base_dir):
        for filename in fnmatch.filter(filenames, target_file):
            matches.append(os.path.join(root, filename))
    return matches


def func_once(func):
    """A decorator that runs a function only once.
    @func_once
    def get_document():
        import xml.dom.minidom
        return xml.dom.minidom.parse("document.xml")
    """
    def decorated(*args, **kwargs):
        try:
            return decorated._once_result
        except AttributeError:
            decorated._once_result = func(*args, **kwargs)
            return decorated._once_result
    return decorated

def method_once(method):
    "A decorator that runs a method only once."
    attrname = "_%s_once_result" % id(method)
    def decorated(self, *args, **kwargs):
        try:
            return getattr(self, attrname)
        except AttributeError:
            setattr(self, attrname, method(self, *args, **kwargs))
            return getattr(self, attrname)
    return decorated


if __name__ == '__main__':
    pass
