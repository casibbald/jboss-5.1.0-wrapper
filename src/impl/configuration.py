# vim: tabstop=4 shiftwidth=4 softtabstop=4
import ConfigParser
import os
from pprint import pprint
import sys 
import re
from zoneconfig.impl.utils import singleton
 
#@singleton
class ConfigReader(object):
   
    def __init__(self, config_file):
        self.config = None
        self.config = self.read_config_file(config_file)
        #self.config_file = config_file
 
    def read_config_file(self, config_file):
        config = ConfigParser.ConfigParser()
        self.config_file = config_file
        if  os.path.exists(self.config_file):
            try:
                config.readfp(open(self.config_file))
                return config
            except Exception, e:
                print "Error Detected: %s" % (e)
                   

    def write_config(self, config):
        config_file = os.path.join(os.path.expanduser('~'), '.dbtools', 'dbtools.cfg')
        if os.path.exists(os.path.dirname(config_file)):         
            try:
                configfile = open(config_file, 'wb')
                config.write(configfile)
            except Exception, e:
                print "Error Detected: %s" % (e)
                return False
        elif not os.path.exists(os.path.dirname(config_file)):
            try:
                os.makedirs(os.path.dirname(config_file))
                configfile = open(config_file, 'wb')
                config.write(configfile)
            except Exception, e:
                print "Error Detected: %s" % (e)
                return False
        else:
            pass  
 
 
    def has_section(self, config, section):
        try:
            return config.has_section(section)
        except Exception, e:
            print "Error Detected: %s" % (e)
            return False
       
    def add_section(self, config, section):
        try:
            config.add_section(section)
            self.write_config(config)
        except Exception, e:
            print "Error Detected: %s" % (e)
            return False
       
    def remove_section(self, config, section):
        try:
            config.remove_section(section)
            self.write_config(config)
        except Exception, e:
            print "Error Detected: %s" % (e)
            return False
       
    def get_sections(self, config):
        try:
            return config.sections()
        except Exception, e:
            print "Error Detected: %s" % (e)
            print "The config file provided does not have sections"
            return False
       
    def get_section_options(self, config, section):
        try:
            return config.options(section)
        except Exception, e:
            print "Error Detected: %s" % (e)
            return False
       
    def has_option(self, config, section, option):
        try:
            return config.has_option(section, option)
        except Exception, e:
            print "Error Detected: %s" % (e)
            return False
        
    def is_quoted(self, value):
        if value[:1] and value[-1:] == "'" or value[:1] and value[-1:] == '"':
            return True
        else:
            return False 
        
    def get_option(self, config, section, option):
        if config.has_option(section, option):
            try:
                if self.is_quoted(config.get(section, option)):
                    return config.get(section, option)[1:-1]
                else:
                    return config.get(section, option)
            except Exception, e:
                print "Error Detected: %s" % (e)
                return False
       
    def add_option(self, config, section, option):
        if self.config.has_option(section, option):
            try:
                config.set(section, option)
                self.write_config(config)
            except Exception, e:
                print "Error Detected: %s" % (e)
                return False
        else:
            try:
                config.add(section, option)
                self.write_config(config)
            except Exception, e:
                print "Error Detected: %s" % (e)
                return False
           
    def set_option(self, config, section, option, value):
        try:
            config.set(section, option, value)
            self.write_config(config)
        except Exception, e:
            print "Error Detected: %s" % (e)
            return False
       
    def remove_option(self, config, section, option):
        try:
            if config.has_option(section, option):
                config.remove_option(section, option)
                self.write_config(config)   
        except Exception, e:
            print "Error Detected: %s" % (e)
            return False
###########
# Where possible use these.
# The following are convenience functions using the above.
###########


    def get_section_dict(self, section):
        options = self.get_section_options(self.config, section)
        return dict([(option, self.get_option(self.config, section, option)) for option in options])
            
    def get_config_dictionary(self):
        return dict([(section, self.get_section_dict(section)) for section in self.get_sections(self.config)])

    def show_config(self):
        sections = self.get_sections(self.config)
        if sections:
            print "Configuration is as follows: "
            for section in sections:
                print "Section: ", section
                if self.get_section_options(self.config, section):
                    for option in self.get_section_options(self.config, section):
                        print "  Option: %s = %s" % (option, self.get_option(self.config, section, option))
         
if __name__ == '__main__':
    C = ConfigReader('/'.join([os.getcwd(), '..', 'tests', 'zoneconfig-wip.ini']))
    C.show_config()
