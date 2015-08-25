UMP - User Mode Persistence
===========================

This module implements a set of hooks for implementing a persistent
object simply. The notion is that you can implement the object as a
standard Zope3 object and later implement your own persistence adapter
to manage it.

interfaces.IExternalObjectFolder
--------------------------------

This is a marker interface on the container. This interface indicates
that it supports the external object storage. The actual implementation
of that external object storage is determined by a user provided adapter.

interfaces.IExternalObject
--------------------------

This is the interface implemeneted by your adapter. You must adapt
a container and your object to provide this interface:

    queryMultiAdapter((object, container), IExternalObject)
    
folder.Folder
-------------

This is a folder which implements the IExternalObjectFolder interface.
If an adapter is provided for an object which is stored in the folder,
then it will store a reference to an external object. Otherwise it stores
the object.

folder.ExternalFolder
---------------------

This folder is intended to map a set of items where the ids are stored
externally, i.e. for mapping to a folder or database table.

folder.FolderDataManager
------------------------

This data manager is connected to the object via the Persistence class.
This object calls back to the adapter Update() method where the underlying
object has been modified in a transaction. This data manager does not
implement conflict management. The underlying object will probably be subject
to another datamanager, e.g. mapped to a relational database, so conflict
management at this level would be obsolete.

The Data manager is returned by the _DM() method on the folder, so it 
can be easily replaced on subclasses of folder.
