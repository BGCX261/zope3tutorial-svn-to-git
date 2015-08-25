
#   Generate a search form. Will be registered on the container

import z3gen_utilities
import os, os.path

TAB='    '

class Generator:
    def __init__(self, DSLModel, Table):
        self.DSLModel = DSLModel
        self.Table = Table
        self.TableName = Table['name']
        self.field0name = Table['columns'][0]['colname']
        self.interface_name = 'I%s%s' % (self.TableName[0].upper(), self.TableName[1:])
        self.z3c_layer=''
        try:
            self.z3c_layer='layer="%s"\n\t\t' % self.DSLModel['GENERAL']['z3c_layer']
        except:
            pass

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

        self.search_columns = Table.get('search_columns', [self.primary_key])
        self.list_columns = Table.get('list_columns', None)
        if not self.list_columns:
            self.list_columns = [ col['colname'] for col in Table['columns'][:5]]

        # Set the search columns back into the table
        Table['search_columns'] = self.search_columns
        Table['list_columns'] = self.list_columns

        # The columns in the search schema
        self.schema_columns = [ col for col in Table['columns'] if col['colname'] in self.list_columns]

        self.load_templates()

    def load_templates(self):
        """Load the template. Search for:
            templates/search_form_library_stereotype
            templates/search_form_library
            templates/search_stereotype
            templates/search

            Form library should be one of formlib or z3c (.form)
        """
        stereotype = self.Table['stereotype']
        form_library = self.DSLModel['GENERAL']['form_library']
        import_paths=[
            'templates/search_%s_%s' % (form_library, stereotype),
            'templates/search_%s' % (form_library),
            'templates/search_%s' % (stereotype),
            'templates/search']
        self.templates = z3gen_utilities.ImportTemplate(import_paths)

    def filename(self):
        """Return the name of the file"""
        return '%s_search.py' % self.TableName

    def render(self):
        """Generate the required files"""

        file_content = self.templates.GenFile(self.DSLModel, self.Table, self)
        file_content = file_content.replace('\t', TAB)

        z3gen_utilities.ReplaceFile(self.DSLModel, self.Table,
            self.filename(), file_content, format="python")

        # configure.zcml entries
        self.genConfiguration()

        # Write out the template - don't do it if it already exists
        TemplatesPath = "%s%s%s%stemplates" % (self.DSLModel['GENERAL']['target_folder'],
            os.sep, self.Table['name'], os.sep)
        TemplateFile= TemplatesPath + os.sep + 'list.pt'
        if not os.path.exists(TemplateFile):
            template_content = self.templates.GenTemplate(self.DSLModel, self.Table, self)
            fh = open(TemplateFile, 'w')
            fh.write(template_content)
            fh.close()

    def genConfiguration(self):
        """The configure.zcml entries required"""

        file_content = self.templates.GenConfiguration(self.DSLModel, self.Table, self)
        self.Table['config'].append(file_content)
