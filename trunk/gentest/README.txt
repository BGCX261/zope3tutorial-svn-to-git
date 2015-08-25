Zope Instance to test Generator
===============================

This folder is intended to operate as a generator test instance.

In the area where you hold your zope instances:

    1.  Use zopeproject to create an area called gentest
    2.  Copy this folder over your new gentest instance

Run the system:

    bin/paste serve debug.ini

Go to manage site, and create a database adapter. 
Register the adapter using the IZopeDatabaseAdapter Interface with the name 'gentest'.

Test it to make sure it works.

Now you are ready to run the generator.

Create a dsl file.

Go to the src folder:

    run python $HOME/generator/z3gen.py filename.dsl

This should create a folder:

    src/tables/table_name

Restart the zope instance and see if it has been picked up.
