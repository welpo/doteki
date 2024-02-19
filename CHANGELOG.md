# Changelog

Welcome to the changelog for dōteki. This document aims to provide a comprehensive list of all notable changes made to the project, organised chronologically by release version.

We use Semantic Versioning (SemVer) for our version numbers, formatted as MAJOR.MINOR.PATCH. Major version changes involve significant (breaking) changes, minor versions introduce features and improvements in a backward compatible manner, and patch versions are for bug fixes and minor tweaks.

## [0.0.7](https://github.com/welpo/doteki/compare/v0.0.3..v0.0.7) - 2024-02-10

### 🐛 Bug fixes

- *(cli)* Use a temp file for safe README updates ([5d3ffa0](https://github.com/welpo/doteki/commit/5d3ffa0808f8b4e0af54226598d42d44f4086371)) by [@welpo](https://github.com/welpo)

### 📝 Documentation

- *(README)* Add git-sumi badge ([31d1d78](https://github.com/welpo/doteki/commit/31d1d7885c3af77f5c34b6b40830c4093466f1c7)) by [@welpo](https://github.com/welpo)
- *(README)* Add IPA notation for pronunciation ([41a6438](https://github.com/welpo/doteki/commit/41a643813381c9c01953a5c3c30a6d87d3e30dd8)) by [@welpo](https://github.com/welpo)
- *(website)* Turn githooks suggestion into a "tip" ([7757145](https://github.com/welpo/doteki/commit/77571455f2a646e4de25300f8cd180c8202bce3e)) by [@welpo](https://github.com/welpo)

### ♻️ Refactor

- *(cli)* Avoid redundant file read for credits ([748545e](https://github.com/welpo/doteki/commit/748545e32ad6e576c4d34d5f304cf0bf8ceb939e)) by [@welpo](https://github.com/welpo)

### 🔧 Miscellaneous tasks

- *(CD)* Bump dōteki in doteki-action on release ([8e42cf1](https://github.com/welpo/doteki/commit/8e42cf11bbe48f25e45b76048e1931be0639e854)) by [@welpo](https://github.com/welpo)
- *(CHANGELOG)* Update commit types ([bb1ed55](https://github.com/welpo/doteki/commit/bb1ed554ca3f0595f3950766ce00596931898ad3)) by [@welpo](https://github.com/welpo)
- *(CHANGELOG)* Improve emoji pattern ([e2e84bf](https://github.com/welpo/doteki/commit/e2e84bfda1c19dec3cd18f7eb016c9f2b8d17979)) by [@welpo](https://github.com/welpo)
- *(CI)* Update git-sumi config ([19c824a](https://github.com/welpo/doteki/commit/19c824a906b006fa9173af24099a6b1d9b4ca9dd)) by [@welpo](https://github.com/welpo)
- *(git-sumi)* Require a space after the gitmoji ([c839160](https://github.com/welpo/doteki/commit/c839160bc5561412de079d7f333b61f1a605a67e)) by [@welpo](https://github.com/welpo)
- *(release)* Verify version tag format on release ([a95ab3f](https://github.com/welpo/doteki/commit/a95ab3ff41ef2d604c5bbf6dd3f67561fb98a889)) by [@welpo](https://github.com/welpo)
- *(release)* Automate PyPI release ([d1dbecb](https://github.com/welpo/doteki/commit/d1dbecb76e1422fd0633d21ab83de9ebe822293b)) by [@welpo](https://github.com/welpo)

## [0.0.3](https://github.com/welpo/doteki/compare/v0.0.2..v0.0.3) - 2024-02-06

### ✨ Features

- Add -v | --version argument ([941c2fd](https://github.com/welpo/doteki/commit/941c2fd7057792cdca5a6d088bb720b8b523d179)) by [@welpo](https://github.com/welpo)

### 🐛 Bug fixes

- *(test_cli)* Read/write using UTF-8 encoding ([24c4756](https://github.com/welpo/doteki/commit/24c4756f6f388550627f2909af6caea3e762b68b)) by [@welpo](https://github.com/welpo)
- Specify UTF-8 encoding when reading files ([1ae728c](https://github.com/welpo/doteki/commit/1ae728c38920cb5d205306133a20b1893ba60c56)) by [@welpo](https://github.com/welpo)

### 📝 Documentation

- *(contributing)* Enrich PR information ([917bf4d](https://github.com/welpo/doteki/commit/917bf4d559d5515978aa4734aaad30f97c3e71bc)) by [@welpo](https://github.com/welpo)
- *(plugin-standard)* Add link to developer guide ([f7310ee](https://github.com/welpo/doteki/commit/f7310ee7e7985ea39868d08a6e8614fc213082da)) by [@welpo](https://github.com/welpo)

### ♻️ Refactor

- *(cli)* Improve code readability ([915f02e](https://github.com/welpo/doteki/commit/915f02ebd81d4dc152585251519ed8a55afeb287)) by [@welpo](https://github.com/welpo)
- Move parse_arguments definition after its calling ([4cbb4bd](https://github.com/welpo/doteki/commit/4cbb4bdd5e93efabbe6c274161d14fb5662124aa)) by [@welpo](https://github.com/welpo)

### 🔧 Miscellaneous tasks

- *(CI)* Fix links in tag description ([c37d53c](https://github.com/welpo/doteki/commit/c37d53ca26edc75c365b4b90f8377ee43608d7af)) by [@welpo](https://github.com/welpo)
- *(README)* Remove codecov logo from shield ([af4b318](https://github.com/welpo/doteki/commit/af4b31801a8a8de2e654cea08027d31d5a744a5f)) by [@welpo](https://github.com/welpo)
- Use git-sumi to lint commit messages ([3e03678](https://github.com/welpo/doteki/commit/3e036786f98341191bfb7ff6c57e31e71753eb8a)) by [@welpo](https://github.com/welpo)
- Add pre-commit script ([58ef244](https://github.com/welpo/doteki/commit/58ef244d73236091ca6cf20e2aac462314aafbe6)) by [@welpo](https://github.com/welpo)
- Sort imports with `isort` ([dbd21a2](https://github.com/welpo/doteki/commit/dbd21a2ba65d5a552da7f86c503792e6511f130b)) by [@welpo](https://github.com/welpo)
- Add continuous deployment workflow ([9f01646](https://github.com/welpo/doteki/commit/9f01646c3de3f82005fa16a1e61de8fb428cb5ed)) by [@welpo](https://github.com/welpo)

## [0.0.2](https://github.com/welpo/doteki/compare/v0.0.1..v0.0.2) - 2024-01-26

### 🐛 Bug fixes

- Add utf-8 encoding to file write operations ([17a8584](https://github.com/welpo/doteki/commit/17a8584822c1cedaa38f6897eefebca70d7f6039)) by [@welpo](https://github.com/welpo)

### ♻️ Refactor

- *(cli)* Improve error message on missing deps ([3367dfa](https://github.com/welpo/doteki/commit/3367dfac2ac17459d70968d727e9879f2cc52a19)) by [@welpo](https://github.com/welpo)

## 0.0.1 - 2024-01-19

### ✨ Features

- Initial commit ([9d80472](https://github.com/welpo/doteki/commit/9d8047210edecbd0a4db2ba478f2dffab102ab68)) by [@welpo](https://github.com/welpo)

<!-- generated by git-cliff -->
