# Changelog

All notable changes to this project will be documented in this file.

## [unreleased]

### ⚙️ Miscellaneous Tasks

- *(renovate)* Switch configuration to shared json5 preset - ([710307b](https://git.0xmax42.io/maxp/clipcode/commit/710307b936514b7527383a576edfaf702072cff6))

## [0.6.0](https://git.0xmax42.io/maxp/clipcode/compare/v0.5.1..v0.6.0) - 2026-01-10

### 🚀 Features

- *(exporter)* Skip binary and svg files on export - ([e080833](https://git.0xmax42.io/maxp/clipcode/commit/e080833c807682a82a9084540c7f43f707756bb0))

## [0.5.1](https://git.0xmax42.io/maxp/clipcode/compare/v0.5.0..v0.5.1) - 2025-10-15

### 🚀 Features

- *(ci)* Add GitHub Actions workflow for continuous integration - ([a80a7de](https://git.0xmax42.io/maxp/clipcode/commit/a80a7dea3ee398fdee2a4e6af09356e22764c432))

### 🐛 Bug Fixes

- *(gitignore_utils)* Normalize paths for consistent .gitignore filtering - ([dd18295](https://git.0xmax42.io/maxp/clipcode/commit/dd18295f6ac21c5c423b9bacfaa8da4e5b15ddf2))
- *(workflows)* Use ubuntu-python runner for ci and build jobs - ([923d73d](https://git.0xmax42.io/maxp/clipcode/commit/923d73d566fd85d465731d3b080534dd8f602236))

### 🚜 Refactor

- *(workflows)* Simplify release workflow with auto-changelog - ([b328ab6](https://git.0xmax42.io/maxp/clipcode/commit/b328ab669f38d8143655ce19209a70dd74523ae0))

### 📚 Documentation

- *(readme)* Remove author section - ([c38af8b](https://git.0xmax42.io/maxp/clipcode/commit/c38af8ba05138f4177188718dfab65b7ff2f5159))

### ⚙️ Miscellaneous Tasks

- *(ci)* Switch to native python runner for ci und build jobs - ([73e64db](https://git.0xmax42.io/maxp/clipcode/commit/73e64db3357d982ea1c00898b6873f688f12fcb5))
- *(ci)* Update runner image to ubuntu-latest - ([55e9722](https://git.0xmax42.io/maxp/clipcode/commit/55e97225cfc4a8170dff9dcaad3118f7ac5fe8e2))
- Configure Renovate - ([7c32b84](https://git.0xmax42.io/maxp/clipcode/commit/7c32b8480a0158ff908298046a91033055044f76))
- *(workflows)* Update Python version and add release sync - ([5c23489](https://git.0xmax42.io/maxp/clipcode/commit/5c234896b83b3dac19ca38fdfe36510b00cd01e0))

## [0.5.0](https://git.0xmax42.io/maxp/clipcode/compare/v0.4.0..v0.5.0) - 2025-07-21

### 🚀 Features

- *(cli)* Add explicit ignore pattern support - ([d30fa63](https://git.0xmax42.io/maxp/clipcode/commit/d30fa63675a12f33c88f4c88e78590ab7183b0f9))

## [0.4.0](https://git.0xmax42.io/maxp/clipcode/compare/v0.3.0..v0.4.0) - 2025-07-04

### 🚀 Features

- *(cli)* Add gitignore support and configuration options - ([b3501b9](https://git.0xmax42.io/maxp/clipcode/commit/b3501b9a13046008a8c21d6217ecaa60546d76ab))

## [0.3.0](https://git.0xmax42.io/maxp/clipcode/compare/v0.2.0..v0.3.0) - 2025-06-20

### ⚙️ Miscellaneous Tasks

- *(workflows)* Improve git-cliff installation and tagging - ([388a668](https://git.0xmax42.io/maxp/clipcode/commit/388a66871d826fca2b36ad2b3382d3a3d346a042))

## [0.2.0](https://git.0xmax42.io/maxp/clipcode/compare/v0.1.2..v0.2.0) - 2025-06-14

### 🚀 Features

- *(exporter)* Support exporting all files if no extensions provided - ([052b6e5](https://git.0xmax42.io/maxp/clipcode/commit/052b6e5af8fd30621f82e7475ee56d8dbfcd0821))
- *(file_utils)* Add recursive file discovery function - ([b9f7232](https://git.0xmax42.io/maxp/clipcode/commit/b9f723299c2c0f068dcdbda0949452a05fea8cc6))

### 🐛 Bug Fixes

- *(cli)* Handle empty extensions list in argument parsing - ([6bce171](https://git.0xmax42.io/maxp/clipcode/commit/6bce1711ec942008ed9a61e85b847c9fe3e362cf))

## [0.1.2](https://git.0xmax42.io/maxp/clipcode/compare/v0.1.1..v0.1.2) - 2025-05-11

### ⚙️ Miscellaneous Tasks

- *(pyproject)* Bump version and update script alias - ([96a6521](https://git.0xmax42.io/maxp/clipcode/commit/96a6521e083af4fa3a875f67f6d4a014e8066bbe))

## [0.1.1] - 2025-05-11

### 🚀 Features

- *(clipcode)* Add CLI tool for exporting code snippets - ([d576e7c](https://git.0xmax42.io/maxp/clipcode/commit/d576e7c060ddb15aa6418bf54ae70fcc96ee9475))
- Initialize project with poetry configuration - ([6a7f236](https://git.0xmax42.io/maxp/clipcode/commit/6a7f236e528c305ee0201de7f78fe8cc8290b785))
- *(vscode)* Customize activity bar and peacock colors - ([59ccca2](https://git.0xmax42.io/maxp/clipcode/commit/59ccca2ed8e19fe6cf8336b1d709d81eb171d150))
- *(ci)* Add automated workflows for releases and nightly builds - ([c60d3ee](https://git.0xmax42.io/maxp/clipcode/commit/c60d3eecc614f5ffb8721e975ced6293f6bfbffd))

### 📚 Documentation

- Add LICENSE and README files - ([7305a38](https://git.0xmax42.io/maxp/clipcode/commit/7305a386b112ff5abcf58cc22589a21e75617879))

### ⚙️ Miscellaneous Tasks

- *(gitignore)* Add patterns to ignore build and env files - ([f024edf](https://git.0xmax42.io/maxp/clipcode/commit/f024edf5d74ec6fc871a18861baccf2a6a0ba97c))


