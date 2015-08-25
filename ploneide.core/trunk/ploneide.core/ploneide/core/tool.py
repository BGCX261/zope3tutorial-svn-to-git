
"""
    This is the portal_ploneide which is created in the root of the plone site.
"""

from zope.interface import implements
from OFS.SimpleItem import SimpleItem

from ploneide.core import IPloneIDE

class PloneIDE(SimpleItem):
    """This should be installed as a Tool by plone"""
    implements(IPloneIDE)


