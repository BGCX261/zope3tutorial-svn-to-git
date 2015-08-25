
"""
    This view should construct the editor
"""

from ploneide.core import IPloneIDE
from ploneide.core import PloneIDEJSViewletManager
from ploneide.core import PloneIDECSSViewletManager
from ploneide.core import PloneIDENavigatorViewletManager

from five import grok

class Editor(grok.View):
    grok.context(IPloneIDE)
    grok.require('cmf.ManagePortal')
    

class JQueryTreeResources(grok.Viewlet):
    """jquery.jstree is in the static folder"""
    grok.name('jquery.jstree')
    grok.require('zope2.View')
    grok.viewletmanager(PloneIDEJSViewletManager)
    grok.context(IPloneIDE)

    grok.order(20)
    
    def render(self):
        return """<script src="%s/++resource++ploneide.core/jquery.jstree/jquery.jstree.js" type="text/javascript"></script>\n""" % self.context.portal_url()


class JQuerySplitterResources(grok.Viewlet):
    """jquery.splitter is in the static folder"""
    grok.name('jquery.splitter')
    grok.require('zope2.View')
    grok.viewletmanager(PloneIDEJSViewletManager)
    grok.context(IPloneIDE)

    grok.order(20)
    
    def render(self):
        return """<script src="%s/++resource++ploneide.core/jquery.splitter/splitter.js" type="text/javascript"></script>\n""" % self.context.portal_url()

class DefaultCSSResources(grok.Viewlet):
    """ploneide.css is in the static/css folder"""
    grok.name('ploneide.core.ploneide')
    grok.require('zope2.View')
    grok.viewletmanager(PloneIDECSSViewletManager)
    grok.context(IPloneIDE)

    grok.order(100)
    
    def render(self):
        return """<link rel="stylesheet" href="%s/++resource++ploneide.core/ploneide.css" type="text/css" />\n""" % self.context.portal_url()


class DefaultJSResources(grok.Viewlet):
    """ploneide.js is in the static/js folder"""
    grok.name('ploneide.core.ploneide')
    grok.require('zope2.View')
    grok.viewletmanager(PloneIDEJSViewletManager)
    grok.context(IPloneIDE)

    grok.order(100)
    
    def render(self):
        return """<link id="ploneide_base" href="%s" /> 
        <script src="%s/++resource++ploneide.core/ploneide.js" type="text/javascript"></script>""" % (self.context.absolute_url(),
            self.context.portal_url())


class JQueryBespinResources(grok.Viewlet):
    """bespin is in the static folder"""
    grok.name('bespin')
    grok.require('zope2.View')
    grok.viewletmanager(PloneIDEJSViewletManager)
    grok.context(IPloneIDE)

    grok.order(20)
    
    def render(self):
        return """<link id="bespin_base" href="%s/++resource++ploneide.core/bespin-0.9a1/" />
 <script src="%s/++resource++ploneide.core/bespin-0.9a1/BespinEmbedded.js" type="text/javascript"></script>\n""" % (
        self.context.portal_url(), self.context.portal_url())







