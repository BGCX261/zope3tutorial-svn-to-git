
import types

from templet import stringfunction

@stringfunction
def GenFile(DSLModel, Table, View):
    """
from zope.interface import Interface
from zope.component import getMultiAdapter
from zope import schema
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.traversing.browser.interfaces import IAbsoluteURL

from zc.table import table, column

from ${DSLModel['GENERAL']['target_folder']}.${Table['name']} import MessageFactory as _

import ${View.TableName}_db

from z3c.form import form, button
Fields = form.field.Fields
from z3c.formui.form import Form

class ISearchActions(Interface):
    search = button.Button(title=u'Search')
    delete = button.Button(title=u'Delete')

class ISearchSchema(Interface):
    "Search Interface for this Container"
${{
for row in [col for col in Table['columns'] if col['colname'] in Table['search_columns']]:
    out.append('\t%s = %s(' % (row['colname'], row['schema_type']))

    for (k,v) in row['schema_fields'].items():
        if k in ['readonly', 'required']: continue
        if type(v) in types.StringTypes:
            out.append("%s=_(u'%s'), " % (k,v))
        else:
            out.append("%s=%s, " % (k,v))
    out.append("required=False, ")
    if row.has_key('value_type'):
        out.append("\\n\t\tvalue_type=%s(" % row['value_type'])
        for (k,v) in row['value_type_fields'].items():
            if type(v) in types.StringTypes:
                out.append("%s=_(u'%s'), " % (k,v))
            else:
                out.append("%s=%s, " % (k,v))
        out.append(')  ')
    out.append(')\\n')
}}


class SearchBase(Form):

    template=ViewPageTemplateFile("templates/list.pt")

    fields = Fields(ISearchSchema)

    label = "Search"

    buttons = button.Buttons(ISearchActions)
    search_buttons=['search']
    result_buttons=['delete']

    # Don't look to the context object for data
    ignoreContext = True

    Columns = [
${{
for row in [col for col in Table['columns'] if col['colname'] in Table['search_columns']]:
    if row['colname'] != View.primary_key:
        if row['dbtype'].find('character') == -1:
            out.append("\t\tcolumn.GetterColumn(title='%s', getter=lambda p,f: p.%s == None and '' or str(p.%s)),\\n"
                % (row['colname'], row['colname'], row['colname']))
        else:
            out.append("\t\tcolumn.GetterColumn(title='%s', getter=lambda p,f: p.%s and p.%s.decode('latin1') or ''),\\n"
                % (row['colname'], row['colname'], row['colname']))
}}
    ]

    def idLink(self, item, formatter):
        return '<a href="%s/%s">%s</a>'%(self.context_absolute_url, item.${View.primary_key}, item.${View.primary_key})

    def checkBox(self, item, formmater):
        return '<input class="noborder slaveBox" name="ids:list" id="%s" value="%s" type="checkbox">' % (
            item.${View.primary_key}, item.${View.primary_key})

    def __init__(self, context, request):
        super(SearchBase, self).__init__(context, request)
        self.results=[]
        self.context_absolute_url = getMultiAdapter((context, request), IAbsoluteURL)

    def renderResults(self):
        if not self.results:
            return ''

        # the first row references back into the class so the columns array must
        # be local to the class
        columns = [
            column.GetterColumn(title="", getter=self.checkBox),
            column.GetterColumn(title="${View.primary_key}", getter=self.idLink),
        ] + self.Columns

        formatter = table.StandaloneFullFormatter(self.context, self.request,
               self.results, prefix="form", columns=columns)
        formatter.cssClasses['table'] = 'listing'
        return formatter()

    @button.handler(ISearchActions['search'])
    def handle_search(self, action):
        "Create the result set, but the Template formats them"

        data, errors = self.extractData()

        table = ${View.TableName}_db.${View.TableName}(self.context)
        self.results= table.Search(**data)

    @button.handler(ISearchActions['delete'])
    def handle_delete(self, action):
        # The items to delete must be read from the request.form list,
        # since they are not form widgets and are not on form_fields
        try:
            ids = self.request.form[u'ids']
        except:
            return
        if len(ids) > 0:
            table = ${View.TableName}_db.${View.TableName}(self.context)
            for id in ids:
                table.Delete(${View.primary_key}=id)

# CAN_EDIT_AFTER_THIS_LINE

class Search(SearchBase):
    pass


"""


@stringfunction
def GenConfiguration(DSLModel, Table, View):
    r"""
<!-- Search Configuration -->

    <z3c:pagelet
        name="search.html"
        for=".interfaces.${View.interface_name}Container"
        class=".${View.TableName}_search.Search"
        permission="zope.ManageContent"
        ${View.z3c_layer} />

    <browser:menuItem
        title="Search"
        for=".interfaces.${View.interface_name}Container"
        menu="zmi_views"
        action="search.html"
        permission="zope.ManageContent"
        />

"""

@stringfunction
def GenTemplate(DSLModel, Table, View):
    r"""
    <h1 tal:content="view/label" i18n:translate="">Contents</h1>

    <div class="summary" tal:condition="view/status"
       tal:content="view/status" i18n:translate="">Status</div>

    <form class="edit-form" enctype="multipart/form-data" method="post"
          action="." tal:attributes="action request/URL">

        <table>
          <tal:block omit-tag="" repeat="widget view/widgets/values">
            <tr metal:define-macro="formrow" class="row"
                tal:condition="python:widget.mode != 'hidden'">
              <td class="label" metal:define-macro="labelcell">
                <label tal:attributes="for widget/id">
                  <span i18n:translate=""
                        tal:content="widget/label"> label </span>
                  <span class="required"
                        tal:condition="widget/required"> * </span>
                </label>
              </td>
              <td class="field" metal:define-macro="widgetcell">
                <div class="widget" tal:content="structure widget/render">
                  <input type="text" />
                </div>
                <div class="error"
                     tal:condition="widget/error">
                  <span tal:replace="structure widget/error"> error </span>
                </div>
              </td>
            </tr>
          </tal:block>
        </table>

      <div class="buttons">
        <input tal:repeat="action view/search_buttons"
               tal:replace="structure python:view.actions[action].render()" />
      </div>
    </form>

    <form tal:condition="view/renderResults"
          class="edit-form" enctype="multipart/form-data" method="post"
          action="." tal:attributes="action request/URL">

        <h2>Search Results</h2>
        <span tal:replace="structure view/renderResults"></span>

      <div class="buttons">
        <input tal:repeat="action view/result_buttons"
               tal:replace="structure python:view.actions[action].render()" />
      </div>
    </form>

"""
