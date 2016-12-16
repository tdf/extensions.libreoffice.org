# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces.controlpanel import IMailSchema
from tdf.exttempsitepolicy.testing import TDF_EXTTEMPSITEPOLICY_INTEGRATION_TESTING  # noqa
from tdf.extensionuploadcenter.euprelease import ValidateEUpReleaseUniqueness
from tdf.extensionuploadcenter.eupreleaselink import ValidateEUpReleaseLinkUniqueness
from tdf.extensionuploadcenter.euprelease import IEUpRelease
from tdf.extensionuploadcenter.eupreleaselink import IEUpReleaseLink
from tdf.extensionuploadcenter.adapter import IReleasesCompatVersions
from tdf.templateuploadcenter.tuprelease import ValidateTUpReleaseUniqueness
from tdf.templateuploadcenter.tupreleaselink import ValidateTUpReleaseLinkUniqueness
from tdf.templateuploadcenter.tuprelease import ITUpRelease
from zope.component import getUtility
from zope.event import notify
from zope.interface import Invalid
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent import ObjectRemovedEvent

import unittest


class TestExtensionsValidators(unittest.TestCase):
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

    def test_extension_releases(self):
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
        project2 = api.content.create(
            center,
            'tdf.extensionuploadcenter.eupproject',
            title='project2'
        )
        release2 = api.content.create(
            project2,
            'tdf.extensionuploadcenter.euprelease',
            title='release2',
            releasenumber=u'2.0'
        )

        # Test the index
        pc = api.portal.get_tool('portal_catalog')
        result = pc.searchResults(portal_type="tdf.extensionuploadcenter.euprelease")
        self.assertTrue(result[0].release_number, u'1.0')

        # Trying to create other release with the same release number will trigger
        # on creation
        validator = ValidateEUpReleaseUniqueness(
            project,
            self.request,
            None,
            IEUpRelease['releasenumber'],
            None
        )
        self.assertRaises(Invalid, validator.validate, u'1.0')
        self.assertIsNone(validator.validate(u'2.0'))

        # Trying to create other release with the same release number will trigger
        # on editing
        validator = ValidateEUpReleaseUniqueness(
            release,
            self.request,
            None,
            IEUpRelease['releasenumber'],
            None
        )
        self.assertIsNone(validator.validate(u'1.0'))
        self.assertIsNone(validator.validate(u'2.0'))

        releaselink = api.content.create(
            project,
            'tdf.extensionuploadcenter.eupreleaselink',
            title='releaselink'
        )

        # on creation
        validatorlink = ValidateEUpReleaseLinkUniqueness(
            project,
            self.request,
            None,
            IEUpReleaseLink['releasenumber'],
            None
        )
        self.assertRaises(Invalid, validatorlink.validate, u'1.0')
        self.assertIsNone(validatorlink.validate(u'3.0'))

        # on editing
        validatorlink = ValidateEUpReleaseLinkUniqueness(
            releaselink,
            self.request,
            None,
            IEUpReleaseLink['releasenumber'],
            None
        )
        self.assertIsNone(validatorlink.validate(u'2.0'))
        self.assertIsNone(validatorlink.validate(u'3.0'))


class TestTemplateValidators(unittest.TestCase):
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

    def test_templates_releases(self):
        center = api.content.create(
            self.portal,
            'tdf.templateuploadcenter.tupcenter',
            title='center'
        )
        project = api.content.create(
            center,
            'tdf.templateuploadcenter.tupproject',
            title='project'
        )
        release = api.content.create(
            project,
            'tdf.templateuploadcenter.tuprelease',
            title='release'
        )

        # Test the index
        pc = api.portal.get_tool('portal_catalog')
        result = pc.searchResults(portal_type="tdf.templateuploadcenter.tuprelease")
        self.assertTrue(result[0].release_number, u'1.0')

        # Trying to create other release with the same release number will trigger
        # on creation
        validator = ValidateTUpReleaseUniqueness(
            project,
            self.request,
            None,
            ITUpRelease['releasenumber'],
            None
        )
        self.assertRaises(Invalid, validator.validate, u'1.0')
        self.assertIsNone(validator.validate(u'2.0'))

        # Trying to create other release with the same release number will trigger
        # on editing
        validator = ValidateTUpReleaseUniqueness(
            release,
            self.request,
            None,
            IEUpRelease['releasenumber'],
            None
        )
        self.assertIsNone(validator.validate(u'1.0'))
        self.assertIsNone(validator.validate(u'2.0'))

        releaselink = api.content.create(
            project,
            'tdf.templateuploadcenter.tupreleaselink',
            title='releaselink'
        )

        # on creation
        validatorlink = ValidateTUpReleaseLinkUniqueness(
            project,
            self.request,
            None,
            IEUpReleaseLink['releasenumber'],
            None
        )
        self.assertRaises(Invalid, validatorlink.validate, u'1.0')
        self.assertIsNone(validatorlink.validate(u'3.0'))

        # on editing
        validatorlink = ValidateTUpReleaseLinkUniqueness(
            releaselink,
            self.request,
            None,
            IEUpReleaseLink['releasenumber'],
            None
        )
        self.assertIsNone(validatorlink.validate(u'2.0'))
        self.assertIsNone(validatorlink.validate(u'3.0'))

    def test_releases_compat_adapter(self):
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

        self.assertEquals(IReleasesCompatVersions(project).get(), [])
        list1 = ['1', '2']
        IReleasesCompatVersions(project).update(list1)
        self.assertEquals(IReleasesCompatVersions(project).get(), list1)
        list2 = ['1', '2', '3']
        IReleasesCompatVersions(project).update(list2)
        self.assertEquals(len(IReleasesCompatVersions(project).get()), 3)

    def test_releases_compat_add_event(self):
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
            title='release',
            compatibility_choice=['LibreOffice 5.1', ]
        )

        self.assertEquals(IReleasesCompatVersions(project).get(), ['LibreOffice 5.1', ])

    def test_releases_compat_modify_event(self):
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
            title='release',
            compatibility_choice=['LibreOffice 5.1', 'LibreOffice 5.2', ]
        )
        release2 = api.content.create(
            project,
            'tdf.extensionuploadcenter.euprelease',
            title='release2',
            compatibility_choice=['LibreOffice 5.2', ]
        )

        # release.reindexObject(idxs=['getCompatibility'])
        notify(ObjectModifiedEvent(release))
        releases = IReleasesCompatVersions(project).get()
        self.assertTrue('LibreOffice 5.1' in releases)
        self.assertTrue('LibreOffice 5.2' in releases)

        release.compatibility_choice = ['LibreOffice 5.2', ]
        release.reindexObject(idxs=['getCompatibility'])
        notify(ObjectModifiedEvent(release))
        releases = IReleasesCompatVersions(project).get()
        self.assertTrue('LibreOffice 5.1' not in releases)
        self.assertTrue('LibreOffice 5.2' in releases)

    def test_releases_compat_delete_event(self):
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
            title='release',
            compatibility_choice=['LibreOffice 5.1', 'LibreOffice 5.2', ]
        )
        release2 = api.content.create(
            project,
            'tdf.extensionuploadcenter.euprelease',
            title='release2',
            compatibility_choice=['LibreOffice 5.2', ]
        )

        releases = IReleasesCompatVersions(project).get()
        self.assertTrue('LibreOffice 5.1' in releases)
        self.assertTrue('LibreOffice 5.2' in releases)

        api.content.delete(release)

        notify(ObjectRemovedEvent(release))
        releases = IReleasesCompatVersions(project).get()
        self.assertTrue('LibreOffice 5.1' not in releases)
        self.assertTrue('LibreOffice 5.2' in releases)
