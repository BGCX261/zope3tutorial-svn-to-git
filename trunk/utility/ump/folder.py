
#   Simple folder implementation
#
#   The folder must provide the standard folder services
#   However, when an object is referenced that is not in
#   memory, the folder will attempt to load it

#   Note on caching - this module piggybacks on the ZODB
#   cache. When ZODB cache is cleared (i.e. reload) these
#   objects will be recycled. 

import sys, time

import transaction
from persistent import Persistent

from zope.interface import Interface, implements, alsoProvides
from zope.component import adapts, queryMultiAdapter
from zope.location.interfaces import ILocation
from zope.exceptions import DuplicationError
from zope.publisher.interfaces import NotFound


from zope.app.folder import folder
from zope.app.container.contained import setitem, uncontained

from interfaces import IExternalObjectFolder, IExternalObject

ECHO=False

#-----------------------------------------------------------------------------------
class FolderDataManager:
    """This is a simple DataManager. It's purpose is to call the adapter
    to call its update method if an attribute is modified. I am using this
    to trigger calls to the SQL database, so I expect that second transaction
    manager to manage the conflicts etc.

    It would be useful for alternative deployments to allow this datamanager
    to be easily pluggable
    """

    transactions={}
    
    def abort(self, transaction):
        pass

    def tpc_begin(self, transaction):
        pass

    def commit(self, transaction):
        pass

    def onBeforeCommit(self, transaction):
        """This handler is called before the commit. It executes the
        update actions for any updated objects. It must be called 
        before the commit or vote since it may cause a new transaction
        handler to join the transaction"""

        try:
            changed_objects = self.transactions[transaction]
        except:
            return

        for o in changed_objects:
            adapter = o._v_external_object_adapter
            adapter.Update()
            o._p_changed = False

    def tpc_vote(self, transaction):
        pass

    def tpc_finish(self, transaction):
        del self.transactions[transaction]

    def tpc_abort(self, transaction):
        try:
            changed_objects = self.transactions[transaction]
        except:
            return

        for o in changed_objects:
            ref = o._v_external_object_reference
            ref._v_realInstance = None # orphan it

    def sortKey(self):
        return 1

    def register(self, object):
        """Register an object with the data manager - in theory
        this should be called by the persistent module when the 
        object is changed"""

        txn = transaction.get()
        if txn not in self.transactions:
            self.transactions[txn] = []
            txn.join(self)
            txn.addBeforeCommitHook(self.onBeforeCommit, args=(txn,))

        self.transactions[txn].append(object)

#-----------------------------------------------------------------------------------
# Simple data manager for basic use. Replace this on your subclass of one of the folders
# below.
_gFDM=FolderDataManager()

#-----------------------------------------------------------------------------------
class Broken(object):
    """A class to be returned if the object cannot be imported"""
    # TODO

#-----------------------------------------------------------------------------------
# This ObjectReference is used for transient objects. Here the key is not
# stored on the database.
class TransientObjectReference(object):
    """This is the actual reference to the object which is stored
    in the Folder, where they persistence is managed externally"""

    modulename = None
    globalname = None
    init_data = None

    def __init__(self, modulename, globalname, container, name, init_data):
        """Create the initial reference. This is only called when the
        object is added to the folder"""
        self.modulename = modulename
        self.globalname = globalname

        # Copy location information
        self.__parent__ = container
        self.__name__ = str(name)

        self.init_data = init_data

    def delInst(self):
        """Delete the object"""
        self._v_external_object_adapter.Delete()

    def setInst(self, inst, name):
        """Set the instance object"""

        # Locate it
        inst.__name__ = self.__name__
        inst.__parent__ = self.__parent__
        alsoProvides(inst, ILocation)

        # Now need to get an adapter 
        adapter = queryMultiAdapter((inst, self.__parent__), IExternalObject)

        if adapter is None:
            print 'could not load source for ', self.modulename, self.globalname
            return

        inst._v_external_object_reference = self
        inst._v_external_object_adapter = adapter
        self._v_external_object_adapter = adapter
        self._v_realInstance = inst

        # Connect to data manager
        inst._p_jar = self.__parent__._DM()

        # Trigger the create method on the adapter
        self._v_external_object_adapter.Create(name=name)
        
    def getInst(self):
        """broken.py in the ZODB is the key point for creating
        objects - this is it's approach"""

        if hasattr(self, '_v_realInstance'):
            if self._v_realInstance is not None:
                return self._v_realInstance

        klass = None
        try:
            __import__(self.modulename)
        except ImportError:
            pass
        else:
            module = sys.modules[self.modulename]
            try:
                klass = getattr(module, self.globalname)
            except AttributeError:
                pass

        if klass is None:
            print 'could not load source for ', self.modulename, self.globalname
            return Broken()

        inst = klass.__new__(klass)
        if ECHO: print '***** Created object ****', inst

        # Locate it
        inst.__name__ = str(self.__name__)
        inst.__parent__ = self.__parent__
        alsoProvides(inst, ILocation)

        # Now need to get an adapter 
        adapter = queryMultiAdapter((inst, self.__parent__), IExternalObject)

        if adapter is None:
            print 'could not load source for ', self.modulename, self.globalname
            return Broken()

        inst._v_external_object_reference = self
        inst._v_external_object_adapter = adapter
        self._v_external_object_adapter = adapter
        self._v_realInstance = inst

        # Initialise the data
        self._v_external_object_adapter.Read(self.init_data)

        # Connect to data manager
        inst._p_jar = self.__parent__._DM()

        # Return the class
        return self._v_realInstance

# This must subclass Persistent or the _v_ attributes are stored.
class ObjectReference(Persistent, TransientObjectReference):
    """This is the actual reference to the object which is
    stored in the Folder, where they persistence is managed
    externally"""
    modulename = None
    globalname = None
    init_data = None

    def __init__(self, context, container, adapter):
        """Create the initial reference. This is only called when the
        object is added to the folder"""
        self.modulename = context.__class__.__module__
        self.globalname = context.__class__.__name__
        context._v_external_object_reference = self
        context._v_external_object_adapter = adapter
        self._v_external_object_adapter = adapter
        self._v_realInstance = context

        # Copy location information
        self.__parent__ = context.__parent__
        self.__name__ = str(context.__name__)

        # Connect to data manager
        context._p_jar = self.__parent__._DM()

        # self.init_data is initialised by Create()
        self.init_data = adapter.Create()

#-----------------------------------------------------------------------------------
class Folder(folder.Folder):
    """A Folder which handles the User Mode Peristence.
    
        The mapped object is either a standard Zope object
        or it is a reference to an object whos persistence is
        managed by the application
    """

    # Marker interface for adapter
    implements(IExternalObjectFolder)

    def _DM(self):
        """Return the data manager object"""
        return _gFDM

    def incarnate_object(self, reference):
        """Given the ObjectReference, return an object"""
        if ECHO: print 'Folder:incarnate_object', reference

        if type(reference) != ObjectReference:   # Just a stored object
            return reference

        return reference.getInst()

    def object_toStoredForm(self, object):
        """Given an object, either do user mode persistence and
        return a reference or return the object"""
        if ECHO: print 'Folder:toStoredForm', object

        if hasattr(object, '_v_external_object_reference'): # Already bound
            return object._v_external_object_reference

        # Is there an adapter for it
        rv = queryMultiAdapter((object, self), IExternalObject)
        if rv is not None:
            # This is a create - if the object had been loaded from the
            # database it would already have an __v_external_object_reference
            reference = ObjectReference(object, self, rv)
            return reference

        # Default - just store the object
        return object

    def values(self):
        """Return a sequence-like object containing the objects that
           appear in the folder.
        """
        if ECHO: print 'Folder:values'
        for val in self.data.values():
            yield self.incarnate_object(val)

    def items(self):
        """Return a sequence-like object containing tuples of the form
           (name, object) for the objects that appear in the folder.
        """
        if ECHO: print 'Folder:items'
        for (k,v) in self.data.items():
            yield(k, self.incarnate_object(v))

    def __getitem__(self, name):
        """Return the named object, or raise ``KeyError`` if the object
           is not found.
        """
        if ECHO: print 'Folder:__getitem__', name

        obj = self.data[name]
        rv = self.incarnate_object(obj)
        if ECHO: print 'Folder:__getitem__ returning ',rv
        return rv

    def get(self, name, default=None):
        """Return the named object, or the value of the `default`
           argument if the object is not found.
        """
        if ECHO: print 'Folder:get', name

        obj =  self.data.get(name, default)
        return self.incarnate_object(obj)

    def __setitem__(self, name, object):
        """Add the given object to the folder under the given name."""
        if ECHO: print 'Folder:setitem'

        if not (isinstance(name, str) or isinstance(name, unicode)):
            raise TypeError("Name must be a string rather than a %s" %
                            name.__class__.__name__)
        try:
            unicode(name)
        except UnicodeError:
            raise TypeError("Non-unicode names must be 7-bit-ascii only")
        if not name:
            raise TypeError("Name must not be empty")

        if name in self.data:
            raise DuplicationError("name, %s, is already in use" % name)

        # TODO: need to change setitem so that events are fired for the object,
        #       not the object stored form - override the __setitem__ method of self.data
        setitem(self, self.set_data_item, name, object)

    def set_data_item(self, name, object):
        if ECHO: print 'Folder:set_data_item'
        newobj = self.object_toStoredForm(object)
        self.data.__setitem__(name, newobj)

    def __delitem__(self, name):
        """Delete the named object from the folder. Raises a KeyError
           if the object is not found."""
        if ECHO: print 'Folder:__delitem__'

        # Have to pull in the object to make this happen
        object = self.get(name)
        if hasattr(object, '_v_external_object_reference'): 
            object._v_external_object_reference.delInst()
            object._v_external_object_reference = None

        try:
            uncontained(self.data[name], self, name)
        except:
            pass
        del self.data[name]

    def clear_cache(self):
        """For test purposes"""
        for ref in self.data.values():
            if ref is not None and hasattr(ref, _v_realInstance):
                ref._v_realInstance = None # orphan it

class ExternalFolder(folder.Folder):
    """This folder should not have a persistent data attribute. The
    keys are retrieved from an external location, i.e. a database
    table primary keys.

    The storage should be efficiently mapped, i.e. inserts/deletes
    should log to an external table to track modification date/time.
    Assumes the row modifications do not change the primary key

    Subclass must set up the modulename, globalname and reload

    Note: Externally keys are strings, internally they are integers
    """

    # Marker interface for adapter
    implements(IExternalObjectFolder)

    modulename=None # Set by inheritance
    globalname=None

    def _DM(self):
        """Return the data manager object"""
        return _gFDM

    def need_reload(self):
        """Default - reload after 2 minutes. If mapped to a relational
        database, underlying table should utilitise triggers on insert/delete
        to track table modification times to allow this to me more efficient"""

        try:
            last_load_time = self._v_last_load_time
        except:
            return True

        age = time.time() - last_load_time
        if age > 120:
            return True

        return False

    def reload(self):
        """Reload the underlying data. Return a list of primary keys"""
        raise NotImplemented, 'reload'

    def verify_data(self):
        """Ensure that the _v_data is setup"""
        if not hasattr(self, '_v_data'):
            self._v_data = {}
            data_list = self.reload()
            for k in [int(k) for k in data_list]:
                self._v_data[k] = None
            self._v_last_load_time = time.time()
            return
        if self.need_reload():
            data_list = self.reload()
            """Use sets to find items added and removed"""
            old_keys = set(self._v_data.keys())
            new_keys = set([int(k) for k in data_list])
            for k in old_keys - new_keys:
                del self._v_data[k]
            for k in new_keys - old_keys:
                self._v_data[k] = None
            self._v_last_load_time = time.time()

    def incarnate_object(self, key):
        """Given the ObjectReference, return an object"""
        if ECHO: print 'ExternalFolder:incarnate_object', key
        self.verify_data()

        try:
            key = int(key)
        except:
            raise KeyError, key
        
        # If the object is not in the _v_data, check the database
        # directly again. This will add it into the _v_data if it exists
        try:
            reference = self._v_data[key]
        except:
            reference = None

        if reference is None:
            try:
                reference = TransientObjectReference(self.modulename,
                    self.globalname, self, key, key)
                self._v_data[int(key)] = reference
            except:
                raise KeyError, key

        reference = self._v_data[int(key)]
        return reference.getInst()

    def values(self):
        """Return a sequence-like object containing the objects that
           appear in the folder.
        """
        if ECHO: print 'ExternalFolder:values'
        self.verify_data()

        for key in self._v_data.keys():
            yield self.incarnate_object(val)

    def items(self):
        """Return a sequence-like object containing tuples of the form
           (name, object) for the objects that appear in the folder.
        """
        if ECHO: print 'ExternalFolder:items'
        self.verify_data()

        for k in self._v_data.keys():
            yield(str(k), self.incarnate_object(k))

    def __getitem__(self, name):
        """Return the named object, or raise ``KeyError`` if the object
           is not found.
        """
        if ECHO: print 'ExternalFolder:__getitem__', name

        rv = self.incarnate_object(name)
        if ECHO: print 'ExternalFolder:__getitem__ returning ',rv
        return rv

    def get(self, name, default=None):
        """Return the named object, or the value of the `default`
           argument if the object is not found.
        """
        if ECHO: print 'ExternalFolder:get', name

        try:
            return self.incarnate_object(name)
        except:
            return default

    def __setitem__(self, name, object):
        """Add the given object to the folder under the given name.
        Note, the map is from ids to reference objects, not actual objects."""
        if ECHO: print 'ExternalFolder:setitem'

        self.verify_data()

        reference = TransientObjectReference(self.modulename,
            self.globalname, self, name, name)
        reference.setInst(object, name)
        self._v_data[int(name)] = reference

    def __delitem__(self, name):
        """Delete the named object from the folder. Raises a KeyError
           if the object is not found."""
        if ECHO: print 'ExternalFolder:__delitem__'
        self.verify_data()

        reference = self._v_data[int(name)]

        # Trigger the delete method on the adapter
        reference.delInst()

        del self._v_data[int(name)]

    def __len__(self):
        self.verify_data()
        return len(self._v_data)

    def clear_cache(self):
        """For test purposes"""
        for ref in self._v_data.values():
            if ref is not None and hasattr(ref, '_v_realInstance'):
                ref._v_realInstance = None # orphan it
