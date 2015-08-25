import z3gen_utilities

TAB='    '

class Generator:
    def __init__(self, DSLModel, Table):
        self.DSLModel = DSLModel
        self.Table = Table
        self.TableName = Table['name']
        self.interface_name = 'I%s%s' % (self.TableName[0].upper(), self.TableName[1:])
        self.field0name = Table['columns'][0]['colname']
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

        self.columns_excluding_key = [x for x in Table['columns'] if x['colname'] != self.primary_key]
        self.key_columns = [x for x in Table['columns'] if x['colname'] == self.primary_key]

        self.update_omit=".omit('__name__', '__parent__')" 
        self.view_omit=".omit('__name__', '__parent__')" 
        self.create_omit=".omit('__name__', '__parent__')"

        self.load_templates()

    def load_templates(self):
        """Load the template. Search for:
            templates/views_form_library_stereotype
            templates/views_form_library
            templates/views_stereotype
            templates/views

            Form library should be one of formlib or z3c (.form)
        """
        stereotype = self.Table['stereotype']
        form_library = self.DSLModel['GENERAL']['form_library']
        import_paths=[
            'templates/views_%s_%s' % (form_library, stereotype),
            'templates/views_%s' % (form_library),
            'templates/views_%s' % (stereotype),
            'templates/views']
        self.templates = z3gen_utilities.ImportTemplate(import_paths)

    def filename(self):
        """Return the name of the file"""
        return '%s_views.py' % self.TableName

    def render(self):
        """Return a string containing the generated file"""

        rv = []
        self.classnames=[]
        self.classnames.append('Add')
        self.classnames.append('Edit')
        self.classnames.append('View')

        file_content = self.templates.GenFile(self.DSLModel, self.Table, self)
        file_content = file_content.replace('\t', TAB)

        z3gen_utilities.ReplaceFile(self.DSLModel, self.Table,
            self.filename(), file_content, format="python")

        # configure.zcml entries
        self.genConfiguration()

    def genConfiguration(self):
        """The configure.zcml entries required"""

        file_content = self.templates.GenConfiguration(self.DSLModel, self.Table, self)
        self.Table['config'].append(file_content)
