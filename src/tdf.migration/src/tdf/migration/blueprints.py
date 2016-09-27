# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import Matcher
from collective.transmogrifier.utils import defaultKeys
from plone.namedfile.file import NamedBlobFile
from zope.interface import classProvides
from zope.interface import implements

import base64
import logging
import mimetypes
import requests

migration_error = logging.getLogger('migration_error')

AVAILABLE_FIELDS = ['file', 'file1', 'file2', 'file3', 'file4', 'file5']


class ReleaseFile2Fields(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.options = options
        self.context = transmogrifier.context

        self.remote_url = self.options.get('remote-url',
                                           'http://localhost:8080')
        self.remote_username = self.options.get('remote-username', 'admin')
        self.remote_password = self.options.get('remote-password', 'admin')

        self.catalog_path = self.options.get('catalog-path', '/Plone/portal_catalog')
        self.site_path_length = len('/'.join(self.catalog_path.split('/')[:-1]))

        self.remote_root = self.options.get('remote-root', '')

    def __iter__(self):
        for item in self.previous:
            if item['_type'] == 'tdf.templateuploadcenter.tuprelease' or \
               item['_type'] == 'tdf.extensionuploadcenter.euprelease' or \
               item['_type'] == 'PSCRelease':

                release = self.context.unrestrictedTraverse(str(item['_path']).lstrip('/'), None)
                if not release:
                    import ipdb; ipdb.set_trace()
                    yield item

                # Get the files below it from the item's original_path
                catalog_query = {'path': {'query': ''}, 'portal_type': ['PSCFile', ]}
                catalog_query['path']['query'] = self.remote_root + item['_original_path']
                catalog_query = ' '.join(str(catalog_query).split())
                catalog_query = base64.b64encode(catalog_query)

                self.payload = {'catalog_query': catalog_query}

                # Make request
                resp = requests.get('{}{}/get_catalog_results'.format(self.remote_url, self.catalog_path), params=self.payload, auth=(self.remote_username, self.remote_password))
                file_list = resp.json()

                # Get the files
                index = 0
                for rfile in file_list:
                    resp = requests.get(self.remote_url + rfile, auth=item['_auth_info'])
                    if resp.ok:
                        data = resp.content
                        filename = rfile.split('/')[-1]

                        thefile = NamedBlobFile(data=data,
                                                filename=filename,
                                                contentType=mimetypes.guess_type(filename)[0] or '')

                        if index < len(AVAILABLE_FIELDS):
                            setattr(release, AVAILABLE_FIELDS[index], thefile)
                        else:
                            migration_error.error('The release {} has exceeded the number of allowed files. The file {} has been discarded.'.format(aq_parent(release).id, filename))
                        index = index + 1

                    else:
                        migration_error.error('There was a problem trying to retrieve the file.')

            yield item


class DFFieldsCorrector(object):
    """ This corrects the differences (mainly in naming) of the incoming fields
        with the expected ones.
    """

    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context

        if 'path-key' in options:
            pathkeys = options['path-key'].splitlines()
        else:
            pathkeys = defaultKeys(options['blueprint'], name, 'path')
        self.pathkey = Matcher(*pathkeys)

    def __iter__(self):
        for item in self.previous:
            pathkey = self.pathkey(*item.keys())[0]

            if not pathkey:
                # not enough info
                yield item; continue

            obj = self.context.unrestrictedTraverse(str(item[pathkey]).lstrip('/'), None)

            if obj is None:
                # path doesn't exist
                yield item; continue

            # DF specific
            if item.get('_type', False):
                if item.get('_type') == 'tdf.templateuploadcenter.tupproject' or \
                   item.get('_type') == 'tdf.extensionuploadcenter.eupproject':
                    item['details'] = item['text']
                    item['category_choice'] = item['categories']
                    item['documentation_link'] = item['documentationLink']
                    if item.get('logo', False):
                        item['project_logo'] = item['logo']

            if item.get('_type', False):
                if item.get('_type') == 'tdf.templateuploadcenter.tuprelease' or \
                   item.get('_type') == 'tdf.extensionuploadcenter.euprelease':
                    item['details'] = item['text']
                    license_fields = ['license', 'license2', 'license3']
                    licenses = []
                    for fname in license_fields:
                        if item.get(fname, False):
                            licenses.extend([item[fname]] if isinstance(item[fname], unicode) else item[fname])

                    item['licenses_choice'] = licenses
                    item['compatibility_choice'] = item['compatibility']

            yield item
