import unittest
import transaction
from AccessControl.SecurityManagement import newSecurityManager, \
    noSecurityManager
from Testing import ZopeTestCase as ztc
from Products.CMFCore.utils import getToolByName
from  Products.PloneTestCase.layer import PloneSiteLayer

from kg.locationfield.tests.base import \
    LocationFieldTestCase


class TestErase(LocationFieldTestCase):
    # we use here nested layer for not to make an impact on
    # the rest test cases, this test case check uninstall procedure
    # thus it has to uninstall package which will be required to
    # be installed for other test cases
    class layer(PloneSiteLayer):
        @classmethod
        def setUp(cls):
            app = ztc.app()
            portal = app.plone
            
            # elevate permissions
            user = portal.getWrappedOwner()
            newSecurityManager(None, user)

            tool = getToolByName(portal, 'portal_quickinstaller')
            product_name = 'kg.locationfield'
            if tool.isProductInstalled(product_name):
                tool.uninstallProducts([product_name,])
            
            # drop elevated perms
            noSecurityManager()
            
            transaction.commit()
            ztc.close(app)
    
    def afterSetUp(self):
        self.loginAsPortalOwner()
    
    def test_factoryTool(self):
        tool = getToolByName(self.portal, 'portal_factory')
        self.failIf('FormLocationField' in tool._factory_types.keys(),
            'FormLocationField type is still in portal_factory tool.')
    
    def test_typesTool(self):
        tool = getToolByName(self.portal, 'portal_types')
        self.failIf('FormLocationField' in tool.objectIds(),
            'FormLocationField type is still in portal_types tool.')
    
    def test_propertiesTool(self):
        tool = getToolByName(self.portal, 'portal_properties')
        navtree = tool.navtree_properties
        self.failIf('FormLocationField' in navtree.metaTypesNotToList,
            'FormLocationField is still in metaTypesNotToList property.')
        site = tool.site_properties
        self.failIf('FormLocationField' in site.types_not_searched,
            'FormLocationField is still in types_not_searched property.')
    
    def test_skinsTool(self):
        tool = getToolByName(self.portal, 'portal_skins')
        self.failIf('locationfield' in tool.objectIds(),
            'There is still locationfield folder in portal_skins.')
        for path_id, path in tool._getSelections().items():
            layers = [l.strip() for l in path.split(',')]
            self.failIf('locationfield' in layers,
                'locationfield layer is still in %s.' % path_id)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestErase))
    return suite
