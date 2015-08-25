from AccessControl import ClassSecurityInfo

from Products.CMFCore.permissions import View
from Products.CMFCore.Expression import getExprContext
from Products.Archetypes.atapi import Schema
from Products.Archetypes.Field import StringField
from Products.Archetypes.Widget import StringWidget
from Products.ATContentTypes.content.base import registerATCT

from Products.Maps.field import LocationField, LocationWidget

from Products.TALESField import TALESString
from Products.PloneFormGen.content.fieldsBase import finalizeFieldSchema, BaseFieldSchema, BaseFormField

from kg.locationfield.config import PROJECTNAME
from zope.component import getMultiAdapter

class MyLocationField(LocationField):
        # There is a massive problem in the retrieval of data from the object. Need 
        # to track it via the normal mechanism
        accessor = "dummy_accessor"
        def dummy_accessor(self):
            if self.tmp_value == None:
                return self.default
            return self.tmp_value

        def getAccessor(self, context):
            return self.dummy_accessor


class FGLocationField(BaseFormField):
    """ A string entry field """

    security  = ClassSecurityInfo()

    schema = BaseFieldSchema.copy() 

    # hide references & discussion
    finalizeFieldSchema(schema, folderish=True, moveDiscussion=False)

    # Standard content type setup
    portal_type = meta_type = 'FormLocationField'
    archetype_name = 'Location Field'
    content_icon = 'location_icon.gif'
    typeDescription= 'A location field'

    def __init__(self, oid, **kwargs):
        """ initialize class """

        super(BaseFormField, self).__init__(oid, **kwargs)

        # set a preconfigured field as an instance attribute
        self.fgField = MyLocationField('fg_location_field',
            languageIndependent = 1,
            default_method="getDefaultLocation",
            required=True,
            write_permission = View,
            validators=('isGeoLocation',),
            tmp_value = None,
            widget=LocationWidget(
               label='Location',
            ),
        )

    def fgPrimeDefaults(self, request, contextObject=None):
        """ primes request with default value"""

        BaseFormField.fgPrimeDefaults(self, request, contextObject)

        form_val = request.get(self.fgField.__name__, None)
        if form_val:
            self.fgField.tmp_value = form_val
        else:
            config = getMultiAdapter((self, request), name="maps_configuration")
            self.fgField.tmp_value = config.default_location
            request.form.setdefault(self.fgField.__name__, self.fgField.tmp_value)

registerATCT(FGLocationField, PROJECTNAME)
