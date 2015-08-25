from zope.i18nmessageid import MessageFactory

_ = MessageFactory('ploneide.core')


from interfaces import IPloneIDE
from interfaces import IPloneIDEModel

# These are for including code from plugins into the rendered view
from browser.managers import PloneIDENavigatorViewletManager
from browser.managers import PloneIDEJSViewletManager
from browser.managers import PloneIDECSSViewletManager
from browser.managers import PloneIDEToolViewletManager
