# vim: tabstop=4 shiftwidth=4 softtabstop=4
import os
import unittest

from zoneconfig.impl.configuration import ConfigReader

class ConfigurationTest(unittest.TestCase):

#
# Fixture Framework
#

    def setUp(self):
        self.C = ConfigReader('/'.join([os.getcwd(), '..', 'tests', 'zoneconfig-metro.ini']))

    def tearDown(self):
        del self.C

#
# Tests
#

    def test_01_get_sections(self):
        sections = ['default', 'thumbnail-online-wip', 'web-online-wip', 'edit-online-wip', 'ava-online-wip', 
                    'dig-online-wip', 'temp-online-wip', 'jobs-unmanaged-wip', 'incoming-unmanaged-wip', 
                    'tocraft-unmanaged-wip', 'zone-ingest-xx', 'wip-configRemoteLocations']
        self.failUnlessEqual(sections, self.C.get_sections(self.C.config))

    def test_02_get_section_options(self):
        thumbnail_online_wip_options = ['zonetype', 'uuid', 'name', 'zonerootpath', 'filesystemrootpath', 'maximumspaceallowed', 
         'copyassertionzonecandidatelist', 'remotezonename', 'copyaffinity', 'newplacementactions', 
         'accessorgenerators']
        self.failUnlessEqual(thumbnail_online_wip_options, self.C.get_section_options(self.C.config, 'thumbnail-online-wip'))
        
    def test_03_has_option(self):
        self.failUnlessEqual(True, self.C.has_option(self.C.config, 'thumbnail-online-wip', 'zonetype'))

    def test_04_get_option(self):
        self.failUnlessEqual('abstractManagedZoneManager', self.C.get_option(self.C.config, 'thumbnail-online-wip', 'zonetype'))

    def test_05_get_option_single_quotes(self):
        self.failUnlessEqual('abstractManagedZoneManager', self.C.get_option(self.C.config, 'web-online-wip', 'zonetype'))

    def test_06_get_option_double_quotes(self):
        self.failUnlessEqual('abstractManagedZoneManager', self.C.get_option(self.C.config, 'edit-online-wip', 'zonetype'))

    def test_07_get_config_dictionary(self):
        one = set(self.C.get_sections(self.C.config))
        two = set(self.C.get_config_dictionary().keys())
        self.failUnlessEqual(True, one == two)
    
    

if __name__ == '__main__':
    unittest.main()
