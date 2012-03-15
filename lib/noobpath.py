# vim: tabstop=4 shiftwidth=4 softtabstop=4
from xml.dom.minidom import parse, parseString

class noobPath(object):
    def __init__(self, dom):
        self.dom = dom
    
    def split_path(self, path):
        pass
    
    def walk(self, path):
        pass

    def has_nodeName(self, path):
        pass
    
    def has_attribute(self, path, name):
        pass
    
    def has_attributes(self, path):
        pass

    def get_attribute(self, path, name):
        pass

    def get_attributes(self, path):
        pass
    
    def set_attribute(self, path, name):
        pass
    
    def find_pathWithAttributeName(self, basePath, name):
        pass
    
    def get_childNodesByType(self, basePath, Bytype):
        pass
    
    