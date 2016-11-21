from Products.Five.browser import BrowserView
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides

import json
import transaction


def import_userdb(site):
    """ Wins the password set on the extensions one """
    pas = site.acl_users
    users = pas.source_users
    templatesuserfile = open('userdb-templates.txt', 'r')
    extensionsuserfile = open('userdb-extensions.txt', 'r')
    templates_users = json.loads(templatesuserfile.read())
    extensions_users = json.loads(extensionsuserfile.read())
    templatesuserfile.close()
    extensionsuserfile.close()

    for user in extensions_users:
        try:
            users.addUser(user, user, extensions_users[user])
        except:
            pass

    # Set all the users for templates
    for user in templates_users:
        try:
            users.addUser(user, user, templates_users[user])
        except KeyError:
            print('There is already an user with the id: {}'.format(user))

    transaction.commit()


class ImportUserInformation(BrowserView):
    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        fext = open('userdata-extensions.txt', 'r')
        ftemp = open('userdata-templates.txt', 'r')
        ext = [tuple(a) for a in json.loads(fext.read())]
        temp = [tuple(a) for a in json.loads(ftemp.read())]
        fext.close()
        ftemp.close()

        for user, fullname, email in temp:
            user_obj = api.user.get(user)
            try:
                user_obj.setMemberProperties(
                    dict(fullname=fullname, email=email)
                )
                api.user.grant_roles(user=user_obj, roles=['Member', ])
            except:
                print('error on user {}'.format(user))

        # Users in ext are last, we took them as canonical
        for user, fullname, email in ext:
            user_obj = api.user.get(user)
            try:
                user_obj.setMemberProperties(
                    dict(fullname=fullname, email=email)
                )
                api.user.grant_roles(user=user_obj, roles=['Member', ])
            except:
                print('error on user {}'.format(user))
