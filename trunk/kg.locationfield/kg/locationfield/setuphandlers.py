from Products.CMFCore.utils import getToolByName

def cleanUpFactoryTool(portal):
    tool = getToolByName(portal, 'portal_factory')
    if 'FormLocationField' in tool._factory_types.keys():
        del tool._factory_types['FormLocationField']

def uninstall(context):
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile(
        'kg.locationfield_uninstall.txt') is None:
        return
    out = []
    site = context.getSite()
    cleanUpFactoryTool(site)
