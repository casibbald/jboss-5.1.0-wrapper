# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os
import sys

class Filer():
    def __init__(self):
        pass

    def createFile(self, FQFileName):
        self.fileName = FQFileName
        if not os.path.exists(self.fileName):  # Avoid clobbering files
            try:
                print
                print "Creating : {0}".format(self.fileName)
                self.o = open(self.fileName, "w")
            finally:
                self.o.flush()
                self.o.close()

    def writeThisToFile(self, stringToWrite):
        self.stringToWrite = stringToWrite
        if os.path.exists(self.fileName):  # Avoid clobbering files
            try:
                print
                print "Writing to : {0}".format(self.fileName)
                print "{0}".format(self.stringToWrite)
                self.w = open(self.fileName, "w")
                self.w.write(self.stringToWrite)
                self.w.write("\n")
            finally:
                self.w.flush()
                self.w.close()

    def appendThisToFile(self, stringToWrite, FQFileName):
        self.stringToWrite = stringToWrite
        self.fileName = FQFileName
        if os.path.exists(self.fileName):  # Avoid clobbering files
            try:
                print
                print "Appending to : {0}".format(self.fileName)
                print "{0}".format(self.stringToWrite)
                self.w = open(self.fileName, "a")
                self.w.write(self.stringToWrite)
            finally:
                self.w.flush()
                self.w.close()