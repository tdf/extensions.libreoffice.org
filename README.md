# LibreOffice Extensions and Templates

This is the repository used to create and configure the new and improved website extensions.libreoffice.org

The purpose of the new site is to provide and exchange extensions and templates for LibreOffice under free software licenses in a more easy way than the current websites.

Important Note: Because there was a decision to change the environment for the LibreOffice extensions and templates website, the development will not take further steps inside this repository. But the development will get further in a fork of this repository with the implemenation of improved Plone add-ons and a migration to Python 3.

# Development notes

## Theme development

There is a Gulp worflow in the theme package in order to watch and compile the
SCSS stylesheet to CSS. To proceed it is required:

```
  $ cd src/tdf.extensioncentertheme
  $ npm install
  $ npm start
```

Then you can modify the SCSS file in
```
  src/tdf.extensioncentertheme/src/tdf/extensioncentertheme/theme/scss/main.scss
```
and it will be compiled to the corresponding CSS in

```
  src/tdf.extensioncentertheme/src/tdf/extensioncentertheme/theme/styles/main.css
```

## Migration

The migration has been developed using a Transmogrifier pipeline in
*src/tdf.migration* package. The definition of the pipeline is splitted in two
(one for extensions and the other for templates):

```
  src/tdf.migration/src/tdf/migration/df-extensions.cfg
```

```
  src/tdf.migration/src/tdf/migration/df-templates.cfg
```

Both should be runned in order to migrate everything.

In order to run the migration, this steps should be followed:

1. Migrate users (using the dump helper, see later notes)
2. Create extensions and templates center objects manually
3. Run the migrator (using the view helper or from a debug session) for templates with these queries (keeping the order)
  1. catalog-query = {'path': {'query': '/LibreOffice-Templates/template-center'}, 'portal_type': ['PSCProject']}
  2. catalog-query = {'path': {'query': '/LibreOffice-Templates/template-center'}, 'portal_type': ['PSCProject', 'PSCRelease']}
4. Run the migrator (using the view helper or from a debug session) for extensions with these queries (keeping the order)
  1. catalog-query = {'path': {'query': '/LibreOffice-Extensions-and-Templates/extension-center'}, 'portal_type': ['PSCProject']}
  2. catalog-query = {'path': {'query': '/LibreOffice-Extensions-and-Templates/extension-center'}, 'portal_type': ['PSCProject', 'PSCRelease']}

### User migration

There are debug scripts in place in order to dump the username database and to import it back again. Due to the origin in this project comes from two different sites, and it's possible that there are duplicated usernames, it's required to define a one source as master, and the other as secondary. In case that there is a duplicated username, the master one password and properties will prevail.

The scripts are:

```
  > from ploneorg.migration.usermigration import export_userdb
  > export_userdb(portal)
```

```
  > from tdf.migration.usermigration import import_userdb
  > import_userdb(portal)
```
