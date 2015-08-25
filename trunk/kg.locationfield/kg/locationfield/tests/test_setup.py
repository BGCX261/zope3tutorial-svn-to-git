import unittest
from Products.CMFCore.utils import getToolByName

from kg.locationfield.tests.base import \
    LocationFieldTestCase


class TestSetup(LocationFieldTestCase):
    
    def afterSetUp(self):
        self.loginAsPortalOwner()
    
    def test_installerTool(self):
        tool = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(tool.isProductInstalled('PloneFormGen'),
            'PloneFormGen product is not installed.')
    
    def test_factoryTool(self):
        tool = getToolByName(self.portal, 'portal_factory')
        self.failUnless('FormLocationField' in tool._factory_types.keys(),
            'FormLocationField type is not in portal_factory tool.')
    
    def test_typesTool(self):
        tool = getToolByName(self.portal, 'portal_types')
        self.failUnless('FormLocationField' in tool.objectIds(),
            'FormLocationField type is not in portal_types tool.')
    
    def test_propertiesTool(self):
        tool = getToolByName(self.portal, 'portal_properties')
        navtree = tool.navtree_properties
        self.failUnless('FormLocationField' in navtree.metaTypesNotToList,
            'FormLocationField is not in metaTypesNotToList property.')
        site = tool.site_properties
        self.failUnless('FormLocationField' in site.types_not_searched,
            'FormLocationField is not in types_not_searched property.')
    
    def test_skinsTool(self):
        tool = getToolByName(self.portal, 'portal_skins')
        self.failUnless('locationfield' in tool.objectIds(),
            'There is no locationfield folder in portal_skins.')
        for path_id, path in tool._getSelections().items():
            layers = [l.strip() for l in path.split(',')]
            self.failUnless('locationfield' in layers,
                'locationfield layer is not registered for %s.' % path_id)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
