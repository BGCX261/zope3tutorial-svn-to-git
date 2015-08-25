
import json
import logging

from zope.component import getMultiAdapter

from ploneide.core import IPloneIDE
from ploneide.core import IPloneIDEModel

from five import grok

logger = logging.getLogger('PloneIDE')

class Handler(grok.View):
    grok.context(IPloneIDE)
    grok.name('handler')
    grok.require('cmf.ManagePortal')

    def render(self):
        logger.info(self.request.form)

        type_name = self.request.get('type_name', None)
        if type_name is None:
            raise NotImplemented
        method_name = self.request.get('method_name', None)
        if method_name is None or method_name.startswith('_'):
            raise NotImplemented
        handler = getMultiAdapter((self.context, self.request), IPloneIDEModel, name=type_name)
        rv = handler.handle(type_name, method_name, self.request.form)
        if type(rv) in [str, unicode]:
            return rv
        else:
            self.request.response.setHeader('content-type', 'text/json')
            return json.dumps(rv)

    
