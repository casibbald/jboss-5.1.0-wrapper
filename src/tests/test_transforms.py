#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4
'''
Created on Oct 30, 2012

@author: casibbald
'''
import os
import unittest
from xml.dom.minidom import parse, parseString

from zoneconfig.impl.templates import *
from zoneconfig.impl.transform import Transform

class Test(unittest.TestCase):


    def setUp(self):
        self.T = Transform('/'.join([os.getcwd(), '..', 'tests', 'zoneconfig-metro.ini']),  '/'.join(os.path.join([os.path.expanduser('~'), 'standard-metro-config.xml'])))


    def tearDown(self):
        del self.T
    
    def test_01_find_element(self):
        attributes = {'class' : 'uk.co.bbc.fabric.common.bean.factory.config.EnvironmentPropertyPlaceholderConfigurer'}
        self.assertEqual(1, len(self.T.find_element(self.T.get_beans(self.T.top_level_bean), **attributes)))
    
    def test_02_update_managed_zone_template(self):
        attributes = {'name' : 'thumbnail-online-wip',
                  'uuid' : '12341234-1234-1234-9999-123412340001',
                  'maximumspaceallowed' : '100000000000',
                  'zonerootpath'         : '/misc/snfs/wiptest4/mediastore/thumbnail-online-wip',
                  'filesystemrootpath'  : '/misc/snfs/wiptest4',
                  'copyaffinity' : '0'}
        dom = self.T.update_managed_zone_template(**attributes)
        dom.childNodes[0].nodeValue = attributes['name']
        self.failUnlessEqual(attributes['name'], dom.childNodes[0].nodeValue)
        self.failUnlessEqual(attributes['name'], dom.childNodes[1].getAttribute('id'))
        self.failUnlessEqual(attributes['uuid'], dom.childNodes[1].childNodes[1].getAttribute('value'))
        self.failUnlessEqual(attributes['name'], dom.childNodes[1].childNodes[3].getAttribute('value'))
        self.failUnlessEqual('/misc/snfs/wiptest4/mediastore/thumbnail-online-wip', dom.childNodes[1].childNodes[5].getAttribute('value'))
        self.failUnlessEqual(attributes['maximumspaceallowed'], dom.childNodes[1].childNodes[9].getAttribute('value'))
        self.failUnlessEqual(attributes['copyaffinity'], dom.childNodes[1].childNodes[13].getAttribute('value'))
        del attributes
        
    def test_03_update_unmanaged_zone_template(self):
        attributes = {'name' : 'thumbnail-online-wip',
                  'uuid' : '12341234-1234-1234-9999-123412340001'}
        dom = self.T.update_unmanaged_zone_template(**attributes)
        self.failUnlessEqual(attributes['name'], dom.childNodes[0].getAttribute('id'))
        self.failUnlessEqual(attributes['uuid'], dom.childNodes[0].childNodes[1].getAttribute('value'))
        del attributes
        del dom

    def test_04_accessor_generators_RTMPE(self): #Issues with RTMPE Namespace
        attributes = {'name' : 'thumbnail-online-wip',
                  'uuid' : '12341234-1234-1234-9999-123412340001',
                  'maximumspaceallowed' : '100000000000',
                  'copyaffinity' : '0'}
        dom = self.T.update_accessor_generators_RTMPE(**attributes)
        self.failUnlessEqual(u'${mediastore.zone.webProxy.urlPrefix.rtmpe}/thumbnail-online-wip', dom.childNodes[0].childNodes[1].childNodes[3].getAttribute('value'))
        
        del attributes
        del dom

    def test_05_accessor_generators_NETWORK_FILE(self):
        attributes = {'name' : 'thumbnail-online-wip'}
        dom = self.T.update_accessor_generators_NETWORK_FILE(**attributes)
        self.failUnlessEqual(u'file://${mediastore.storage.dmi.essence.root.zones}/thumbnail-online-wip/', dom.childNodes[0].childNodes[1].childNodes[3].getAttribute('value'))
        
        del attributes
        del dom
        

    def test_06_accessor_generators_LOCAL_FILE(self):
        attributes = {'name' : 'thumbnail-online-wip'}
        dom = self.T.update_accessor_generators_LOCAL_FILE(**attributes)
        self.failUnlessEqual(u'file://${mediastore.storage.dmi.essence.root.zones}/thumbnail-online-wip/', dom.childNodes[0].childNodes[1].childNodes[3].getAttribute('value'))
        del attributes
        del dom

    def test_07_accessor_generators_SIGNIANT_FILE(self):
        attributes = {'name' : 'thumbnail-online-wip'}
        dom = self.T.update_accessor_generators_SIGNIANT_FILE(**attributes)
        self.failUnlessEqual(u'signiant://${java.io.tmpdir}/thumbnail-online-wip', dom.childNodes[0].childNodes[1].childNodes[3].getAttribute('value'))
        del attributes
        del dom

    def test_08_accessor_generators_SIGNIANT_FILE(self):
        attributes = {'name' : 'thumbnail-online-wip'}
        dom = self.T.update_accessor_generators_SIGNIANT_FILE(**attributes)
        self.failUnlessEqual(u'signiant://${java.io.tmpdir}/thumbnail-online-wip', dom.childNodes[0].childNodes[1].childNodes[3].getAttribute('value'))
        del attributes
        del dom

    def test_09_accessor_generators_SIGNIANT_FILE(self):
        attributes = {'name' : 'thumbnail-online-wip'}
        dom = self.T.update_accessor_generators_SIGNIANT_FILE(**attributes)
        self.failUnlessEqual(u'signiant://${java.io.tmpdir}/thumbnail-online-wip', dom.childNodes[0].childNodes[1].childNodes[3].getAttribute('value'))
        del attributes
        del dom

    def test_10_update_copy_assertion_zone_candidate_list(self):
        attributes = {'remotezonename' : '?'}
        dom = self.T.update_copy_assertion_zone_candidate_list(**attributes)
        self.failUnlessEqual('?', dom.childNodes[0].childNodes[1].getAttribute('value'))
        del attributes
        del dom
        

    def test_11_update_new_placement_actions_a(self): #TODO
        attributes = {'localzone' : 'dig-online-metro',
                      'assertiontimeoutinmins' : '2'}
        dom = self.T.update_new_placement_actions_a(**attributes)
        self.failUnlessEqual(attributes['localzone'], dom.childNodes[0].childNodes[1].getAttribute('ref'))
        self.failUnlessEqual(attributes['assertiontimeoutinmins'], dom.childNodes[0].childNodes[3].getAttribute('value'))
        del attributes
        del dom


    def test_12_update_remote_location_registry(self): #TODO
        attributes = {}
        dom = self.T.update_remote_location_registry(**attributes)
        
        del attributes
        del dom


    def test_13_update_remote_location(self):
        attributes = {'remote_location_url' : 'thumbnail-online-wip',
                      'remote_location_distance' : '10'}
        dom = self.T.update_remote_location(**attributes)
        self.failUnlessEqual(attributes['remote_location_url'], dom.childNodes[0].childNodes[1].getAttribute('value'))
        self.failUnlessEqual(attributes['remote_location_distance'], dom.childNodes[0].childNodes[3].getAttribute('value'))

        del attributes
        del dom
        

if __name__ == "__main__":
    unittest.main()
    
    

    

