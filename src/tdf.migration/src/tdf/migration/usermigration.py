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
