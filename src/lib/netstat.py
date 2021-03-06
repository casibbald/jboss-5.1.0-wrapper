#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import pwd
import os
import re
import glob
 
PROC_TCP = "/proc/net/tcp"
STATE = {
        '01':'ESTABLISHED',
        '02':'SYN_SENT',
        '03':'SYN_RECV',
        '04':'FIN_WAIT1',
        '05':'FIN_WAIT2',
        '06':'TIME_WAIT',
        '07':'CLOSE',
        '08':'CLOSE_WAIT',
        '09':'LAST_ACK',
        '0A':'LISTEN',
        '0B':'CLOSING'
        }
 
def _load():
    with open(PROC_TCP,'r') as f:
        content = f.readlines()
        content.pop(0)
    return content
 
def _hex2dec(s):
    return str(int(s,16))
 
def _ip(s):
    ip = [(_hex2dec(s[6:8])),(_hex2dec(s[4:6])),(_hex2dec(s[2:4])),(_hex2dec(s[0:2]))]
    return '.'.join(ip)
 
def _remove_empty(array):
    return [x for x in array if x !='']
 
def _convert_ip_port(array):
    host,port = array.split(':')
    return _ip(host),_hex2dec(port)
 
def get_netstat():
    '''
    Function to return a list with status of tcp connections at linux systems
    To get pid of all network process running on system, you must run this script
    as superuser
    '''
 
    content=_load()
    result = []
    for line in content:
        line_array = _remove_empty(line.split(' '))
        l_host,l_port = _convert_ip_port(line_array[1])
        r_host,r_port = _convert_ip_port(line_array[2]) 
        tcp_id = line_array[0]
        state = STATE[line_array[3]]
        uid = pwd.getpwuid(int(line_array[7]))[0]
        inode = line_array[9]
        pid = _get_pid_of_inode(inode)
        try:
            exe = os.readlink('/proc/'+pid+'/exe')
        except:
            exe = None
 
        nline = [tcp_id, uid, l_host+':'+l_port, r_host+':'+r_port, state, pid, exe]
        result.append(nline)
    return result

def netstat():
    print '%4s %s %s %s %s %s %s' % ("Id", "User".ljust(10),
                                                "Local IP:Port".ljust(20),
                                                "Remote IP:Port".ljust(20),
                                                "State".ljust(14),
                                                "Pid".ljust(8),
                                                "Executable".ljust(30))
    for conn in get_netstat():
        print '%4s %s %s %s %s %s %s' % (conn[0], conn[1].ljust(10), conn[2].ljust(20),
                                                       conn[3].ljust(20), conn[4].ljust(14),
                                                       str(conn[5]).ljust(8), str(conn[6]).ljust(30))


 
def _get_pid_of_inode(inode):
    '''
    To retrieve the process pid, check every running process and look for one using
    the given inode.
    '''
    for item in glob.glob('/proc/[0-9]*/fd/[0-9]*'):
        try:
            if re.search(inode,os.readlink(item)):
                return item.split('/')[2]
        except:
            pass
    return None
 
if __name__ == '__main__':
#    for conn in get_netstat():
#        print conn
    netstat()