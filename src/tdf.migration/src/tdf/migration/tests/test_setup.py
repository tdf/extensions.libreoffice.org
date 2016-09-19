# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from tdf.migration.testing import TDF_MIGRATION_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that tdf.migration is properly installed."""

    layer = TDF_MIGRATION_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if tdf.migration is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'tdf.migration'))

    def test_browserlayer(self):
        """Test that ITdfMigrationLayer is registered."""
        from tdf.migration.interfaces import (
            ITdfMigrationLayer)
        from plone.browserlayer import utils
        self.assertIn(ITdfMigrationLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = TDF_MIGRATION_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['tdf.migration'])

    def test_product_uninstalled(self):
        """Test if tdf.migration is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'tdf.migration'))

    def test_browserlayer_removed(self):
        """Test that ITdfMigrationLayer is removed."""
        from tdf.migration.interfaces import ITdfMigrationLayer
        from plone.browserlayer import utils
        self.assertNotIn(ITdfMigrationLayer, utils.registered_layers())
