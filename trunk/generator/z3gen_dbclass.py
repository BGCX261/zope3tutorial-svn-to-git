import sys
import z3gen_utilities

TAB='    '


def DTMLType(n):
    if n == 'integer':
        return 'int'
    if n == 'double precision':
        return 'float'
    else:
        return 'string'

class Generator:
    def __init__(self, DSLModel, Table):
        self.DSLModel = DSLModel
        self.Table = Table
        self.TableName = Table['name']
        self.columns=[]
        for column in Table['columns']:
            required = column['schema_fields'].get('required', False)
            self.columns.append((column['colname'], DTMLType(column['dbtype']), required))

        # Extract the primary key from the list of fields. Don't allow the user
        # to change this on the edit screens
        self.primary_key=Table.get('primary_key', None)
        if self.primary_key != None:
            if type(self.primary_key) == type([]):
                # primary key DSL syntax can be list of fields
                if len(self.primary_key) > 1:
                    print 'Error - only handle the case of a single primary key'
                    sys.exit(1)
                self.primary_key = self.primary_key[0]
        else:
            # For now assume that it is the first field if the generator needs one.
            # later this should be an error
            self.fields_excluding_key = Table['columns'][1:]
            self.primary_key = self.field0name
            print 'Assuming that the primary key is the first key field'

        # Split the primary_key out of the list of columns
        self.columns_excluding_key = [x for x in self.columns if x[0] != self.primary_key]
        self.key_columns = [x for x in self.columns if x[0] == self.primary_key]

        if len(self.key_columns) == 0:
            print 'Error - primary key is not set of columns'
            sys.exit(1)

        self.primary_key_type = self.key_columns[0][1]

        key_table_col = [x for x in Table['columns'] if x['colname'] == self.primary_key]

        # Extract special field types that have to be massaged during create/update
        self.bools=[x['colname'] for x in Table['columns'] if x['schema_type'] == 'schema.Bool' and x['dbtype'] == 'boolean']
        self.commalists=[x['colname'] for x in Table['columns'] if x.get('mapping_type', 'MappingProperty') == 'MappingList']

        self.load_templates()

    def load_templates(self):
        """Load the template. Search for:
            templates/dbclass_sql_dialect_stereotype
            templates/dbclass_sql_dialect
            templates/dbclass_stereotype
            templates/dbclass

            Form library should be one of formlib or z3c (.form)
        """
        stereotype = self.Table['stereotype']
        sql_dialect = self.DSLModel['GENERAL']['sql_dialect']
        import_paths=[
            'templates/dbclass_%s_%s' % (sql_dialect, stereotype),
            'templates/dbclass_%s' % (sql_dialect),
            'templates/dbclass_%s' % (stereotype),
            'templates/dbclass']
        self.templates = z3gen_utilities.ImportTemplate(import_paths)

    def filename(self):
        """Return the name of the file"""
        return '%s_db.py' % self.TableName

    def render(self):
        """Return a string containing the generated file"""

        self.classnames=[]
        self.classnames.append(self.Table['name'])

        file_content = self.templates.GenFile(self.DSLModel, self.Table, self)
        file_content = file_content.replace('\t', TAB).replace('\\"""', '"""')

        z3gen_utilities.ReplaceFile(self.DSLModel, self.Table,
            self.filename(), file_content, format="python")
