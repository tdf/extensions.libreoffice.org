# -*- coding: utf-8 -*-
from plone import api
from Products.Five.browser import BrowserView
from tdf.exttempsitepolicy import _
from Acquisition import aq_inner, aq_parent


class frontpageView(BrowserView):

    """ The view of the LibreOffice extensions and templates frontpage
    """

    def tupproject_count(self):
        """Return number of projects
        """
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')

        return len(catalog(portal_type=('tdf.templateuploadcenter.tupproject',
                                        'tdf.templateuploadcenter.tupsmallproject')))

    def tuprelease_count(self):
        """Return number of downloadable files
        """
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')

        return len(catalog(portal_type='tdf.templateuploadcenter.tuprelease'))

    def get_newest_templateprojects(self):
        self.catalog = api.portal.get_tool(name='portal_catalog')
        sort_on = 'created'
        contentFilter = {
                          'sort_on': sort_on,
                          'sort_order': 'reverse',
                          'review_state': 'published',
                          'portal_type': ('tdf.templateuploadcenter.tupproject',
                                          'tdf.templateuploadcenter.tupsmallproject')}

        results = self.catalog(**contentFilter)

        return results

    def get_latest_template_releases(self):
        self.catalog = api.portal.get_tool(name='portal_catalog')
        sort_on = 'created'
        contentFilter = {'sort_on': sort_on,
                         'sort_order': 'reverse',
                         'review_state': 'final',
                         'portal_type': ('tdf.templateuploadcenter.tuprelease',
                                         'tdf.templateuploadcenter.tupreleaselink'),
                         }
        results = self.catalog(**contentFilter)
        return results

    def get_latest_temp_releases(self):
        published_projects = api.content.find(portal_type='tdf.templateuploadcenter.tupproject',
                                              review_state='published')
        release_uids = []
        for brain in published_projects:
            project = brain.getObject()
            release_uids += [brain.UID for brain in api.content.find(context=project,
                                                                     portal_type=('tdf.templateuploadcenter.tuprelease',
                                                                                  'tdf.templateuploadcenter.tupreleaselink'))]
        releases = api.content.find(UID=release_uids,
                                    review_state='final',
                                    sort_on='created',
                                    sort_order='reverse')

        return(releases)

    def eupproject_count(self):
        """Return number of projects
        """
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')

        return len(catalog(portal_type=('tdf.extensionuploadcenter.eupproject',
                                        'tef.extensionuploadcenter.eupsmallproject')))

    def euprelease_count(self):
        """Return number of downloadable files
        """
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')

        return len(catalog(portal_type='tdf.extensionuploadcenter.euprelease'))

    def get_newest_extensionprojects(self):
        self.catalog = api.portal.get_tool(name='portal_catalog')
        sort_on = 'created'
        contentFilter = {
                          'sort_on': sort_on,
                          'sort_order': 'reverse',
                          'review_state': 'published',
                          'portal_type': ('tdf.extensionuploadcenter.eupproject',
                                          'tdf.extensionuploadcenter.eupsmallproject')}

        results = self.catalog(**contentFilter)

        return results

    def get_latest_ext_releases(self):
        published_projects = api.content.find(portal_type='tdf.extensionuploadcenter.eupproject',
                                              review_state='published')
        release_uids = []
        for brain in published_projects:
            project = brain.getObject()
            release_uids += [brain.UID for brain in api.content.find(context=project,
                                                                     portal_type=('tdf.extensionuploadcenter.euprelease',
                                                                                  'tdf.extensionuploadcenter.eupreleaselink'))]
        releases = api.content.find(UID=release_uids,
                                    review_state='final',
                                    sort_on='created',
                                    sort_order='reverse')

        return(releases)
