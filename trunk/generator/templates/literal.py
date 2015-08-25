from templet import stringfunction


@stringfunction
def db_file(DSLModel, Table):
    """
# A base class to allow me to structure my SQLDTML Code together

import zope.component
from zope.rdb.interfaces import IZopeDatabaseAdapter
from zope.rdb import queryForResults
from zope.app.sqlscript.dtml import SQLDTML

from ${DSLModel['GENERAL']['target_folder']}.${Table['name']} import CONNECTION_NAME

ECHO_SQL=False

class SQLDTML_BaseBase:

    def __init__(self, context):
        \"""I need to store the context. Since I use a local utility, the
        context is required to find it. Otherwise would find only global utilities\"""
        self.context = context

    def execute(self, ex_command_name, ex_dtml_str, **params):
        \"""execute the instruction.
            ex_command_name is the name of the function - intended for use in error messages
            dtml_str is the dmtl command as a string
            params are the parameters to be encoded
        \"""
        sqldtml = SQLDTML(ex_dtml_str)
        query = sqldtml(**params)
        if ECHO_SQL:
            print "--------------------------------------------------------------------"
            print query 
        connection= zope.component.getUtility(IZopeDatabaseAdapter, CONNECTION_NAME, self.context)()
        return queryForResults(connection, query)

# CAN_EDIT_AFTER_THIS_LINE

class SQLDTML_Base(SQLDTML_BaseBase):
    pass

""" 

@stringfunction
def config_file(DSLModel, Table):
    """
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
${{
if (DSLModel['GENERAL']['form_library'] == 'z3c'):
    out.append('\txmlns:z3c="http://namespaces.zope.org/z3c"\\n')
}}
    i18n_domain="${DSLModel['GENERAL']['namespace']}.${Table['name']}">

${{
for c in Table['config']:
    out.append(c)
    out.append('\\n')
}}

<!-- CAN_EDIT_AFTER_THIS_LINE -->

</configure>
    """

@stringfunction
def init_file(DSLModel, Table):
    """
from zope.i18nmessageid import MessageFactory
MessageFactory = MessageFactory('${DSLModel['GENERAL']['namespace']}.${Table['name']}')
CONNECTION_NAME='${DSLModel['GENERAL']['namespace']}'
"""

@stringfunction
def schema_helpers(DSLModel, Table):
    """
# Functions used to map single content elements to single table 
# elements. Focus on database type to python type e.g. list

from zope.schema.fieldproperty import FieldProperty

from base64 import encodestring, decodestring

def Bool_toStorage(value):
    if value: return 't'
    return 'f'
def Bool_fromStorage(value):
    return value
def List_toStorage(value):
    if value:
        return ','.join(value)
    else:
        return ''
def List_fromStorage(value):
    if value:
        return value.split(',')
    else:
        return []
def BinaryToBase64_fromStorage(value):
    if value is None or len(value) == 0: return ''
    return decodestring(value)
def BinaryToBase64_toStorage(value):
    if value is None or len(value) == 0: return ''
    return encodestring(value)

"""
