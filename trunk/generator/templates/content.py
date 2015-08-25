
from templet import stringfunction

@stringfunction
def GenFile(DSLModel, Table, View):
    """
from persistent import Persistent

from zope.component import adapts
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

from zope.dublincore.zopedublincore import ZopeDublinCore
from zope.dublincore.interfaces import IZopeDublinCore

from zope.app.container.contained import NameChooser

from utility.ump.folder import ExternalFolder

from ${DSLModel['GENERAL']['target_folder']}.${Table['name']} import MessageFactory as _

from interfaces import ${View.interface_name}, ${View.interface_name}Container
import ${Table['name']}_db

class ${Table['name']}Base(Persistent):
    implements(${View.interface_name})

${{
    for column in Table['columns']:
        if column['colname'] == View.primary_key: continue
        out.append("\t%s = FieldProperty(%s['%s'])\\n" % (column['colname'], View.interface_name,
            column['colname']))
}}

class ${Table['name']}ContainerBase(ExternalFolder):
    implements(${View.interface_name}Container)

    modulename='tables.${View.TableName}.${View.TableName}_content'
    globalname='${View.TableName}'

    def reload(self):
        table = ${View.TableName}_db.${View.TableName}(self)
        cursor = table.Keys()
        return [str(row.${View.primary_key}) for row in cursor]


class ${View.TableName}_dublincoreBase(ZopeDublinCore):
    adapts(${View.interface_name})
    implements(IZopeDublinCore)

    def initialiseData(self, dcdata):
        dcdata['Title'] = [self.context.__name__]
        dcdata['Description'] = [self.context.__name__]

    def __init__(self, context):
        self.context = context
        dcdata = {}
        self.initialiseData(dcdata)
        ZopeDublinCore.__init__(self, dcdata)

class ${View.TableName}ContainerNameChooserBase(NameChooser):
    "Name chooser which forces integers"

    adapts(${View.interface_name}Container)

    def checkName(self, name, object):
        "Rule - valid integer"
        i = int(name)

    def chooseName(self, name, object):
        table = ${View.TableName}_db.${View.TableName}(self.context)
        return '%d'%(table.NextPrimaryKey()[0].${View.primary_key})

# CAN_EDIT_AFTER_THIS_LINE

${{
for classname in View.classnames:
    out.append('class %s(%sBase):\\n' % (classname, classname))
    out.append('\tpass\\n\\n')
}}
"""


@stringfunction
def GenConfiguration(DSLModel, Table, View):
    """
<!-- Content Configuration -->

    <class class=".${View.TableName}_content.${View.TableName}"> 
        <require
            permission="zope.View"
            interface=".interfaces.${View.interface_name}" 
            />
        <require
            permission="zope.ManageContent"
            set_schema=".interfaces.${View.interface_name}" 
            />
    </class>

    <class class=".${View.TableName}_content.${View.TableName}Container">
        <require
            permission="zope.View"
            interface="zope.app.container.interfaces.IReadContainer"
            />
        <require
            permission="zope.ManageContent"
            interface="zope.app.container.interfaces.IWriteContainer"
            />
        <implements
            interface="zope.annotation.interfaces.IAttributeAnnotatable"
            />
    </class>

    <browser:addMenuItem
        title="${View.TableName} Container"
        class=".${View.TableName}_content.${View.TableName}Container"
        permission="zope.ManageContent"
        />

    <class class=".${View.TableName}_content.${View.TableName}_dublincore">
        <require
            permission="zope.View"
            interface="zope.dublincore.interfaces.IZopeDublinCore"
            />
    </class>

    <adapter
        factory=".${View.TableName}_content.${View.TableName}_dublincore"
        provides="zope.dublincore.interfaces.IZopeDublinCore"
        for=".interfaces.${View.interface_name}"
        trusted="True"
        />

    <adapter
        factory=".${View.TableName}_storage.${View.TableName}_Storage"
        />

    <adapter
        factory=".${View.TableName}_content.${View.TableName}ContainerNameChooser"
        />

"""


@stringfunction
def GenStorageFile(DSLModel, Table, View):
    """
from zope.interface import implements
from zope.component import adapts
from zope.publisher.interfaces import NotFound

from utility.ump.interfaces import IExternalObject

from schema_helpers import Bool_toStorage, Bool_fromStorage, List_toStorage, \\
    List_fromStorage, BinaryToBase64_toStorage, BinaryToBase64_fromStorage

from ${DSLModel['GENERAL']['target_folder']}.${Table['name']} import MessageFactory as _

from interfaces import ${View.interface_name}, ${View.interface_name}Container
import ${Table['name']}_db

class ${Table['name']}_StorageBase(object):

    adapts(${View.interface_name}, ${View.interface_name}Container)
    implements(IExternalObject)

    def __init__(self, context, container):
        self.context = context
        self.container = container
        self.table = ${Table['name']}_db.${Table['name']}(self.context)

    def ContextToStorage(self, data):
        "Save the context object to the data object passed in"
${{
    for column in Table['columns']:
        if column['colname'] == View.primary_key: continue
        mapping_type = column.get('mapping_type', None)
        if mapping_type is None:
            out.append("\t\tdata['%s'] = self.context.%s\\n" % (column['colname'],column['colname']))
        else:
            out.append("\t\tdata['%s'] = %s_toStorage(self.context.%s)\\n" % (column['colname'],
                mapping_type, column['colname']))
}}

    def StorageToContext(self, row):
        "Save the storage (database row) to the context object"
${{
    for column in Table['columns']:
        if column['colname'] == View.primary_key: continue
        mapping_type = column.get('mapping_type', None)
        if mapping_type is None:
            mapped = 'row.%s' % column['colname']
        else:
            mapped = '%s_fromStorage(row.%s)' % (mapping_type, column['colname'])
        schema_type = column.get('schema_type', 'TextLine')
        if schema_type == 'schema.Set':
            mapped = 'set(%s)' % mapped
        out.append("\t\tself.context.%s = %s\\n" % (column['colname'], mapped))
}}

    def Create(self, name=None):
        "Create the object externally, and return the instance"
        "data which is required by the read method to reload it"

        data = {}
        if name is not None:
            data['${View.primary_key}'] = int(name)
        else:
            data['${View.primary_key}'] = self.table.NextPrimaryKey()[0].${View.primary_key}
            self.context.__name__ = str(data['${View.primary_key}'])

        self.ContextToStorage(data)

        self.table.Create(**data)
        return data['${View.primary_key}']

    def Read(self, init_data):
        "Reload the data from the external object init data"

        cursor = self.table.Read(${View.primary_key} = init_data)
        if len(cursor) == 0:
            raise NotFound(self.container, str(init_data), None)
        row = cursor[0]
        self.context.__name__ = str(row.${View.primary_key})

        self.StorageToContext(row)

    def Update(self):
        "Update the external data if changed"

        data = {'${View.primary_key}': self.context.__name__}

        self.ContextToStorage(data)

        cursor = self.table.Update(**data)

    def Delete(self):
        "Delete the external data"

        data = {'${View.primary_key}': self.context.__name__}
        cursor = self.table.Delete(**data)

# CAN_EDIT_AFTER_THIS_LINE

class ${Table['name']}_Storage(${Table['name']}_StorageBase):
    pass

"""
