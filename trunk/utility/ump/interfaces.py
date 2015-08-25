
from zope.interface import Interface, Attribute

class IExternalObjectFolder(Interface):
    pass

class IExternalObject(Interface):
    """The External Object Adapter Interface"""
    def Create():
        """Create the object externally, and return the instance
        data which is required by the read method to reload it"""
    def Read(self, init_data):
        """Reload the data from the external object init data"""
    def Update(self):
        """Update the external data if changed"""
        pass
    def Delete(self):
        """Delete the external data"""
        pass

