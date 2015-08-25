
#   This is the layer for registering z3c.form and z3c.pagelets against

import z3c.layer.pagelet
import z3c.form.interfaces

class IPageletLayer(
    z3c.form.interfaces.IFormLayer,
    z3c.layer.pagelet.IPageletBrowserLayer):
    pass
