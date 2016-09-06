# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from tdf.exttempsitepolicy.testing import TDF_EXTTEMPSITEPOLICY_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that tdf.exttempsitepolicy is properly installed."""

    layer = TDF_EXTTEMPSITEPOLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if tdf.exttempsitepolicy is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'tdf.exttempsitepolicy'))

    def test_browserlayer(self):
        """Test that ITdfExttempsitepolicyLayer is registered."""
        from tdf.exttempsitepolicy.interfaces import (
            ITdfExttempsitepolicyLayer)
        from plone.browserlayer import utils
        self.assertIn(ITdfExttempsitepolicyLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = TDF_EXTTEMPSITEPOLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['tdf.exttempsitepolicy'])

    def test_product_uninstalled(self):
        """Test if tdf.exttempsitepolicy is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'tdf.exttempsitepolicy'))

    def test_browserlayer_removed(self):
        """Test that ITdfExttempsitepolicyLayer is removed."""
        from tdf.exttempsitepolicy.interfaces import ITdfExttempsitepolicyLayer
        from plone.browserlayer import utils
        self.assertNotIn(ITdfExttempsitepolicyLayer, utils.registered_layers())
