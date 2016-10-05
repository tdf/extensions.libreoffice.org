from plone import api
from Products.Five.browser import BrowserView
from collective.transmogrifier.transmogrifier import Transmogrifier
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


class DFMigrationTemplates(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        portal = api.portal.get()
        transmogrifier = Transmogrifier(portal)
        transmogrifier('df.templates')
        return 'DONE!'


class DFMigrationExtensions(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        portal = api.portal.get()
        transmogrifier = Transmogrifier(portal)
        transmogrifier('df.extensions')
        return 'DONE!'


class MagicDebug(BrowserView):

    def __call__(self):
        import ipdb; ipdb.set_trace()


class GetRidOfMailtos(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        pc = api.portal.get_tool('portal_catalog')
        results = pc.searchResults(portal_type=[
            'tdf.extensionuploadcenter.eupproject',
            'tdf.extensionuploadcenter.euprelease',
            'tdf.extensionuploadcenter.eupreleaselink',
            'tdf.templateuploadcenter.tupproject',
            'tdf.templateuploadcenter.tuprelease',
            'tdf.templateuploadcenter.tupreleaselink',
        ])

        log = []
        for item in results:
            obj = item.getObject()
            if 'project' in item.portal_type and \
               obj.contactAddress is not None:
                if 'mailto:' in obj.contactAddress:
                    obj.contactAddress = obj.contactAddress.replace('mailto:', '')
                    log.append(obj.id)
            if 'release' in item.portal_type and \
               obj.contact_address2 is not None:
                if 'mailto:' in obj.contact_address2:
                    obj.contact_address2 = obj.contact_address2.replace('mailto:', '')
                    log.append(obj.id)

        return log
