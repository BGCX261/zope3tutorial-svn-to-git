
#   Very simple skin so that we can show our viewlets 
#   Modification of Boston for a change

import zope.interface

from zope.viewlet.interfaces import IViewletManager, IViewlet
from zope.viewlet.manager import ConditionalViewletManager
from zope.app.boston import Boston

import z3c.layer.pagelet
import z3c.form.interfaces
import z3c.formui.interfaces

from layer import IPageletLayer

class ISkin(
    IPageletLayer,
    Boston,
    z3c.formui.interfaces.IDivFormLayer
):
    pass


class IListingHeadshot(IViewletManager):
    "Headshot on Listings"

class ListingHeadshot(ConditionalViewletManager):
    zope.interface.implements(IListingHeadshot)
