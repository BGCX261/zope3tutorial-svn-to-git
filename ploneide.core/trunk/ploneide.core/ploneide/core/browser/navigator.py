
"""
    Simple navigator to allow easy navigation of code in 
    the file system.
"""

import os
import os.path

from zope.publisher.interfaces import IRequest

from five import grok

from ploneide.core import PloneIDENavigatorViewletManager
from ploneide.core import PloneIDEJSViewletManager
from ploneide.core import IPloneIDE
from ploneide.core import IPloneIDEModel

class FileSystemNavigator(grok.Viewlet):
    grok.name('navigator-filesystem')
    grok.require('cmf.ManagePortal')
    grok.context(IPloneIDE)
    grok.viewletmanager(PloneIDENavigatorViewletManager)

    grok.order(100)

    def render(self):
        # Navigator must provide code to fit into the jstree structure.
        return """
            <h2 class="current">Files</h2>
            <div style="display:block" class="pane">
                <p style="color:#333">Files in ./src folder:</p>
                <div id="tree"></div>
            </div>"""

class FileSystemNavigatorResources(grok.Viewlet):
    """jquery.jstree is in the static folder"""
    grok.name('navigator-filesystem')
    grok.require('cmf.ManagePortal')
    grok.viewletmanager(PloneIDEJSViewletManager)
    grok.context(IPloneIDE)

    grok.order(200)
    
    def render(self):
        rv = [
            """<script src="%s/++resource++ploneide.core/ploneide-fs-navigator.js" type="text/javascript"></script>""" % self.context.portal_url(),
            """<script src="%s/++resource++ploneide.core/ploneide-edit-bespin.js" type="text/javascript"></script>""" % self.context.portal_url(),
            ]
        return '\n'.join(rv)

class FileSystemHandler(grok.MultiAdapter):
        grok.adapts(IPloneIDE, IRequest)
        grok.provides(IPloneIDEModel)
        grok.name('navigator-filesystem')

        def __init__(self, context, request):
            self.context = context
            self.request = request

        def handle(self, type_name, method_name, form):
            """The filesystem should be built using ajax to reduce load.
            This method should be called to build the tree"""
            try:
                method = getattr(self, method_name)
            except:
                raise NotImplemented

            return method()

        ## methods implementing the services

        def _included(self, filename):
            """Used to exclude files and folders"""
            if filename.startswith('.'):
                return False
            for suffix in ['.pyc', '.pyo', '.egg-info', '.swp', '~', '.pt.py', '.tmp', '.save', 'PKG-INFO', 'SOURCES.txt', '.#']:
                if filename.endswith(suffix):
                    return False
            return True

        def _is_editable(self, filename):
            for suffix in ['.png', '.jpg', 'gif', 'swf']:
                if filename.endswith(suffix):
                    return False
            return True

        def _recurse_folder(self, folder, is_project=False):
            """recurse the path adding items the output"""
            children = []
            dirs = []
            for filename in sorted(os.listdir(folder)):
                if not self._included(filename):
                    continue
                if os.path.isdir(folder + os.sep + filename):
                    dirs.append(filename)
                else:
                    children.append({'data': {
                            'title': filename,
                            'attr': {}
                        },
                        'attr': {'id': 'navigator-filesystem:' + folder + os.sep + filename}
                    })
            for dirname in dirs:
                children.append(self._recurse_folder(folder + os.sep + dirname))
            return {
                'data': {
                'title': os.path.basename(folder),
                'attr': {
                    'isFolder': True,
                    'lineNumber': 1,
                    },
                },
                'attr': {'id': 'navigator-filesystem:' + folder},
                'children': children}

        def _isProject(self, folder):
            """If the path represents a project, return True, else False"""
            if os.path.isdir(folder) and os.path.exists(folder + os.sep + 'setup.py'):
                return True
            return False

        def getNavigation(self):
            """Return a structure containing the navigation, as used by dynatree
            """
            rv = []
            srcdir = os.getcwd() + os.sep + 'src'
            for folder in os.listdir(srcdir):
                if self._isProject(srcdir + os.sep + folder):
                    rv.append(self._recurse_folder(srcdir + os.sep + folder, True))
            return rv

        def getFile(self):
            """retrieve a file - return it with some other information"""
            filename = self.request.get('filename', None)
            if filename is None:
                raise NotImplemented
            payload = open(filename).read()
            syntax = None
            model = None
            if filename.endswith('.py'):
                model = syntax = 'py'
            elif filename.endswith('.pt'):
                syntax = 'html'
                model = 'pt'
            elif filename.endswith('.zcml'):
                syntax = 'html'
                model = 'zcml'
            elif filename.endswith('.txt'):
                syntax = model = 'txt'
            elif filename.endswith('.css'):
                syntax = model = 'css'
            elif filename.endswith('.js'):
                model = 'js'
                syntax = 'javascript'
            else:
                syntax = 'auto'
                model = 'txt'
            return {
                'filename': filename,
                'syntax': syntax,
                'model': model,
                'payload': payload,
                'readonly': False
            }


