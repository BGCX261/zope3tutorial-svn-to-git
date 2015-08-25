
# interfaces.py
#
# This file should contain the full set of public interfaces for the project.
# These should be of use to plugin developers.

from zope.interface import Interface

class IPloneIDE(Interface):
    """This is a marker interface for the PloneIDE object."""

class IPloneIDEModel(Interface):
    """Interface to register handlers for different object types,
    e.g. 'python' for python files. Naming matches controllers on client side.

    The Interface will be located as :

        getMultiAdapter((IPloneIDE, request), IPloneIDEModel, name="python")

    """
    def handle(type_name, method_name, params):
        """
        The type_name will be the name underwhich the adapter was looked up. The
        same adapter can be registered from multiple type_names.

        The method_name is the name passed from the client, i.e. the javascript client.

        params are the parameters passed from the client
        """
