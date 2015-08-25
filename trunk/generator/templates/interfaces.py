# Templates for generating interfaces
#
# Uses the templet library from davidbau.com
#

from templet import stringfunction
import types

@stringfunction
def GenFile(DSLModel, Table, View):
    """
from zope import schema

from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import contains, containers

from ${DSLModel['GENERAL']['target_folder']}.${Table['name']} import MessageFactory as _

class ${View.interface_name}Base(IContained):
${{
for row in Table['columns']:
    if row['colname'] == View.primary_key: continue
    out.append('\t%s = %s(' % (row['colname'], row['schema_type']))

    for (k,v) in row['schema_fields'].items():
        if type(v) in types.StringTypes:
            out.append("%s=_(u'%s'), " % (k,v))
        else:
            out.append("%s=%s, " % (k,v))
    if row.has_key('value_type'):
        out.append("\\n\t\tvalue_type=%s(" % row['value_type'])
        for (k,v) in row['value_type_fields'].items():
            if type(v) in types.StringTypes:
                out.append("%s=_(u'%s'), " % (k,v))
            else:
                out.append("%s=%s, " % (k,v))
        out.append(')  ')
    out.append(')\\n')
}}

    containers('${DSLModel['GENERAL']['target_folder']}.${Table['name']}.interfaces.${View.interface_name}Container')

class ${View.interface_name}ContainerBase(IContainer):
    contains('${DSLModel['GENERAL']['target_folder']}.${Table['name']}.interfaces.${View.interface_name}')

# CAN_EDIT_AFTER_THIS_LINE

${{
for classname in View.classnames:
    out.append('class %s(%sBase):\\n' % (classname, classname))
    out.append('\tpass\\n\\n')
}}
"""
