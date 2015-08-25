
from templet import stringfunction

@stringfunction
def GenTestLoader(DSLModel, Table, View):
    """
import unittest
from doctest import DocFileSuite

def test_suite():
    return unittest.TestSuite((DocFileSuite('${Table['name']}.txt'),))

if __name__ == '__main__':
    unittest.main(defaultTest = 'test_suite')
"""

@stringfunction
def GenDocTests(DSLModel, Table, View):
    """
Doc Test for ${Table['name']}
=================

Run these from the same area that your start your zope instance,
using this command:

    ./bin/test -s tables.${Table['name']}

Once this file exists, it should not be replaced by the generator

Note, you will need to have a test database which works with the
schema implemented. Edit the DB_CONNECTION_STRING below as appropriate.
To echo SQL statement, set the flag below. This causes tests to fail.

    >>> DB_CONNECTION_STRING='dbi://'
    >>> DB_ECHO_SQL=False

Create a site:

    >>> from zope.app.testing import setup
    >>> root = setup.placefulSetUp(site=True)
    >>> sitemanager = setup.createSiteManager(root)
    >>> from zope.component import getSiteManager
    >>> sitemanager = getSiteManager()

Connect to the database:

    >>> import psycopgda.adapter as adapter
    >>> from psycopgda.adapter import PsycopgAdapter
    >>> db_adapter = PsycopgAdapter(DB_CONNECTION_STRING)

    >>> from zope.rdb.interfaces import IZopeDatabaseAdapter
    >>> from tables.${Table['name']} import CONNECTION_NAME
    >>> sitemanager.registerUtility(db_adapter, provided=IZopeDatabaseAdapter, name=CONNECTION_NAME)

Set up a database connection utility

    >>> from zope.component import getUtility
    >>> connection = getUtility(IZopeDatabaseAdapter, CONNECTION_NAME)()
    >>> from zope.rdb import queryForResults
    >>> rowcount = queryForResults(connection, 'select count(*) from ${Table['name']}')[0].count

Set up dummy vocabularies for all of the required vocabularies

[ The utility registry does not seem to work with vocabularies in a unit test. 
I am forced to register them directly to the vocabulary registry ]

    >>> from zope.interface import alsoProvides
    >>> from zope.schema.vocabulary import SimpleVocabulary
    >>> from zope.schema.interfaces import IVocabularyFactory
    >>> def testvocab(context):
    ...     return SimpleVocabulary.fromValues(['x'])
    >>> alsoProvides(testvocab, IVocabularyFactory)
    >>> from zope.schema.vocabulary import getVocabularyRegistry
    >>> vr = getVocabularyRegistry()
${{
    for vocab in View.required_vocabularies:
        out.append("\\t>>> vr.register( u'%s', testvocab)\\n" % vocab)
}}


Verify that all of our modules import

    >>> import tables.${Table['name']} 
    >>> from tables.${Table['name']} import schema_helpers
    >>> from tables.${Table['name']} import db 
    >>> db.ECHO_SQL = DB_ECHO_SQL
    >>> from tables.${Table['name']} import interfaces
    >>> from tables.${Table['name']} import ${Table['name']}_db 
    >>> from tables.${Table['name']} import ${Table['name']}_storage 
    >>> from tables.${Table['name']} import ${Table['name']}_content 
    >>> from tables.${Table['name']} import ${Table['name']}_views 
    >>> from tables.${Table['name']} import ${Table['name']}_search

Register the adapters:

    >>> factory=${Table['name']}_storage.${Table['name']}_Storage
    >>> sitemanager.registerAdapter(factory)
    >>> factory=${Table['name']}_content.${Table['name']}ContainerNameChooser
    >>> sitemanager.registerAdapter(factory)
    >>> factory=${Table['name']}_content.${Table['name']}_dublincore
    >>> sitemanager.registerAdapter(factory)

Create the container

    >>> container = ${Table['name']}_content.${Table['name']}Container()
    >>> container.__name__ = '${Table['name']}'
    >>> root[container.__name__] = container
    >>> container = root[container.__name__] 

Create a ${Table['name']} object

    >>> import transaction

    >>> from zope.app.container.interfaces import INameChooser
    >>> newobj = ${Table['name']}_content.${Table['name']}()
    >>> from datetime import date

${{
    for column in Table['columns']:
        if column['colname'] == View.primary_key: continue
        schema_type = column.get('schema_type', 'TextLine')
        value = None
        if schema_type == 'schema.TextLine':
            max_length = column['schema_fields'].get('max_length', '1')
            value = 'A' * int(max_length)
            value = 'u"' + value + '"'
        if schema_type == 'schema.Int':
            value = '1'
        if schema_type == 'schema.Float':
            value = '1.0'
        if schema_type == 'schema.List':
            value = '[]'
        if schema_type == 'schema.Set':
            value = 'set([])'
        if schema_type == 'schema.Text':
            value = 'u"TEXT"'
        if schema_type == 'schema.Date':
            import time
            t = time.localtime()
            value = 'date(%d, %02.2d, %02.2d)' % (t[0], t[1], t[2])
        if value is not None:
            out.append("\t>>> newobj.%s = %s\\n" % (column['colname'], value))
}}

    >>> nc = INameChooser(container)
    >>> newobj.__name__ = nc.chooseName('', newobj)
    >>> container[newobj.__name__] = newobj
    >>> transaction.get().commit()
    >>> contained_obj = container[newobj.__name__] 
    >>> contained_obj == newobj
    True

Update a ${Table['name']} object

${{
    for column in Table['columns']:
        if column['colname'] == View.primary_key: continue
        schema_type = column.get('schema_type', 'TextLine')
        value = None
        if schema_type == 'schema.TextLine':
            max_length = column['schema_fields'].get('max_length', '1')
            value = 'x' * int(max_length)
            value = 'u"' + value + '"'
        if schema_type == 'schema.Int':
            value = '0'
        if schema_type == 'schema.Float':
            value = '0.0'
        if schema_type == 'schema.List':
            value = '[]'
        if schema_type == 'schema.Set':
            value = 'set([])'
        if schema_type == 'schema.Text':
            value = 'u"text"'
        if schema_type == 'schema.Date':
            import time
            t = time.localtime()
            value = 'date(%d, %02.2d, %02.2d)' % (t[0], t[1], t[2])
        if value is not None:
            out.append("\t>>> newobj.%s = %s\\n" % (column['colname'], value))
}}

    >>> transaction.get().commit()


Read an actor object back. We need to clear the cache to for external storage Read().

    >>> container.clear_cache()
    >>> oldobj = container[newobj.__name__]
    >>> oldobj != newobj
    True

    >>> newobj = oldobj

Verify the DublinCore Annotations

    >>> from zope.dublincore.interfaces import IZopeDublinCore
    >>> dc = IZopeDublinCore(newobj)
    >>> dc.title == newobj.__name__
    True
    >>> dc.description == newobj.__name__
    True

Delete the ${Table['name']} object

    >>> del container[newobj.__name__]
    >>> transaction.get().commit()
"""

