
from zope.interface import implements

from Products.Five.browser import BrowserView

from Products.Maps.interfaces import IMapView

from kg.locationfield.field import MyLocationField

class MapWidgetEnabled(BrowserView):
    implements(IMapView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def enabled(self):
        for field in self.context.fgFields():
            if isinstance(field, MyLocationField):
                return True
        return False

