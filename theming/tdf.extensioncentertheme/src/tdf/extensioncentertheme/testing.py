# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import tdf.extensioncentertheme


class TdfExtensioncenterthemeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=tdf.extensioncentertheme)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'tdf.extensioncentertheme:default')


TDF_EXTENSIONCENTERTHEME_FIXTURE = TdfExtensioncenterthemeLayer()


TDF_EXTENSIONCENTERTHEME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TDF_EXTENSIONCENTERTHEME_FIXTURE,),
    name='TdfExtensioncenterthemeLayer:IntegrationTesting'
)


TDF_EXTENSIONCENTERTHEME_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TDF_EXTENSIONCENTERTHEME_FIXTURE,),
    name='TdfExtensioncenterthemeLayer:FunctionalTesting'
)


TDF_EXTENSIONCENTERTHEME_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        TDF_EXTENSIONCENTERTHEME_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='TdfExtensioncenterthemeLayer:AcceptanceTesting'
)
