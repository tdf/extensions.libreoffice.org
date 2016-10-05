# LibreOffice Extensions and Templates

This is the repository is used to create and configure the new and improved website extensions.libreoffice.org

The purpose of the new site is to provide and exchange extensions and templates for LibreOffice under free software licenses in a more easy way than the current websites.

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
src/tdf.extensioncentertheme/src/tdf/extensioncentertheme/theme/scss/main.scss
and it will be compiled to the corresponding CSS in
src/tdf.extensioncentertheme/src/tdf/extensioncentertheme/theme/styles/main.css
