# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from tdf.exttempsitepolicy.testing import TDF_EXTTEMPSITEPOLICY_INTEGRATION_TESTING  # noqa
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from Products.CMFPlone.interfaces.controlpanel import IMailSchema

import unittest


class TestSetup(unittest.TestCase):
    """Test that tdf.exttempsitepolicy is properly installed."""

    layer = TDF_EXTTEMPSITEPOLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        registry = getUtility(IRegistry)
        mail_settings = registry.forInterface(
            IMailSchema, prefix='plone', check=False)
        mail_settings.smtp_host = u'localhost'
        mail_settings.email_from_address = 'whatever'

    def test_releases(self):
        center = api.content.create(
            self.portal,
            'tdf.extensionuploadcenter.eupcenter',
            title='center'
        )
        project = api.content.create(
            center,
            'tdf.extensionuploadcenter.eupproject',
            title='project'
        )
        release = api.content.create(
            project,
            'tdf.extensionuploadcenter.euprelease',
            title='release'
        )

        # Test the index
        pc = api.portal.get_tool('portal_catalog')
        result = pc.searchResults(portal_type="tdf.extensionuploadcenter.euprelease")
        self.assertTrue(result[0].release_number, u'1.0')

        # Trying to create other release with the same release number will trigger
        from tdf.extensionuploadcenter.euprelease import ValidateEUpReleaseUniqueness
        from tdf.extensionuploadcenter.euprelease import IEUpRelease
        from zope.interface import Invalid

        validator = ValidateEUpReleaseUniqueness(
            release,
            self.request,
            None,
            IEUpRelease['releasenumber'],
            None
        )
        self.assertRaises(Invalid, validator.validate, u'1.0')
        self.assertIsNone(validator.validate(u'2.0'))
