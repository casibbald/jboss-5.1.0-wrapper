#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
'''
Created on Oct 18, 2012

@author: casibbald
'''

import os #site, errno;
import sys
import tarfile
import shutil
import urllib2

python_version = sys.version[:3]

userhome = os.path.expanduser("~")

def checkenvpaths(path):
    currentpath = os.environ.get('PATH')
    if currentpath.find(path) == 0 :
        print "Python Path has been set to : %s" % (path)
        return True
    elif currentpath.find(path) == -1:
        print "Python Path has NOT been set.................!"
        return False


def detect_environment():
    environment = {}
    environment['os_detected'] = sys.platform
    python_version = sys.version[:3]
    if environment['os_detected'] == 'darwin':
        environment['userprofile'] = os.path.join(userhome, ".bash_profile")
        environment['fileName'] = os.path.join(userhome, '.pydistutils.cfg')
        environment['bin_dir'] = os.path.join(userhome, "bin")
        environment['install_dir'] = os.path.join(userhome, "Library", "python", python_version, "site-packages")
        environment['python_dir'] = os.path.join("/Library", "Frameworks", "Python.framework", "Versions", python_version, "bin")
        environment['ssh_dir'] = os.path.join(userhome, '.ssh')
    elif environment['os_detected'] == 'linux' or 'linux2' :
        environment['userprofile'] = os.path.join(userhome, ".bashrc")
        environment['fileName'] = os.path.join(userhome, '.pydistutils.cfg')
        environment['bin_dir'] = os.path.join(userhome, "bin")
        environment['install_dir'] = os.path.join("/", "usr", "lib", ''.join(["python", python_version]), "site-packages")
        environment['python_dir'] = os.path.join(userhome, "Library", "Frameworks", "Python.framework", "Versions", python_version, "bin")
        environment['ssh_dir'] = os.path.join(userhome, '.ssh')
    elif environment['os_detected'] == 'sunos5':
        environment['userprofile'] = os.path.join(userhome, ".profile")
        environment['fileName'] = os.path.join(userhome, '.pydistutils.cfg')
        environment['bin_dir'] = os.path.join(userhome, "bin")
        environment['install_dir'] = os.path.join(userhome, "Library", "python", python_version, "site-packages")
        environment['python_dir'] = os.path.join(userhome, "Library", "Frameworks", "Python.framework", "Versions", python_version, "bin")
        environment['ssh_dir'] = os.path.join('/etc', 'ssh', 'keys')
    elif environment['os_detected'] == 'windows' or 'win32' :
        environment['fileName'] = os.path.join(userhome, '.pydistutils.cfg')
        environment['bin_dir'] = os.path.join(userhome, "bin")
        environment['install_dir'] = os.path.join(userhome, "Library", "python", python_version, "site-packages")
        environment['python_dir'] = os.path.join(userhome, "Library", "Frameworks", "Python.framework", "Versions", python_version, "bin")
        environment['ssh_dir'] = os.path.join(userhome, '.ssh')
    else:
        environment['fileName'] = os.path.join(userhome, '.pydistutils.cfg')
        environment['bin_dir'] = os.path.join(userhome, "bin")
        environment['install_dir'] = os.path.join(userhome, "lib", "python", python_version, "site-packages")
    return environment

environment = detect_environment()

system_os = {   'darwin' : """[install]
install_lib = %s
install_scripts = %s """ % (environment['install_dir'], environment['bin_dir']),
                'linux' : """[install]
install_lib = %s
install_scripts = %s""" % (environment['install_dir'], environment['bin_dir']),
                'linux2' : """[install]
install_lib = %s
install_scripts = %s""" % (environment['install_dir'], environment['bin_dir']),
                'sunos5' : """[install]
install_lib = %s
install_scripts = %s""" % (environment['install_dir'], environment['bin_dir']),
                'windows' : """[install]
install_lib = %s
install_scripts = %s""" % (environment['install_dir'], environment['bin_dir']),
            }

class Filer(object):
    def __init__(self):
        print "Filer initalised"

    def createFile(self, FQFileName):
        self.fileName = FQFileName
        if not os.path.exists(self.fileName):  # Avoid clobbering files
            try:
                print
                print "Creating : %s" % (self.fileName)
                o = open(self.fileName, "w")
                o.flush()
                o.close()
            finally:
                pass

    def writeThisToFile(self, stringToWrite):
        if os.path.exists(self.fileName):  # Avoid clobbering files
            try:
                print
                print "Writing to : %s " % (self.fileName)
                w = open(self.fileName, "w")
                w.write(stringToWrite)
                w.write("\n")
                w.flush()
                w.close()
            finally:
                pass


class ThirdPartyApp(object):
    def __init__(self):
        print
        print "Third Party Install Instance Initialised"
        self.thirdparty = os.path.join(os.getcwd(), "thirdparty")
        if not os.path.exists(self.thirdparty):
            try:
                print
                print "Creating Thirdparty Directory: %s " % (self.thirdparty)
                os.mkdir(self.thirdparty)
            except OSError :
                pass

        if not os.path.exists(environment['install_dir']):
            try:
                print "Creating Python Egg Directory: %s" % (environment['install_dir'])
                os.makedirs(environment['install_dir'])
            except OSError :
                pass

        if not os.path.exists(environment['bin_dir']):
            try:
                print "Creating Python Egg Directory: %s" % (environment['bin_dir'])
                os.makedirs(environment['bin_dir'])
            except OSError :
                pass

    def legacy_download_this(self, url, to_dir, saveas=None):
        """This Class Method is only used once to pull down the very basic requirements of the project.
        **kwargs saveas is used if the downloaded file should be renamed when saved to disk.
        """
        self.url = url
        self.to_dir = to_dir
        self.saveas = saveas
        if self.saveas:
            self.saveto = os.path.join(self.to_dir, self.saveas)
        else:
            self.saveto = os.path.join(self.to_dir, os.path.basename(self.url))
            
        self.src = self.dst = None
        if not os.path.exists(self.saveto):  # Avoid repeated downloads
            try:
                print
                print "Attempting to Download : %s from %s" % (os.path.basename(self.url), os.path.dirname(self.url))
                self.src = urllib2.urlopen(self.url)
                # Read/write all in one block, so we don't create a corrupt file
                # if the download is interrupted.
                self.data = self.src.read()
                self.dst = open(self.saveto,"wb"); self.dst.write(self.data)
            finally:
                if self.src:
                    self.src.close()
                if self.dst:
                    self.dst.close()
                    print "%s Downloaded Successfully" % (os.path.basename(self.url))
                    print
        return os.path.realpath(self.saveto)


    def determine_compression_algorithim(self, infile):
        self.infile = infile
        if self.infile.endswith(".tar") :
            self.arc_type = 'r:*'
        elif self.infile.endswith(".gz") :
            self.arc_type = 'r:gz'
        elif self.infile.endswith(".bz2") :
            self.arc_type = 'r:bz2'
        elif self.infile.endswith(".zip") :
            self.arc_type = 'r:*'
        print "File %s detected as a %s " % (self.infile, self.arc_type.split(":")[1])
        return self.arc_type

    def extract_archive(self, infile, to_dir):
        self.infile = infile
        self.to_dir = to_dir
        print "Archive to extract: ", self.infile
        self.tar = tarfile.open(self.infile, self.determine_compression_algorithim(self.infile))
        self.tar.extractall(self.to_dir)
        self.tar.close()

    def read_thirdparty_config(self):
        if os.path.exists("thirdparty.cfg"):
            self.fileToRead = ("thirdparty.cfg")
        print self.fileToRead
        self.thirdparty_app = {}
        self.f = open(self.fileToRead,'r')
        self.details = self.f.readlines()
        for self.detail in self.details:
            if not self.detail.isspace() :
                if not self.detail.startswith('#'):
                    self.pair = self.detail.split('||')
                    if self.pair[0]:
                        self.thirdparty_app[self.pair[0].strip()] = (self.pair[1].strip(), self.pair[2].strip())
        return self.thirdparty_app


def cleandest():
    builddest = os.path.abspath("build")
    distdest = os.path.abspath("dist")
    buildegg = os.path.join(environment['install_dir'], "releasetools-*")
    if os.path.exists(builddest):
        try:
            print "Cleaning Build Destination: %s" % (builddest)
            shutil.rmtree(builddest)
        except OSError :
            pass

    if os.path.exists(distdest):
        try:
            print "Cleaning Dist Destination: : %s" % (distdest)
            shutil.rmtree(distdest)
        except OSError :
            pass

    if os.path.exists(buildegg):
        try:
            print "Destroying Previously Built Egg: : %s" % (buildegg)
            shutil.rmtree(buildegg)
        except OSError :
            pass

def configure_python() :
    """Configure python to use seperate site packages dir if NO Virtual Environment is detected"""
    print "Operating System Detected : ", environment['os_detected']
    f = Filer()
    f.createFile(environment['fileName'])
    f.writeThisToFile(system_os[environment['os_detected']])
    third_party_app = ThirdPartyApp()
    app_list = third_party_app.read_thirdparty_config()
    for each in app_list:
        if each == 'ez_setup':
            third_party_app.legacy_download_this(app_list[each][0], os.getcwd(), saveas='ez_setup.py')
        else:
            third_party_app.legacy_download_this(app_list[each][0], os.path.join(os.path.join(os.getcwd(), "thirdparty")))
    
