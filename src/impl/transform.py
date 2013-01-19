#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
'''
Created on Oct 30, 2012

@author: casibbald
'''
import os
from pprint import pprint
from xml.dom.minidom import parse, parseString, Document

from zoneconfig.impl.templates import *
from zoneconfig.impl.configuration import ConfigReader


class ERRORBeanNotFound(Exception):
    pass


class Transform(object):
    def __init__(self, source_ini, to_file):
        self.dom = None
        self.top_level_bean = None
        self.set_template()
        self.set_top_level_bean()
        self.to_file = to_file
        self.C = ConfigReader(source_ini)
        
    def set_template(self):
        self.dom=parseString(base_template)
    
    def set_top_level_bean(self):
        self.top_level_bean = self.dom.childNodes[0]

    def read_template(self, template_type, template):
        if template_type == 'string':
            return parseString(template)
        elif template_type == 'file':
            if os.path.exists(template):
                return parse(template)

    def write_xml(self, dom, to_file):
        if os.path.exists(os.path.dirname(to_file)):
            try:
                f = open(to_file, 'w')
                f.write(dom.toxml())
                f.close()
            except Exception, e:
                print Exception, e
                

    def append_node(self, node):
        pass

    def get_elements(self, element_type, Node):
        element_list = []
        for element in Node.childNodes:
            if element.nodeName == element_type:
                element_list.append(element)
        return element_list

    def get_sub_nodes(self, node, node_type):
        """ Given a bean, return a list of any child beans
        >>> self.get_sub_nodes(self.top_level_bean, 'bean')
        [<DOM Element: bean at 0x103c3c998>, <DOM Element: bean at 0x103c40908>, 
        <DOM Element: bean at 0x103c40ef0>, <DOM Element: bean at 0x103c7b1b8>, 
        <DOM Element: bean at 0x103c7b710>, <DOM Element: bean at 0x103c7bd88>, 
        <DOM Element: bean at 0x103c7c320>, <DOM Element: bean at 0x103c7d3b0>]
        
        >>> self.get_sub_nodes(self.get_sub_nodes(self.top_level_bean, 'bean')[0], 'property')
        [<DOM Element: property at 0x103c3cc20>, <DOM Element: property at 0x103c3cea8>, 
        <DOM Element: property at 0x103c40170>]
        """
        node_list = []
        for element in node.childNodes:
            if element.nodeName == node_type:
                node_list.append(element)
        return node_list
    
    def get_beans(self, bean):
        """ Given a bean, return a list of any child beans
        >>> self.get_beans(self.top_level_bean)[-1].getAttribute('class')
        [<DOM Element: bean at 0x10d061908>, <DOM Element: bean at 0x10d065878>, 
         <DOM Element: bean at 0x10d065e60>, <DOM Element: bean at 0x10d0a0128>, 
         <DOM Element: bean at 0x10d0a0680>, <DOM Element: bean at 0x10d0a0cf8>, 
         <DOM Element: bean at 0x10d0a1290>, <DOM Element: bean at 0x10d0a2320>]
        
        >>> self.get_beans(self.top_level_bean)[-1].getAttribute('class')
        u'uk.co.bbc.fabric.mi.mediastore.zone.LocalFSUnmanagedZoneManager'
        """
        bean_list = []
        for node in bean.childNodes:
            if node.nodeName == 'bean':
                bean_list.append(node)
        return bean_list

    #Need to consider merging the following two class methods into a single one that handles either beans or properties 
    def find_element(self, nodes, **kwargs):
        """Returns a list of beans that match the defined attributes
        >>> kwargs = {'id': u'abstractUnmanagedZoneManager', 'abstract': u'true', 'class': u'uk.co.bbc.fabric.mi.mediastore.zone.LocalFSUnmanagedZoneManager'}
        >>> self.find_element(self.get_beans(self.top_level_bean), **kwargs)
        [<DOM Element: bean at 0x10f378830>, <DOM Element: bean at 0x10f379440>, <DOM Element: bean at 0x10f37a4d0>, 
         <DOM Element: bean at 0x10f37a4d0>, <DOM Element: bean at 0x10f37a4d0>]
        """
        element_list = []
        for element in nodes:
            validity = None
            for key in kwargs:
                if validity != False and element.getAttribute(key) == kwargs[key]:
                    validity = True
                    element_list.append(element)
                else:
                    validity = False
        return element_list

    def update_managed_zone_template(self, **kwargs):
        dom = self.read_template('string', managed_zone_template)
        if kwargs.has_key('name'):
            dom.childNodes[0].nodeValue = kwargs['name']
            dom.childNodes[1].setAttribute('id', kwargs['name']) #ID
            dom.childNodes[1].childNodes[3].setAttribute('value', kwargs['name']) #NAME
            
        if kwargs.has_key('zonerootpath'):
            dom.childNodes[1].childNodes[5].setAttribute('value', kwargs['zonerootpath'])
        
        if kwargs.has_key('filesystemrootpath'):
            dom.childNodes[1].childNodes[7].setAttribute('value', kwargs['filesystemrootpath'])
        
        if kwargs.has_key('uuid'):
            dom.childNodes[1].childNodes[1].setAttribute('value', kwargs['uuid']) #UUID
        
        if kwargs.has_key('maximumspaceallowed'):
            dom.childNodes[1].childNodes[9].setAttribute('value', kwargs['maximumspaceallowed']) #MAXIMUMSPACEALLOWED
        if kwargs.has_key('copyaffinity'):
            dom.childNodes[1].childNodes[13].setAttribute('value',kwargs['copyaffinity']) #COPYAFFINITY
        
        return dom
        
    def update_unmanaged_zone_template(self, **kwargs):
        dom = self.read_template('string', unmanaged_zone_template)
        if kwargs.has_key('name'):
            dom.childNodes[0].setAttribute('id', kwargs['name'])
            dom.childNodes[0].childNodes[3].setAttribute('value', kwargs['name'])
            
        if kwargs.has_key('zonerootpath'):
            dom.childNodes[0].childNodes[5].setAttribute('value', kwargs['zonerootpath'])
        
        if kwargs.has_key('filesystemrootpath'):
            dom.childNodes[0].childNodes[7].setAttribute('value', kwargs['filesystemrootpath'])
            
        if kwargs.has_key('uuid'):                
            dom.childNodes[0].childNodes[1].setAttribute('value', kwargs['uuid'])
        
        return dom
    
    def update_accessor_generators_RTMPE(self, **kwargs): #Issues with RTMPE Namespace
        dom = self.read_template('string', accessor_generators['RTMPE'])
        dom.childNodes[0].childNodes[1].childNodes[3].setAttribute('value', '/'.join([dom.childNodes[0].childNodes[1].childNodes[3].getAttribute('value'), kwargs['name']]))
        return dom

    
    def update_accessor_generators_NETWORK_FILE(self, **kwargs):
        dom = self.read_template('string', accessor_generators['NETWORK_FILE'])
        split_values = dom.childNodes[0].childNodes[1].childNodes[3].getAttribute('value').split('/')
        split_values[3] = kwargs['name']
        dom.childNodes[0].childNodes[1].childNodes[3].setAttribute('value', '/'.join([split_values[0], '', split_values[2], split_values[3], '']))
        return dom
    
    def update_accessor_generators_LOCAL_FILE(self, **kwargs):
        dom = self.read_template('string', accessor_generators['LOCAL_FILE'])
        split_values = dom.childNodes[0].childNodes[1].childNodes[3].getAttribute('value').split('/')
        split_values[3] = kwargs['name']
        dom.childNodes[0].childNodes[1].childNodes[3].setAttribute('value', '/'.join([split_values[0], '', split_values[2], split_values[3], '']))
        
        return dom

    def update_accessor_generators_SIGNIANT_FILE(self, **kwargs):
        dom = self.read_template('string', accessor_generators['SIGNIANT_FILE'])
        split_values = dom.childNodes[0].childNodes[1].childNodes[3].getAttribute('value').split('/')
        split_values[3] = kwargs['name']
        dom.childNodes[0].childNodes[1].childNodes[3].setAttribute('value', '/'.join([split_values[0], '', split_values[2], split_values[3]]))

        return dom

    def update_accessor_generators_HTTP(self, **kwargs):
        dom = self.read_template('string', accessor_generators['HTTP'])
        dom.childNodes[0].childNodes[1].childNodes[3].setAttribute('value', kwargs['accessorGenerators_HTTP_url'])
        
        return dom

    def update_accessor_generators_HTTPS(self, **kwargs):
        dom = self.read_template('string', accessor_generators['HTTPS'])
        dom.childNodes[0].childNodes[1].childNodes[3].setAttribute('value', kwargs['accessorGenerators_HTTPS_url'])
        
        return dom


    def update_copy_assertion_zone_candidate_list(self, **kwargs):
        dom = self.read_template('string', copy_assertion_zone_candidate_list)
        dom.childNodes[0].childNodes[1].setAttribute('value', kwargs['remotezonename'])
        
        return dom

    def update_new_placement_actions(self):
        return self.read_template('string', new_placement_actions)
        

    def update_new_placement_actions_a(self, **kwargs): #TODO 
        dom = self.read_template('string', new_placement_actions_a)
        if kwargs.has_key('localzone'):
            dom.childNodes[0].childNodes[1].setAttribute('ref', kwargs['localzone'])
        if kwargs.has_key('assertiontimeoutinmins'):
            dom.childNodes[0].childNodes[3].setAttribute('value', kwargs['assertiontimeoutinmins'])
        
        return dom
    
    def update_remote_location_registry(self):
        dom = self.read_template('string', remote_location_registry)
        
        return dom

    def update_remote_location(self, **kwargs):
        dom = self.read_template('string', remote_location)
        dom.childNodes[0].childNodes[1].setAttribute('value', kwargs['remote_location_url'])
        dom.childNodes[0].childNodes[3].setAttribute('value', kwargs['remote_location_distance'])
        
        return dom

    def insert_managed_zone_templates(self):
        print self.dom.toxml()

    def transform_managed_zone_templates(self):
        config = self.C.get_config_dictionary()
        zones = [x for x in config.keys() if x != 'default' and config[x].has_key('zonetype') and config[x]['zonetype']=='abstractManagedZoneManager']
        zone_doms = []
        #Transform base managed zone template
        for zone in zones:
            insert_zone = self.update_managed_zone_template(**config[zone])
            if config[zone].has_key('copyassertionzonecandidatelist'):
                if config[zone]['copyassertionzonecandidatelist'] == 'True':   #True is quoted as config does not return a real boolean object! so must handle this way.
                    list_element = self.get_sub_nodes(self.find_element(self.get_sub_nodes(insert_zone.childNodes[1], 'property'), name=u'copyAssertionZoneCandidateList')[0], 'list')[0] 
                    copyassertionzonecandidatelist = self.update_copy_assertion_zone_candidate_list(**config[zone])
                    self.get_sub_nodes(self.find_element(self.get_sub_nodes(insert_zone.childNodes[1], 'property'), name=u'copyAssertionZoneCandidateList')[0], 'list')[0].insertBefore(copyassertionzonecandidatelist.childNodes[0], None)
            
            if config[zone].has_key('newplacementactions'):
                if config[zone]['newplacementactions'] == 'True':
                    newplacementactions = self.update_new_placement_actions()
                    insert_zone = self.update_managed_zone_template(**config[zone])
                    newplacementactions_a = self.update_new_placement_actions_a(**config[zone])
                    list_element = self.get_sub_nodes(newplacementactions.childNodes[0], 'list')[0]
                    list_element.insertBefore(newplacementactions_a.childNodes[0], None)
                    insert_zone.childNodes[1].insertBefore(newplacementactions.childNodes[0], None)
            
            if config[zone].has_key('accessorgenerators'):
                accessorgenerator_list = [x.split()[0] for x in config[zone]['accessorgenerators'].split(',') ]
                for accessor in accessorgenerator_list:
                    if accessor == 'LOCAL_FILE':
                        accessordom = self.update_accessor_generators_LOCAL_FILE(**config[zone])    
                        map = self.get_sub_nodes(self.find_element(self.get_sub_nodes(insert_zone.childNodes[1], 'property'), name="accessorGenerators")[0], 'map')[0]
                        map.insertBefore(accessordom.childNodes[0], None)
                    elif accessor == 'SIGNIANT_FILE':
                        accessordom = self.update_accessor_generators_SIGNIANT_FILE(**config[zone])
                        map = self.get_sub_nodes(self.find_element(self.get_sub_nodes(insert_zone.childNodes[1], 'property'), name="accessorGenerators")[0], 'map')[0]
                        map.insertBefore(accessordom.childNodes[0], None)
                    elif accessor == 'NETWORK_FILE':
                        accessordom = self.update_accessor_generators_NETWORK_FILE(**config[zone])
                        map = self.get_sub_nodes(self.find_element(self.get_sub_nodes(insert_zone.childNodes[1], 'property'), name="accessorGenerators")[0], 'map')[0]
                        map.insertBefore(accessordom.childNodes[0], None)
                    elif accessor == 'RTMPE':
                        accessordom = self.update_accessor_generators_RTMPE(**config[zone])
                        #accessordom.toxml()
                        pass
                    
            zone_doms.append(insert_zone)
            
        for zone in zone_doms:
            self.dom.childNodes[0].insertBefore(zone.childNodes[1], self.dom.childNodes[0].childNodes[-4])


    def transform_unmanaged_zone_templates(self):
        config = self.C.get_config_dictionary()
        zones = [x for x in config.keys() if x != 'default' and config[x].has_key('zonetype') and config[x]['zonetype']=='abstractUnmanagedZoneManager']
        zone_doms = []
        for zone in zones:
            insert_zone = self.update_unmanaged_zone_template(**config[zone])
            zone_doms.append(insert_zone)
            
        for zone in zone_doms:
            self.dom.childNodes[0].insertBefore(zone.childNodes[0], self.dom.childNodes[0].childNodes[-4])

    
    def transform_ZoneList(self, list):
        if list == 'managedZoneList':
            beans = [bean for bean in self.get_sub_nodes(self.dom.childNodes[0], 'bean') if bean.getAttribute('parent')=='abstractManagedZoneManager']
            attributes = {'id':'managedZoneList'}
        elif list == 'unmanagedZoneList':
            beans = [bean for bean in self.get_sub_nodes(self.dom.childNodes[0], 'bean') if bean.getAttribute('parent')=='abstractUnmanagedZoneManager']
            attributes = {'id':'unmanagedZoneList'}

        for bean in beans:
            element = self.dom.createElement('ref')
            element.setAttribute('local', bean.getAttribute('id'))
            self.find_element(self.get_sub_nodes(self.dom.childNodes[0], 'util:list'), **attributes)[0].insertBefore(element, self.find_element(self.get_sub_nodes(self.dom.childNodes[0], 'util:list'), **attributes)[0].lastChild)


    def transform_remote_locations(self):
        remotelocationregistry = self.update_remote_location_registry()
        config = self.C.get_config_dictionary()
        list_element = self.get_sub_nodes(remotelocationregistry.childNodes[0], 'util:list')[0]
        if config.has_key('wip-configRemoteLocations'): 
            section = config['wip-configRemoteLocations']
        elif config.has_key('metro-configRemoteLocations'):
            section = config['metro-configRemoteLocations']
         
        for value in section:
            items = [x.split()[0] for x in section['{0}'.format(value)].split(',')]
            url = items[0]
            distance = items[1]
            attributes = {'remote_location_url': url, 'remote_location_distance': distance}
            updateremotelocation = self.update_remote_location(**attributes)
            list_element.insertBefore(updateremotelocation.childNodes[0], None)
        self.write_xml(remotelocationregistry, os.path.join(os.path.dirname(self.to_file), 'mediastore-remotelocations-config.xml'))
        
        
        

def generate_xml(source_ini,  to_file):
    T = Transform(source_ini,  to_file)

    T.transform_managed_zone_templates()
    T.transform_ZoneList('managedZoneList')
    
    T.transform_unmanaged_zone_templates()
    T.transform_ZoneList('unmanagedZoneList')
    
    T.transform_remote_locations()

    T.write_xml(T.dom, T.to_file)


if __name__ == '__main__':
    T = Transform('/'.join([os.getcwd(), '..', 'tests', 'zoneconfig-metro.ini']),  '/'.join(os.path.join([os.path.expanduser('~'), 'standard-metro-config.xml'])))
    #generate_xml('/'.join([os.getcwd(), '..', 'tests', 'zoneconfig-metro.ini']),  '/'.join(os.path.join([os.path.expanduser('~'), 'standard-metro-config.xml'])))



