
#   This is the layer for registering z3c.form and z3c.pagelets against

import z3c.layer.pagelet
import z3c.form.interfaces
from jquery.layer import IJQueryJavaScriptBrowserLayer


class IPageletLayer(
    z3c.form.interfaces.IFormLayer,
    IJQueryJavaScriptBrowserLayer,
    z3c.layer.pagelet.IPageletBrowserLayer):
    pass
