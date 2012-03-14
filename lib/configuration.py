#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
import ConfigParser
import os
import sys 

from utils import singleton
from utils import get_os_seperator

seperator = get_os_seperator()

@singleton
class Config(object):
   
    def __init__(self, config_file=None):
        self.config_dir = os.path.join(os.path.abspath(__file__), seperator[1], 'environment')
        self.default_config_file = os.path.join(self.config_dir, 'default', 'env.properties')
        self.custom_config_file = os.path.join(self.config_dir, 'custom', 'env.properties')
        self.config = self.read_config_file(self.config_file)
 
        #                                  SectionName          Option        DefaultValueIfNotSet
        self.default_config_dictionary = {'Authentication' :    {'username'    : 'daffy',
                                                                 'password'    : 'duck'},
        'Nexus'          :    {'hostname'    : 'localhost',
                               'port'        : '8081'},
        'Subversion'     :    {'hostname'    : 'localhost',
                               'port'        : '80',
                               'protocol'    : 'http',
                               'base_project': 'canvas'},
        'SMTP'           :    {'hostname'    : 'localhost',
                               'port'        : '25',
                               'debug'       : True,
                               'mail_domain' : 'mydomain' },
        'Notification': {'author'  : 'me@mydomain',
                         'alpha'   : 'me', 
                         'beta'    : '',
                         'release' : ''},
      }


    def validate_set_options(self):
        count = 3 #Count must be the depth of default_config_dictionary data structure
        while count != 0:
            for section in self.default_config_dictionary:
                if self.has_section(self.config, section):
                    for option in self.default_config_dictionary[section]:
                        if self.has_option(self.config, section, option ):
                            option_value = self.get_option(self.config, section, option)
                            if option_value == '':
                                print "  Option {0} = {1}".format(option, 'None - Unset value')
                        else:
                            self.set_option(self.config, section, option, self.default_config_dictionary[section][option])
                else:
                    self.add_section(self.config, section)
            count -= 1 
 
    def read_config_file(self, config_file):
        config = ConfigParser.ConfigParser()
        if config_file == None:
            self.config_file = self.default_config_file
            if  os.path.exists(self.config_file):
                try:
                    config.readfp(open(self.config_file))
                except IOError:
                    pass # TODO CHECK EXCEPTION AND LOG
            else:
                config.readfp(open(self.config_file))
        else:
            try:
                config.readfp(open(config_file))
            except IOError:
                pass # TODO CHECK EXCEPTION AND LOG
        return config
 
    def write_config(self, config):
        config_file = self.default_config_file
        if os.path.exists(os.path.dirname(config_file)):         
            try:
                with open(config_file, 'wb') as configfile:
                    config.write(configfile)
            except Exception as e:
                print "Error Detected: {0}".format(e)
                return False
        elif not os.path.exists(os.path.dirname(config_file)):
            try:
                os.makedirs(os.path.dirname(config_file))
                with open(config_file, 'wb') as configfile:
                    config.write(configfile)
            except Exception as e:
                print "Error Detected: {0}".format(e)
                return False
        else:
            pass  
 
    def has_section(self, config, section):
        try:
            return config.has_section(section)
        except Exception as e:
            print "Error Detected: {0}".format(e)
            return False
       
    def add_section(self, config, section):
        try:
            config.add_section(section)
            self.write_config(config)
        except Exception as e:
            print "Error Detected: {0}".format(e)
            return False
       
    def remove_section(self, config, section):
        try:
            config.remove_section(section)
            self.write_config(config)
        except Exception as e:
            print "Error Detected: {0}".format(e)
            return False
       
    def get_sections(self, config):
        try:
            return config.sections()
        except Exception as e:
            print "Error Detected: {0}".format(e)
            return False
       
    def get_section_options(self, config, section):
        try:
            return config.options(section)
        except Exception as e:
            print "Error Detected: {0}".format(e)
            return False
       
    def has_option(self, config, section, option):
        try:
            return config.has_option(section, option)
        except Exception as e:
            print "Error Detected: {0}".format(e)
            return False
       
    def get_option(self, config, section, option):
        if config.has_option(section, option):
            try:
                return config.get(section, option)
            except Exception as e:
                print "Error Detected: {0}".format(e)
                return False
       
    def add_option(self, config, section, option):
        if self.config.has_option(section, option):
            try:
                config.set(section, option)
                self.write_config(config)
            except Exception as e:
                print "Error Detected: {0}".format(e)
                return False
        else:
            try:
                config.add(section, option)
                self.write_config(config)
            except Exception as e:
                print "Error Detected: {0}".format(e)
                return False
           
    def set_option(self, config, section, option, value):
        try:
            config.set(section, option, value)
            self.write_config(config)
        except Exception as e:
            print "Error Detected: {0}".format(e)
            return False
       
    def remove_option(self, config, section, option):
        try:
            if config.has_option(section, option):
                config.remove_option(section, option)
                self.write_config(config)   
        except Exception as e:
            print "Error Detected: {0}".format(e)
            return False
            
    def show_config(self):
        sections = self.get_sections(self.config)
        print "Configuration for Release Tools System is as follows: "
        for section in sections:
            print "Section: ", section
            for option in self.get_section_options(self.config, section):
                print "  Option: {0} = {1}".format(option, self.get_option(self.config, section, option)) 
 
if __name__ == '__main__':
    C = Config()
    C.validate_set_options()
    C.show_config()



