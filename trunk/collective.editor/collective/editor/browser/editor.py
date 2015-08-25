
from five import grok

from Products.CMFPlone.interfaces import IPloneSiteRoot

try:
    import json
except:
    import simplejson as json

import os
import os.path

class SimpleEditor(grok.View):
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')
    title = "Simple Code Editor"

    def __init__(self, context, request):
        super(SimpleEditor, self).__init__(context, request)

    def __call__(self):
        if self.request.get('requestType', None) == 'ajax':
            requestId = self.request.get('requestId', None)

            if requestId is None or requestId.startswith('_'):
                raise NotImplemented
            try:
                method = getattr(self, requestId)
            except:
                raise NotImplemented

            rv = method()
            if type(rv) in [str, unicode]:
                return rv
            else:
                self.request.response.setHeader('content-type', 'text/json')
                return json.dumps(rv)

        return super(SimpleEditor, self).__call__()

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
                    'attr': {'id': (self._is_editable(filename) and 'file:' or 'binary:') + folder + os.sep + filename}
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
            'attr': {'id': (is_project and 'project:' or 'folder:') + folder},
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
        if filename.endswith('.py'):
            syntax = 'py'
        elif filename.endswith('.pt'):
            syntax = 'html'
        elif filename.endswith('.js'):
            syntax = 'javascript'
        else:
            syntax = 'auto'
        return {
            'filename': filename,
            'syntax': syntax,
            'payload': payload,
            'readonly': False
        }

