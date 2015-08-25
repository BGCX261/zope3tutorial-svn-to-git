
from zope.viewlet import manager


class LeftViewletManager(manager.ConditionalViewletManager):
    """Ordered viewlet and Conditional."""

    def sort(self, viewlets):
        """Sort the viewlets on their weight."""
        return sorted(viewlets,
                      lambda x, y: cmp(x[1].getWeight(), y[1].getWeight()))

