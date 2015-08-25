
#   Extra area added for global navigation


from zope.viewlet.interfaces import IViewletManager
from zope.viewlet.manager import WeightOrderedViewletManager

import zope.interface

class IGlobalMenu(IViewletManager):
    "Navigation Menu Viewlet Manager"

class GlobalMenu(WeightOrderedViewletManager):
    zope.interface.implements(IGlobalMenu)
