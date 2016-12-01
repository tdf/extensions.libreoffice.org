# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import helpers

import tdf.exttempsitepolicy
import collective.MockMailHost


class TdfExttempsitepolicyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=tdf.exttempsitepolicy)
        self.loadZCML(package=collective.MockMailHost)
        z2.installProduct(app, 'collective.MockMailHost')
        z2.installProduct(app, 'tdf.extensionuploadcenter')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'tdf.exttempsitepolicy:default')
        applyProfile(portal, 'tdf.extensionuploadcenter:default')
        applyProfile(portal, 'collective.MockMailHost:default')
        helpers.quickInstallProduct(portal, 'collective.MockMailHost')
        setRoles(portal, TEST_USER_ID, ['Manager'])

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'collective.MockMailHost')


TDF_EXTTEMPSITEPOLICY_FIXTURE = TdfExttempsitepolicyLayer()


TDF_EXTTEMPSITEPOLICY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TDF_EXTTEMPSITEPOLICY_FIXTURE,),
    name='TdfExttempsitepolicyLayer:IntegrationTesting'
)


TDF_EXTTEMPSITEPOLICY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TDF_EXTTEMPSITEPOLICY_FIXTURE,),
    name='TdfExttempsitepolicyLayer:FunctionalTesting'
)


TDF_EXTTEMPSITEPOLICY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        TDF_EXTTEMPSITEPOLICY_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='TdfExttempsitepolicyLayer:AcceptanceTesting'
)
