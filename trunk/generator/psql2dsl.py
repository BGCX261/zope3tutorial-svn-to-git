#!/usr/bin/env python

#   Generate a dsl file from a postgres database table

#   TODO: Merge results with an existing output file

import sys, os

NAMESPACE='castingzone'
PSQLCMD='echo \\\d %s | psql -t' 

# First Grab the Data Model
def grab_schema(table):
    """Postgres mechanism to grab schema"""
    pipe = os.popen(PSQLCMD % table)

    # Now parse it
    rv=[]
    for row in pipe.readlines():
        if len(row) == 0: continue
        if row[-1] in ['\n', '\r']: row = row[:-1]
        if len(row) == 0: continue
        if row[-1] in ['\n', '\r']: row = row[:-1]
        if len(row) == 0: continue
        parts = row.split('|')
        if len(parts) < 2:
            continue
        parts = [x.strip() for x in parts ]
        rv.append(parts)
    return rv

def getSequenceId(s):
    """If the field is a serial, pull the sequence id out of the field"""
    parts = s.split('nextval')
    if len(parts) < 2:
        return ''
    parts = parts[1].split("'")
    return parts[1]

def getLengthFromType(t):
    """Get the maximum length of a field from the postgres type"""
    if t.find('char') == -1:
        return None
    dimension = t.split('(')[1].split(')')[0]
    return int(dimension)

# Guess a schema type based on the postgres type
def PGTypeToSchemaType(pgname, pgtype, pgextra):
    if pgextra.find('not null') != -1:
        required=True
    else:
        required=False
    fields=[(u'title', pgname), (u'description', pgname)]
    if pgtype == 'integer':
        seq = getSequenceId(pgextra)
        if seq:
            fields.append((u'readonly', True))
        else:
            fields.append((u'required', required))
        return ('schema.Int', fields)

    fields.append((u'required', required))
    if pgtype == 'double precision':
        return 'schema.Float', fields
    elif pgtype == 'boolean':
        return 'schema.Bool', fields
    elif pgtype == 'date':
        return 'schema.Date', fields
    elif pgtype == 'text':
        return 'schema.Text', fields
    elif pgtype.find('timestamp') != -1:
        return 'schema.Datetime', fields
    else:
        fieldlen = getLengthFromType(pgtype)
        if fieldlen != None:
            fields.append((u'max_length', fieldlen))
        return 'schema.TextLine', fields

print """GENERAL = {
    'namespace': '%s',
    'sql_dialect': 'postgresql',
    'target_folder': 'tables',
    'form_library': 'z3c',  # formlib or z3c
    'z3c_layer': 'boston_pagelet_skin.IPageletLayer',
}
""" % NAMESPACE

print "TABLES=["

for table in sys.argv[1:]:
    schema = grab_schema(table)

    print "\t{"
    print "\t\t'name': '%s'," % table
    print '\t\t# Options should be : traversal-standard, traversal-group, standard, group, grid'
    print "\t\t'stereotype': 'traversal-standard',"

    # TODO: Get the primary key properly
    column = schema[0]
    print "\t\t'primary_key': ['%s'], " % column[0]

    # Check to see if the primary key has a sequence
    seq = getSequenceId(column[2])
    if seq:
        print "\t\t'primary_key_has_sequence': True,"
        print "\t\t'primary_key_sequence_name': '%s'," % seq
    else:
        print "\t\t'primary_key_has_sequence': False,"

    print "\t\t'columns':  ["

    for column in schema:
        print "\t\t\t{"
        print "\t\t\t\t'colname': '%s'," % column[0]
        print "\t\t\t\t'dbtype': '%s',"  % column[1]
        if column[2]:
            print '\t\t\t\t"dbextra": "%s",' % column[2]

        if column[1] == 'boolean':
            print "\t\t\t\t'mapping_type': 'MappingBool',"

        (stype, sextra) =  PGTypeToSchemaType(column[0], column[1], column[2])
        print "\t\t\t\t'schema_type': '%s'," % stype
        print "\t\t\t\t'schema_fields': {"
        for (k,v) in sextra:
            if v in [True, False]:
                v = str(v)
            elif type(v) == type(0):
                v = str(v)
            else:
                v = "'"+str(v)+"'"
            print "\t\t\t\t\t'%s': %s," % (k,v)
        print "\t\t\t\t},"
        print "\t\t\t},"

    print "\t\t],"

    print "\t},"

print "]"  # End of tables list
