import sys
import z3gen_utilities

TAB='    '

class Generator:

    def __init__(self, DSLModel, Table):
        self.DSLModel = DSLModel
        self.Table = Table
        self.TableName = Table['name']
        self.interface_name = 'I%s%s' % (self.TableName[0].upper(), self.TableName[1:])
        self.field0name = Table['columns'][0]['colname']

        # Build a list of all of the vocabularies required
        vocabs=[]
        for col in Table['columns']:
            schema = col['schema_fields']
            if 'vocabulary' in schema:
                vocab = schema['vocabulary']
                if vocab not in vocabs:
                    vocabs.append(vocab)
            if 'value_type_fields' in col:
                schema = col['value_type_fields']
                if 'vocabulary' in schema:
                    vocab = schema['vocabulary']
                    if vocab not in vocabs:
                        vocabs.append(vocab)
        self.required_vocabularies = vocabs
            
        self.load_templates()

        # Extract the primary key from the list of fields for separate
        # processing if required
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

        self.fields_excluding_key = [x for x in Table['columns'] if x['colname'] != self.primary_key]

    def load_templates(self):
        """Load the template. Search for:
            templates/content_stereotype
            templates/content
        """
        stereotype = self.Table['stereotype']
        import_paths=['templates/content_%s' % stereotype, 'templates/content']
        self.templates = z3gen_utilities.ImportTemplate(import_paths)
        import_paths=['templates/tests_%s' % stereotype, 'templates/tests']
        self.test_templates = z3gen_utilities.ImportTemplate(import_paths)

    def filename(self):
        """Return the name of the file"""
        return '%s_content.py' % self.TableName

    def storage_filename(self):
        """Return the name of the file"""
        return '%s_storage.py' % self.TableName

    def tests_filename(self):
        """Return the name of the file"""
        return 'tests.py'

    def doctests_filename(self):
        """Return the name of the file"""
        return '%s.txt' % self.TableName

    def render(self):
        """Return a string containing the generated file"""

        self.classnames=[]
        self.classnames.append(self.Table['name'])
        self.classnames.append(self.Table['name']+'Container')
        self.classnames.append(self.Table['name']+'_dublincore')
        self.classnames.append(self.Table['name']+'ContainerNameChooser')

        file_content = self.templates.GenFile(self.DSLModel, self.Table, self)
        file_content = file_content.replace('\t', TAB)

        z3gen_utilities.ReplaceFile(self.DSLModel, self.Table,
            self.filename(), file_content, format="python")

        file_content = self.templates.GenStorageFile(self.DSLModel, self.Table, self)
        file_content = file_content.replace('\t', TAB)

        z3gen_utilities.ReplaceFile(self.DSLModel, self.Table,
            self.storage_filename(), file_content, format="python")

        # configure.zcml entries
        self.genConfiguration()

        # Tests
        self.genTests()

    def genConfiguration(self):
        """The configure.zcml entries required"""

        file_content = self.templates.GenConfiguration(self.DSLModel, self.Table, self)
        self.Table['config'].append(file_content)

    def genTests(self):
        """Generate the tests - these files are not replaced if they exist"""
        if not z3gen_utilities.FileExists(self.DSLModel, self.Table,
            self.tests_filename()):
            file_content = self.test_templates.GenTestLoader(self.DSLModel, self.Table, self)
            file_content = file_content.replace('\t', TAB)

            z3gen_utilities.ReplaceFile(self.DSLModel, self.Table,
                self.tests_filename(), file_content, format="python")

        if not z3gen_utilities.FileExists(self.DSLModel, self.Table,
            self.doctests_filename()):
            file_content = self.test_templates.GenDocTests(self.DSLModel, self.Table, self)
            file_content = file_content.replace('\t', TAB)

            z3gen_utilities.ReplaceFile(self.DSLModel, self.Table,
                self.doctests_filename(), file_content, format="doctest")



