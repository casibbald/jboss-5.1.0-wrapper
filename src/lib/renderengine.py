# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os
import sys
import tempfile
from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions

class Renderer(object):
    
    def __init__(self, template_dir=None):
        self.tmpdir = None
        #if template_dir == None:
        template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
        #    print template_dir
        try:    
            self.template_lookup = TemplateLookup(directories=[template_dir])
        except:
            print exceptions.text_error_template().render()

    def get_temp_dir(self):
        if self.tmpdir == None:
            try:
                tmpdir = tempfile.mkdtemp(prefix='mako-')
                self.tmpdir = tmpdir
                return tmpdir
            except Exception as e:
                print "Error Detected: {0}".format(e)
        else:
            try:
                os.path.isdir(self.tmpdir)
                return self.tmpdir
            except Exception as e:
                print "Error Detected: {0}".format(e)


    def serve_template(self, template_name, **kwargs):
        try:
            render_template = self.template_lookup.get_template(template_name)
            return render_template.render(**kwargs)
        except:
            print exceptions.text_error_template().render()
    
    

if __name__ == '__main__':
    C = {}

    R = Renderer()
    print R.serve_template('.html', C=C)