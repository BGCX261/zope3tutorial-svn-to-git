Generator
=========

This is a simple generator to generate Zope content types from the 
database. The toolchain is:

    python psql2dsl.py  table_name > dsl_file_name

    python z3gen.py dsl_file_name

Motivation
----------

This is essentially a teaching tool. I developed it because my tutorial on
ZSQLScript with Zope3 was too complicated. The configuration is just too
complex to keep explaining it in every tutorial.

It should also be useful for kick-starting a project, much the same as
ArchgenXML in Plone.

psql2dsl.py
-----------

This script will pull a definition from a postgresql database and generate
a dsl (domain specific language) file for it. You will need to edit the
psql2dsl.py script if your psql command requires parameters, i.e. a username
or database name.

z3gen.py
--------

This script generates a content object from the dsl definition. The ouput
is written to a folder called 'tables/table_name'. The entire content object
is stored in one folder.

The DSL
-------

The DSL is python. There are two sections, GENERAL and TABLES.

GENERAL
-------

This defines the following:

    namespace:      used for the translation domain and the name of the IZopeDatabaseAdapter
                    to be used for accessing the database;
    sql_dialect:    set to postgresql - intended to allow you to provide alternative templates
                    for other SQL targets
    target_folder:  where to put the generated files
    form_library:   either formlib or z3c
    z3c_layer:      If you are using z3c, you can specify a layer for the configuration.
                    The demonstration project (gentest) uses boston_pagelet_skin.IPageletLayer.

TABLES
------

List if tables to be generated:

    name:           The table name 
    stereotype:     Used to select alternative templates during generation
    primary_key:    The list of columns for primary key - only one column supported
    primary_key_has_sequence:
                    Boolean if the primary key has a sequence
    primary_key_sequence_name:
                    Name of the sequence if the primary key has a sequence
    columns:        The database columns

        colname:        the name of the column
        dbtype:         the type specification as per the database
        dbextra:        extra information from db, e.g. constraints 
        mapping_type:   The name of the class to map the underlying data object
                        to the value expected by the client. For example, MappingList
                        maps between an underlying comma separated string and a list.
        schema_type:    zope schema type
        schema_fields:  fields passed verbatim to the zope schema definition
        value_type:     for list type schema entries, the information about the values
        value_type_fields:  
                        pass verbatim to the value_type section of the schema

Examples:
========

    See examples folder

Issues, Bugs and Incompletnesses:
--------------------------------

The generator (currently) has only one template so can only generate a single output
type. However, when more templates are produced, they can be added via stereotype fields.

The conversion from postgresql to dsl makes a lot of assumptions.

The z3c.form code does not work with the IAdding menu.

The mapping between application types and underlying data is performed in two places.
The content object and the DMTL to created/update the record. See MappingList in the
code for more information.


Templates and Code Structure
----------------------------

z3gen.py

This is the driver code.

The code performs a number of steps to generate the output:

    z3gen_content
        This generates the content object and the related configuration.
        It uses the templates/content*py
    z3gen_dbclass
        This generates the database access methods.
        It uses the templates/dbclass*py
    z3gen_interfaces.py
        This generates the Zope schema.
        It uses the templates/interfaces*py
    z3gen_views.py
        This geneerates the view code.
        It uses the templates/view*py

z3gen_utilities.py

Provides a number of utilty functions.

templet.py

This is a templating library developed by David Bau, see http://davidbau.com/templet.
