
from templet import stringfunction

@stringfunction
def GenFile(DSLModel, Table, View):
    """
from zope.component import getMultiAdapter
from zope.app.container.interfaces import INameChooser
from zope.app.container.interfaces import IAdding
from zope.traversing.browser.interfaces import IAbsoluteURL

from z3c.form import form
from z3c.formui.form import EditForm, AddForm, DisplayForm

Fields = form.field.Fields

import ${View.TableName}_content
from interfaces import ${View.interface_name}

class AddBase(AddForm):
    label="Add: ${View.TableName}"
    fields = Fields(${View.interface_name})${View.create_omit}

    def __init__(self, context, request):
        super(AddBase, self).__init__(context, request)

        if IAdding.providedBy(self.context):
            self.container = self.context.context
        else:
            self.container = self.context

    def create(self, data):
        # Create object
        newobj = ${View.TableName}_content.${View.TableName}()
${{
for row in Table['columns']:
    if row['colname'] == View.primary_key: continue
    out.append("\t\tnewobj.%s = data['%s']\\n" % (row['colname'], row['colname']))
}}

        # Name it - must be done at this stage for event subscribers
        nc = INameChooser(self.container)
        newobj.__name__ = nc.chooseName('', newobj)

        return newobj

    def add(self, object):
        self.new_object_id = object.__name__
        self.container[object.__name__] = object
        return object

    def nextURL(self):
        container_url = getMultiAdapter((self.container, self.request), IAbsoluteURL)
        return '%s/%s/index.html'% (str(container_url), self.new_object_id)


class EditBase(EditForm):
    label="Edit: ${View.TableName}"
    fields = Fields(${View.interface_name})${View.update_omit}

class ViewBase(DisplayForm):
    label="View: ${View.TableName}"
    fields = Fields(${View.interface_name})${View.update_omit}

# CAN_EDIT_AFTER_THIS_LINE

${{
for classname in View.classnames:
    out.append('class %s(%sBase):\\n' % (classname, classname))
    out.append('\tpass\\n\\n')
}}
"""

@stringfunction
def GenConfiguration(DSLModel, Table, View):
    r"""
<!-- View Configuration -->
    <z3c:pagelet
        name="index.html"
        for=".interfaces.${View.interface_name}"
        class=".${View.TableName}_views.View"
        permission="zope.Public"
        ${View.z3c_layer}/>

    <browser:menuItem
        title="View"
        for=".interfaces.${View.interface_name}"
        menu="zmi_views"
        action="@@index.html"
        permission="zope.Public"
        />

    <z3c:pagelet
        name="edit.html"
        for=".interfaces.${View.interface_name}"
        class=".${View.TableName}_views.Edit"
        permission="zope.Public"
        ${View.z3c_layer}/>

    <browser:menuItem
        title="Edit"
        for=".interfaces.${View.interface_name}"
        menu="zmi_views"
        action="@@edit.html"
        permission="zope.ManageContent"
        />

    <z3c:pagelet
        for="zope.app.container.interfaces.IAdding"
        name="add${View.TableName}.html"
        class=".${View.TableName}_views.Add"
        permission="zope.ManageContent"
        ${View.z3c_layer}/>

    <browser:addMenuItem
        title="Add ${View.TableName}"
        class=".${View.TableName}_content.${View.TableName}"
        permission="zope.ManageContent"
        view="add${View.TableName}.html"
        ${View.z3c_layer}/>

    <browser:containerViews
        for=".interfaces.${View.interface_name}Container"
        add="zope.ManageContent"
        contents="zope.View"
        index="zope.View"
        ${View.z3c_layer}/>

"""

