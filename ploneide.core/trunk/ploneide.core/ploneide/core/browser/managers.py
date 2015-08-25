

from five import grok
 
from ploneide.core import IPloneIDE


class PloneIDENavigatorViewletManager(grok.ViewletManager):
    """The manager for the left hand side navigation panel.

    To implement your own navigator...

    from five import grok
    from ploneide.core import PloneIDENavigatorViewletManager

    class MyNavigator(grok.Viewlet):
        grok.name('mynavigator')
        grok.require('cmf.ManagePortal')
        grok.viewletmanager(PloneIDENavigatorViewletManager)

        # Viewlets should contain a 'weight' attribute to manage ordering.
        grok.order(200)

        def render(self):
            # Navigator must provide code to fit into the jstree structure.
            return '<h2>title</h2><div>Body</div>'
                    

    """
    grok.name('ploneide.core.Navigator')
    grok.context(IPloneIDE)


class PloneIDEJSViewletManager(grok.ViewletManager):
    """The manager for including javascript resources into the editor. This manager
    will be rendered in the head,

    Jquery should be included at 10
    ploneide.js should be included at 100
    bespin editor plugin should be included at 1000

    To include your own javascript - TODO: see how to do this directly with a resource declaration

    To include your own javascript...

    from five import grok
    from ploneide.core import PloneIDEJSViewletManager

    class MyJSResource(grok.Viewlet):
        grok.name('my-js-resource')
        grok.require('cmf.ManagePortal')
        grok.viewletmanager(PloneIDEJSViewletManager)

        # Viewlets should contain a 'weight' attribute to manage ordering.
        grok.order(200)

        def render(self):
            return '<script type="text/javascript" src="your path"></script>' 
                    

    """
    grok.name('ploneide.core.JS')
    grok.context(IPloneIDE)


class PloneIDECSSViewletManager(grok.ViewletManager):
    """The manager for including CSS resources into the editor. This manager
    will be rendered in the head,

    ploneide.css should be included at 100

    To include your own CSS...

    from five import grok
    from ploneide.core import PloneIDECSSViewletManager

    class MyCSSResource(grok.Viewlet):
        grok.name('my-css-resource')
        grok.require('cmf.ManagePortal')
        grok.viewletmanager(PloneIDECSSViewletManager)

        # Viewlets should contain a 'weight' attribute to manage ordering.
        grok.order(200)

        def render(self):
            return '<style type="text/css">@import url(my-css-path);</style>' 

    """
    grok.name('ploneide.core.CSS')
    grok.context(IPloneIDE)


class PloneIDEToolViewletManager(grok.ViewletManager):
    """The manager for including html into the tools area, i.e. the bottom of the page.

    To implement your own tool...

    from five import grok
    from ploneide.core import PloneIDEToolViewletManager

    class MyTool(grok.Viewlet):
        grok.name('my-tool')
        grok.require('cmf.ManagePortal')
        grok.viewletmanager(PloneIDEToolViewletManager)

        # Viewlets should contain a 'weight' attribute to manage ordering.
        grok.order(200)

        def render(self):
            # tools must provide code to fit into the jstree structure.
            return '<h2>title</h2><div>Body</div>'

    """
    grok.name('ploneide.core.Tool')
    grok.context(IPloneIDE)
