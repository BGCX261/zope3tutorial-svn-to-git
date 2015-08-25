import unittest
import doctest

from Testing import ZopeTestCase as ztc

from kg.locationfield.tests.base import \
    LocationFieldFunctionalTestCase

def test_suite():
    return unittest.TestSuite([
        ztc.FunctionalDocFileSuite(
            'locationfield.txt',
            package='kg.locationfield.tests',
            test_class=LocationFieldFunctionalTestCase,
            optionflags= doctest.REPORT_ONLY_FIRST_FAILURE | \
                doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
    ])
