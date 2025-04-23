# -*- coding: utf-8 -*-
"""Setup handlers for plone.mls.listing."""

from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        items = [
            'plone.mls.listing:uninstall',
        ]

        return items
