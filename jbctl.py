#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
###############################################################################
#
# Author          : Charles Sibbald
# Email           : casibbald at gmail dot com
# Contributors    : 
# License         : BSD
# Copyright (c) 2012 Origami Planes Ltd.
# All rights reserved, excluding that of external software or modules
# from 3rd Parties.
# Redistribution and use in source and binary forms are permitted
# provided that the above copyright notice and this paragraph are
# duplicated in all such forms and that any documentation,
# advertising materials, and other materials related to such
# distribution and use acknowledge that the software was developed
# by the <organization>.  The name of the
# University may not be used to endorse or promote products derived
# from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
# 
###############################################################################

import os
import sys

if (sys.version_info[0],sys.version_info[1]) == (2, 4):
    try:
        import argparse
    except Exception, e:
        try:
            import yum #easy way to detect Redhat... will look for another option at some other point. 
            print
            print 'ERROR: failed to import argprse module, try installing the python-argparse.noarch rpm.'
            print 'yum install -y python-argparse'
            sys.exit(1)
        except:
            pass
elif (sys.version_info[0],sys.version_info[1]) == (2, 6) or (2, 7) or (3, 3):
    import argparse


jbosswrapper_parser = argparse.ArgumentParser(description='''A Complete Wrapper domain for JBoss.''',
                                 add_help=True)
jbosswrapper_parser.add_argument('--show-config', action="store_true",
                            help="""""")

prepare_parser = argparse.ArgumentParser(parents=[jbosswrapper_parser], add_help=False)
prepare_parser.add_argument('--start', required=False, help='Start JBoss Domain', action="store", type=str)
prepare_parser.add_argument('--stop', required=False, help='Graceful shutdown of JBoss Domain', action="store", type=str)
prepare_parser.add_argument('--kill', required=False, help='Hard kill of JBoss Domain', action="store", type=str)
prepare_parser.add_argument('--status', required=False, help='Check if JBoss is running (Does PID and port conflict Check', action="store", type=str)


def main():
    options = prepare_parser.parse_args()
    
    if options.show_config:
        from src.impl.configuration import ConfigReader
        C = ConfigReader(options.config)
        print
        C.show_config()
    elif options.config and options.output and not options.show_config:
        from src.impl.transform import generate_xml
        print
        print 'Running xml transform...'
        print 'Check %s/ directory for output.' % (os.path.dirname(options.output))
        print
        generate_xml(options.config, options.output)
        
if __name__ == '__main__':
    main()



