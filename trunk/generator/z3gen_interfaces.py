#   Generator for interfaces

import z3gen_utilities

TAB='    '

class Generator:
    def __init__(self, DSLModel, Table):
        self.DSLModel = DSLModel
        self.Table = Table
        self.TableName = Table['name']
        self.interface_name = 'I%s%s' % (self.TableName[0].upper(), self.TableName[1:])

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


    def load_templates(self):
        """Load the template. Search for:
            templates/interfaces_stereotype
            templates/interfaces
        """
        stereotype = self.Table['stereotype']
        import_paths=['templates/interfaces_%s' % stereotype, 'templates/interfaces']
        self.templates = z3gen_utilities.ImportTemplate(import_paths)

    def filename(self):
        """Return the name of the file"""
        return 'interfaces.py'

    def render(self):
        """Return a string containing the generated file"""

        self.classnames=[]
        self.classnames.append(self.interface_name)
        self.classnames.append('%sContainer' % self.interface_name)

        file_content = self.templates.GenFile(self.DSLModel, self.Table, self)
        file_content = file_content.replace('\t', TAB)

        z3gen_utilities.ReplaceFile(self.DSLModel, self.Table,
            self.filename(), file_content, format="python")
