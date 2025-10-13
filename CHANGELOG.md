# Changelog


## v0.10.0 (2025-10-13)

* Bump version to 0.10.0.

* Feat: always print compressed size and gains.


## v0.9.0 (2025-09-01)

* Bump version to 0.9.0.

* Fix ImageMagick compatibility for both v6 and v7.

  Support both ImageMagick 6.x (convert/identify commands) and 7.x (magick command).
  The code now automatically detects which version is available and uses the
  appropriate commands, fixing CI failures on Ubuntu which ships with ImageMagick 6.x.

  🤖 Generated with [Claude Code](https://claude.ai/code)

* Update GH workflow to add imagemagick.

* Fix ruff versions.


## v0.8.4 (2025-09-01)

* Bump version to 0.8.4.

* Migrate to uv and modern package structure.

* Add uv to readme.

* Set python_requires to >=3.9.

* Changed license specifier.

* Removed wheel settings from setup.cfg.


## v0.8.3 (2023-10-02)

* Migrate to magick commands.


## v0.8.2 (2023-10-02)

* Add CLI option for num_cpus.


## v0.8.1 (2023-10-02)

* Formatting and fix path handling.


## v0.8.0 (2023-03-13)

* Bump requirement to python 3.8.

* Docs: add @caydey as a contributor.

* Update README and minor code changes.

* Added '-l' to compress emf files using libreoffice.

* Fixed bug for when file compression fails.

* Fixed bug with clashing variable names.

* Refractored "image" to "file"

* Media file compression and recompress jpeg files.


## v0.7.2 (2023-01-30)

* Remove manifest.in.


## v0.7.1 (2022-08-02)

* Update python requirements.


## v0.7.0 (2022-08-02)

* Update python requirements.


## v0.6.0 (2021-10-28)

* Add feature to skip transparent images completely, add EMF.


## v0.5.0 (2021-08-06)

* Allow POTX files, fixes #4.

* Fallback to 'convert' and 'identify', fixes #3.


## v0.4.0 (2021-05-25)

* Add handling of transparency and TIFFs.


## v0.3.0 (2021-05-14)

* Auto-formatting.

* Add -f/--force parameter.

* Update gitignore.


## v0.2.1 (2021-03-29)

* Add defaults to CLI options.

* Update badge link.


## v0.2.0 (2021-03-10)

* Change executable name for harmonization purposes.


## v0.1.3 (2021-03-10)

* Improve setup.py.

* Remove release script.


## v0.1.2 (2021-03-06)

* Format setup.py and switch to markdown.

* Add warning.

* Update badge URL.


## v0.1.1 (2021-02-08)

* Better error handling; check for magick command.

* Add badge to readme.


## v0.1.0 (2021-02-07)

* Fix README.

* Add changelog.

* Switch to python package.

* Various updates, v0.2.

* Add TODO notice.

* Handle input errors.

* Update instructions, add script.

* Add script and README.

* Initial commit.


