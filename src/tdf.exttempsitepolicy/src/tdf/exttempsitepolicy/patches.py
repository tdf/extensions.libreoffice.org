# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces.controlpanel import IMailSchema
from Products.statusmessages.interfaces import IStatusMessage
from email.MIMEText import MIMEText
from plone.registry.interfaces import IRegistry
from smtplib import SMTPException
from zope.component import getUtility
from zope.site.hooks import getSite
import logging

log = logging.getLogger(__name__)


def send_message(self, data):
    subject = data.get('subject')

    portal = getSite()
    registry = getUtility(IRegistry)
    mail_settings = registry.forInterface(IMailSchema, prefix='plone')
    send_to_address = mail_settings.email_from_address
    from_address = mail_settings.email_from_address
    registry = getUtility(IRegistry)
    encoding = registry.get('plone.email_charset', 'utf-8')
    host = getToolByName(self.context, 'MailHost')

    data['url'] = portal.absolute_url()
    message = self.generate_mail(data, encoding)
    message = MIMEText(message, 'plain', encoding)
    message['Reply-To'] = data['sender_from_address']

    try:
        # This actually sends out the mail
        host.send(
            message,
            send_to_address,
            from_address,
            subject=subject,
            charset=encoding
        )
    except (SMTPException, RuntimeError) as e:
        log.error(e)
        plone_utils = getToolByName(portal, 'plone_utils')
        exception = plone_utils.exceptionString()
        message = _(u'Unable to send mail: ${exception}',
                    mapping={u'exception': exception})
        IStatusMessage(self.request).add(message, type=u'error')
