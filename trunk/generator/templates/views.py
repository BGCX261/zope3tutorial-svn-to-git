
from templet import stringfunction

@stringfunction
def GenFile(DSLModel, Table, View):
    """
import copy

from zope.formlib import form
from zope.traversing.browser import absoluteURL

import ${View.TableName}_db
from interfaces import ${View.interface_name}

class AddBase(form.AddForm):
    label="Add: ${View.TableName}"
    form_fields = form.Fields(${View.interface_name})${View.create_omit}

    def create(self, data):
        table = ${View.TableName}_db.${View.TableName}(self.context)
${{
    if Table['primary_key_has_sequence']:
        out.append("\t\tdata['%s'] = table.NextPrimaryKey()[0].%s\\n" % (View.primary_key, View.primary_key))
}}        
        table.Create(**data)
        self.${View.primary_key} = data['${View.primary_key}']

    def add(self, object):
        self.request.response.redirect(
            absoluteURL(self.context.__parent__, self.request) +
            '/%s/@@SelectedManagementView.html'% self.${View.primary_key})

class EditBase(form.EditForm):
    label="Edit: ${View.TableName}"
    form_fields = form.Fields(${View.interface_name})${View.update_omit}

    @form.action('Save', name='save')
    def handle_save(self, action, data):
        table = ${View.TableName}_db.${View.TableName}(self.context)
        res = table.Update(${View.primary_key} = self.context.${View.primary_key}, **data)
        self.context.LoadFromDatabase(self.context, self.request)

class ViewBase(form.EditForm):
    label="View: ${View.TableName}"
    form_fields = form.Fields(${View.interface_name})${View.update_omit}

    for field in form_fields:
        field.field = copy.copy(field.field)
        field.field.readonly=True

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

    <browser:addMenuItem
        title="${View.TableName}"
        class=".${View.TableName}_content.${View.TableName}"
        view="${View.TableName}.add${View.TableName}"
        permission="zope.ManageContent"
        />

    <browser:page
        name="index.html"
        for=".interfaces.${View.interface_name}"
        class=".${View.TableName}_views.View"
        permission="zope.Public"
        menu="zmi_views" title="View"
        />

    <browser:page
        name="edit.html"
        for=".interfaces.${View.interface_name}"
        class=".${View.TableName}_views.Edit"
        permission="zope.Public"
        menu="zmi_views" title="Edit"
        />

    <browser:page
        for="zope.app.container.interfaces.IAdding"
        name="${View.TableName}.add${View.TableName}"
        class=".${View.TableName}_views.Add"
        permission="zope.ManageContent"
        />

    <browser:containerViews
        for=".interfaces.${View.interface_name}Container"
        add="zope.ManageContent"
        contents="zope.View"
        index="zope.View"
        />

"""
