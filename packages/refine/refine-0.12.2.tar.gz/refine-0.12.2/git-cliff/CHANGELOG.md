# Changelog

All notable changes to this project will be documented in this file.

## [0.12.2](https://github.com/s0undt3ch/refine/releases/tag/0.12.2) - 2025-04-21

### 🚀 Features

- *(imports)* Simplify adding and removing imports in codemods
- *(logging)* Allow passing `-v/--verbose` to switch to debug logging
- *(SQL regex matching)* Separated logic into a few reusable utilities
- *(cli)* Differentiate `--exclude` and `--exclude-extend`
- *(cli)* Differentiate `--select` and `--select-extend`
- *(cli)* Differentiate `--codemods-path` and `--codemods-path-extend`
- *(sql formatter)* Skip modules that don't contain query strings

### 🐛 Bug Fixes

- *(sqlfmt)* Remove auto skip tests files logic
- *(sqlfmt)* Properly handle big query strings

### 🚜 Refactor

- *(cli)* Refactor CLI code to enable simplified testing

### 🧪 Testing

- *(registry)* Refactor registry to enable testing
- *(cli)* Add CLI usage tests

### ⚙️ Miscellaneous Tasks

- *(cleanup)* Remove unused variable
- Define `__all__` in `refine/__init__.py`
- *(config)* Add `as_dict` method to `refine.config.Config`
- *(pre-commit)* Run `ruff-format` before `ruff`

