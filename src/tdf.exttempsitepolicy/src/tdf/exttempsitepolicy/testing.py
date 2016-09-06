# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import tdf.exttempsitepolicy


class TdfExttempsitepolicyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=tdf.exttempsitepolicy)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'tdf.exttempsitepolicy:default')


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
