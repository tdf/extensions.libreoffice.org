# -*- coding: utf-8 -*-
"""Installer for the tdf.exttempsitepolicy package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read() +
    '\n' +
    'Contributors\n' +
    '============\n' +
    '\n' +
    open('CONTRIBUTORS.rst').read() +
    '\n' +
    open('CHANGES.rst').read() +
    '\n')


setup(
    name='tdf.exttempsitepolicy',
    version='1.0a1',
    description="LibreOffice-Extension-Templates-Website-Policy",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Andreas Mantke',
    author_email='maand@gmx.de',
    url='https://pypi.python.org/pypi/tdf.exttempsitepolicy',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['tdf'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'setuptools',
        'z3c.jbot',
        'tdf.extensionuploadcenter',
        'tdf.templateuploadcenter',
        'cioppino.twothumbs',
        'tdf.extensioncentertheme',
        'collective.registrationcaptcha[captchawidgets]',
        'collective.recaptchacontactform',
        'collective.monkeypatcher',
        'kitconcept.dsgvo'
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
            'collective.MockMailHost'
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
