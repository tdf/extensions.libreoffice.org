.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide_addons.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
tdf.exttempsitepolicy
==============================================================================

This Plone add-on contains the site policy for the new LibreOffice extensions and templates website.

Features
--------

- Install and activate the Plone add-ons that are used to drive the LibreOffice extensions and template site:

  - plone.api
  - tdf.extensionuploadcenter
  - tdf.templateuploadcenter
  - cioppino.twothumbs
  - collective.ATClamAV
  - tdf.extensioncentertheme

- Set title and description of the site.
- New front-page with dynamic content and internationalisation


Examples
--------

This add-on can be seen in action at the following sites:
- http://vm141.documentfoundation.org:9103


Documentation
-------------

The documentation will be in the docs folder of this add-on.


Translations
------------

This product has been translated into

- currently no translation


Installation
------------

Install tdf.exttempsitepolicy by adding it to your buildout::

    [buildout]

    ...

    eggs =
        tdf.exttempsitepolicy


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/tdf/tdf.exttempsitepolicy/issues
- Source Code: https://github.com/tdf/tdf.exttempsitepolicy
- Documentation: inside the docs folder of the add-on


Support
-------

If you are having issues, please let us know.



License
-------

The project is licensed under the GPLv2.
