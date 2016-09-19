# -*- coding: utf-8 -*-
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
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

                        setattr(release, AVAILABLE_FIELDS[index], thefile)

                        index = index + 1

                    else:
                        migration_error.error('Thre was a problem trying to retrieve the file.')

            yield item
