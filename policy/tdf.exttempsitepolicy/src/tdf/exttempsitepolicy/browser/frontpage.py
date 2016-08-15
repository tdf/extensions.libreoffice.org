# -*- coding: utf-8 -*-
from plone import api
from Products.Five.browser import BrowserView
from tdf.exttempsitepolicy import _
from Acquisition import aq_inner



class frontpageView(BrowserView):

    """ The view of the LibreOffice extensions and templates frontpage
    """



    def tupproject_count(self):
        """Return number of projects
        """
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')

        return len(catalog(portal_type='tdf.templateuploadcenter.tupproject'))



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
                          'sort_on' : sort_on,
                          'sort_order' : 'reverse',
                          'review_state': 'published',
                          'portal_type':'tdf.templateuploadcenter.tupproject'}

        results = self.catalog(**contentFilter)

        return results



    def get_latest_template_releases(self):
        self.catalog =api.portal.get_tool(name='portal_catalog')
        sort_on = 'created'
        contentFilter = {'sort_on' : sort_on,
                         'sort_order' : 'reverse',
                         'review_state' : 'final',
                         'portal_type' : ('tdf.templateuploadcenter.tuprelease', 'tdf.templateuploadcenter.tupreleaselink' ),
                         }

        results = self.catalog(**contentFilter)
        return results




    def eupproject_count(self):
        """Return number of projects
        """
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')

        return len(catalog(portal_type='tdf.extensionuploadcenter.eupproject'))



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
                          'sort_on' : sort_on,
                          'sort_order' : 'reverse',
                          'review_state': 'published',
                          'portal_type':'tdf.extensionuploadcenter.eupproject'}

        results = self.catalog(**contentFilter)

        return results


    def get_latest_extension_releases(self):
        self.catalog =api.portal.get_tool(name='portal_catalog')
        sort_on = 'created'
        contentFilter = {'sort_on' : sort_on,
                         'sort_order' : 'reverse',
                         'review_state' : 'final',
                         'portal_type' : ('tdf.extensionuploadcenter.euprelease', 'tdf.extensionuploadcenter.eupreleaselink' ),
                         }

        results = self.catalog(**contentFilter)
        return results
