'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');

gulp.task('sass', function () {
  return gulp.src('./src/tdf/extensioncentertheme/theme/scss/**/*.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('./src/tdf/extensioncentertheme/theme/styles'));
});

gulp.task('default', function () {
  gulp.watch('./src/tdf/extensioncentertheme/theme/**/*.scss', ['sass']);
});
