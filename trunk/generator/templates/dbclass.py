# Templates for generating interfaces
#
# Uses the templet library from davidbau.com
#

from templet import stringfunction


@stringfunction
def GenFile(DSLModel, Table, View):
    r"""
import types
from base64 import encodestring

from db import SQLDTML_Base


class ${Table['name']}Base(SQLDTML_Base):
    \"""
    CREATE TABLE ${Table['name']} (
${{
    for i in range(len(Table['columns'])):
        column = Table['columns'][i]
        if i == len(Table['columns'])-1: comma=''
        else: comma=','
        if column.has_key('dbextra'):
            dbextra = ' '+column['dbextra']
        else:
            dbextra = ''
        out.append('\t\t%s %s%s%s\n' % (column['colname'], column['dbtype'], dbextra, comma))
}}
    );
    \"""
    def Create(self,
    ${{
        out.append('\t'+', '.join([col[0] for col in View.columns_excluding_key]))
    }}, ${View.primary_key} = None):
        \"""
        insert into ${Table['name']} (
    ${{
        out.append('\t\t'+', '.join([col[0] for col in View.columns_excluding_key]))
    }}

            <dtml-if expr="${View.primary_key} != None">
                , ${View.primary_key}
            </dtml-if>
        ) values (
${{
        for (name, dbtype, required) in View.columns_excluding_key[:-1]:
            optional=''
            if not required: optional=' optional'
            out.append('\t\t\t<dtml-sqlvar %s type="%s"%s>,\n' % (name, dbtype, optional))
        (name, dbtype, required) = View.columns_excluding_key[-1]
        optional=''
        if not required: optional=' optional'
        out.append('\t\t\t<dtml-sqlvar %s type="%s"%s>\n' % (name, dbtype, optional))
}}
            <dtml-if expr="${View.primary_key} != None">
                , <dtml-sqlvar ${View.primary_key} type="${View.primary_key_type}">
            </dtml-if>
        );
${{if Table['primary_key_has_sequence']:
        out.append('\t\t<dtml-if expr="%s == None">\n' % View.primary_key)
        out.append("\t\t\tselect currval('%s') as %s;\n" %
            (Table['primary_key_sequence_name'], View.primary_key))
        out.append('\t\t</dtml-if>\n')
    }}
        \"""
        params={}
        for (k,v) in locals().items():
            if k in ['self', 'params']: continue
            if v is not None: params[k] = v
        result = self.execute('${Table['name']}.Create', self.Create.__doc__, **params)
        return result

    def Read(self, ${View.primary_key}):
        \"""select * from ${Table['name']} where
            ${View.primary_key} = <dtml-sqlvar ${View.primary_key} type="${View.primary_key_type}">
        \"""
        params=locals().copy()
        del params['self']
        result = self.execute('${Table['name']}.Read', self.Read.__doc__, **params)
        return result

    def Update(self, ${View.primary_key},
${{field_names=[col[0] for col in View.columns[1:]]
out.append('\t\t' + '=None, '.join(field_names) +'=None')
}}
):
        \"""
        update ${Table['name']}
            set ${View.primary_key} = ${View.primary_key} 
${{
    for (col_name, col_type, required) in View.columns_excluding_key:
        out.append('\t\t\t<dtml-if expr="%s != None">\n' % col_name)
        out.append('\t\t\t\t, %s=<dtml-sqlvar %s type="%s">\n' % (col_name, col_name, col_type))
        out.append('\t\t\t</dtml-if>\n')
}}
        where
            ${View.primary_key} = <dtml-sqlvar ${View.primary_key} type="${View.primary_key_type}">
        \"""
        params={}
        for (k,v) in locals().items():
            if k in ['self', 'params']: continue
            params[k] = v
        result = self.execute('${Table['name']}.Update', self.Update.__doc__, **params)
        return result

    def Delete(self, ${View.primary_key}):
        \"""
        delete from ${Table['name']} where 
            ${View.primary_key} = <dtml-sqlvar ${View.primary_key} type="${View.primary_key_type}">
        \"""
        params=locals().copy()
        del params['self']
        result = self.execute('${Table['name']}.Delete', self.Delete.__doc__, **params)
        return result

    def Keys(self):
        \"""
            select ${View.primary_key} from ${Table['name']} order by ${View.primary_key}
        \"""
        result = self.execute('${Table['name']}.Keys', self.Keys.__doc__)
        return result

    def Len(self):
        \"""
            select count(*) from ${Table['name']}
        \"""
        result = self.execute('${Table['name']}.Len', self.Len.__doc__)
        return result


    def Search(self, ${{ out.append('=None, '.join(Table['search_columns']) +'=None,') }}
        start=None, batch_size=None):
        \"""select * from ${Table['name']}
            where
                1 = 1
${{
    for (col_name, col_type, required) in [ col for col in View.columns if col[0] in Table['search_columns']]:
        if col_type == 'string': match = 'ilike'
        else: match = '='
        out.append('\t\t\t<dtml-if expr="%s != None">\n' % col_name)
        out.append('\t\t\t\tand %s %s <dtml-sqlvar %s type="%s">\n' % (col_name, match, col_name, col_type))
        out.append('\t\t\t</dtml-if>\n')
}}
                <dtml-if expr="start != None">
                    and id > <dtml-sqlvar start type="int">
                </dtml-if>
            order by id
            <dtml-if expr="batch_size != None">
                limit <dtml-sqlvar batch_size type="int">
            </dtml-if>
        \"""
        params={}
        for (k,v) in locals().items():
            if k in ['self', 'params']: continue
            if k in ['start', 'batch_size']:
                params[k] = v
                continue
            if type(v) in types.StringTypes:
                params[k] = v.replace('*', '%')
            else:
                params[k] = v

        result = self.execute('${Table['name']}.Search', self.Search.__doc__, **params)
        return result



${{if Table['primary_key_has_sequence']:
    out.append('\tdef NextPrimaryKey(self):\n')
    out.append('\t\t\"""\n')
    out.append("\t\t\tselect nextval('%s') as %s;\n" %
            (Table['primary_key_sequence_name'], View.primary_key))
    out.append('\t\t\"""\n')
    out.append("\t\tresult = self.execute('%s.NextPrimaryKey', self.NextPrimaryKey.__doc__)\n" % Table['name'])
    out.append('\t\treturn result\n\n')
}}

# CAN_EDIT_AFTER_THIS_LINE

${{
for classname in View.classnames:
    out.append('class %s(%sBase):\n' % (classname, classname))
    out.append('\tpass\n\n')
}}
"""
