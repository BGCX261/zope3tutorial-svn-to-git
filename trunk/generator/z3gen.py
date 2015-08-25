#!/usr/bin/env python

#   z3gen.py
#
#   WARNING: This module evaluates the dsl using the python interpreter
#            Only run this code on a file you are complete sure of
#
#   This is a very simple generator for building content types
#   which are stored in the database.
#
#   The generation works from a dsl file. 
#
#   You can generate a dsl file from a postgres database using the
#   psql2dsl.py command
#
szUsage="Usage: python zope3gen.py [options] dslfile\n"

import sys, os

import z3gen_utilities

#######################################################################################
# Process the command line and get the DSLModel

cmd_args=z3gen_utilities.parseCmdLine(sys.argv[1:])

dsl_filenames=cmd_args[1]
if len(dsl_filenames) != 1:
    sys.stderr.write(szUsage)
    sys.exit(1)

# Load the model from the DSL File
dsl_filename=dsl_filenames[0]
DSLModel={}
execfile(dsl_filename, DSLModel)

# Modify the model with any command line arguments (these affect the general section)
for (k,v) in cmd_args[0]:
    DSLModel['GENERAL'][k]=v


#######################################################################################
#   Load the generators and generate

import z3gen_interfaces
import z3gen_dbclass
import z3gen_content
import z3gen_views
import z3gen_search
import templates.literal

GENERATORS=[
    z3gen_interfaces.Generator,
    z3gen_dbclass.Generator,
    z3gen_content.Generator,
    z3gen_views.Generator,
    z3gen_search.Generator,
    ]


for Table in DSLModel['TABLES']:

    z3gen_utilities.BuildPath(DSLModel, Table)
    z3gen_utilities.AddNewPackage(DSLModel['GENERAL']['target_folder'],
        Table['name'], DSLModel['GENERAL']['namespace'])

    Table['config'] = [] # The generators can put configuration stuff here

    # These are the important generators - they output their own files
    for generator in GENERATORS:
        view = generator(DSLModel, Table)
        view.render()

    content = templates.literal.db_file(DSLModel, Table)
    z3gen_utilities.ReplaceFile(DSLModel, Table, 'db.py', content, format="python")

    content = templates.literal.config_file(DSLModel, Table)
    z3gen_utilities.ReplaceFile(DSLModel, Table, 'configure.zcml', content, format="zcml")

    content = templates.literal.init_file(DSLModel, Table)
    z3gen_utilities.ReplaceFile(DSLModel, Table, '__init__.py', content, format="python")

    content = templates.literal.schema_helpers(DSLModel, Table)
    z3gen_utilities.ReplaceFile(DSLModel, Table, 'schema_helpers.py', content, format="python")


