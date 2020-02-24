# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from tdf.extensioncentertheme.testing import TDF_EXTENSIONCENTERTHEME_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that tdf.extensioncentertheme is properly installed."""

    layer = TDF_EXTENSIONCENTERTHEME_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if tdf.extensioncentertheme is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'tdf.extensioncentertheme'))

    def test_browserlayer(self):
        """Test that ITdfExtensioncenterthemeLayer is registered."""
        from tdf.extensioncentertheme.interfaces import (
            ITdfExtensioncenterthemeLayer)
        from plone.browserlayer import utils
        self.assertIn(ITdfExtensioncenterthemeLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = TDF_EXTENSIONCENTERTHEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['tdf.extensioncentertheme'])

    def test_product_uninstalled(self):
        """Test if tdf.extensioncentertheme is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'tdf.extensioncentertheme'))

    def test_browserlayer_removed(self):
        """Test that ITdfExtensioncenterthemeLayer is removed."""
        from tdf.extensioncentertheme.interfaces \
            import ITdfExtensioncenterthemeLayer
        from plone.browserlayer import utils
        self.assertNotIn(ITdfExtensioncenterthemeLayer,
                         utils.registered_layers())
