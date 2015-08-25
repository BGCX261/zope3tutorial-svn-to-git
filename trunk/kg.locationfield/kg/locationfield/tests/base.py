from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

ztc.installProduct('PloneFormGen')

@onsetup
def setup_package():
    # roadrunner is not working without these 2 lines
    import Products.PloneFormGen
    zcml.load_config('configure.zcml', Products.PloneFormGen)

    fiveconfigure.debug_mode = True
    import kg.locationfield
    zcml.load_config('configure.zcml',
        kg.locationfield)
    fiveconfigure.debug_mode = False

    ztc.installPackage('kg.locationfield')

setup_package()
ptc.setupPloneSite(products=['kg.locationfield',])


class LocationFieldTestCase(ptc.PloneTestCase):
    """Common test base class"""


class LocationFieldFunctionalTestCase(ptc.FunctionalTestCase):
    """Common functional test base class"""
