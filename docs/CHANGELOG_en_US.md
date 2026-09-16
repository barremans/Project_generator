# Changelog

All changes to the Project Generator are documented here.

## [1.2.0] - 2026-09-16

### Added
- **New "Tools" menu** (between Language and Help) with action **"Headers &
  Structure..."** — bundles two tools ported from the standalone
  project-doc-tool project, which has thereby been merged into Project
  Generator (leaving only 1 application):
  - **Dry-run headers**: analyses a chosen project folder and shows which
    files have no header or an incorrect one, without changing anything
  - **Add headers**: actually adds/fixes headers, in Project Generator's
    own header format (`File:`/`Rol:`/`Applicatie:`/`Versie:`/`Auteur:`/
    `Changes:`)
  - **Generate project structure**: generates `PROJECT_STRUCTURE.md` (tree
    overview + per-file header metadata as a fenced code block) for a
    chosen project folder and output folder; automatically opens the
    output folder afterwards
- **New Tools settings** (via the "⚙ Settings" button in the Tools dialog):
  include extensions, exclude folders, exclude files, and header defaults
  for application/version (author reuses the existing "Default Author"
  setting — no duplicate field)
- The Tools dialog's project folder and output folder are now remembered
  across sessions
- Every newly generated project now automatically gets a
  `docs/PROJECT_STRUCTURE.md` (new step 9 in the generator), in addition to
  the option to (re)generate it separately via Tools
- New standalone scripts: `scripts/generate_project_structure.py` and
  `scripts/add_headers.py` (dry-run by default, `--apply` for actual
  changes with add_headers)

### Changed
- `core/extension_registry.py` now recognises headers in two vocabularies
  (the old project-doc-tool format and Project Generator's own format) —
  needed so already-generated files don't incorrectly show up as "no
  header"

### Fixed
- BUGFIX (ported from project-doc-tool, already present in the original):
  header detection on short files (< 30 lines) failed silently due to a
  PEP 479 incompatibility — now fixed using `itertools.islice`
- BUGFIX: writing `//` comments into `.json` files (invalid JSON) has been
  stopped — `.json` is now skipped when adding headers

## [1.1.0] - 2026-09-15

### Added
- **`core/` folder**: new standard folder in the generated project
  structure, including an `__init__.py` — intended for core/shared logic,
  separate from the `app/` package.

## [1.0.4] - 2024-02-12

### Added
- **Modern Python Packaging**: pyproject.toml (PEP 517/518/621)
- **Build system**: setup.py for backwards compatibility
- **Package manifest**: MANIFEST.in for distribution
- **License**: MIT License template
- **Development guide**: CONTRIBUTING.md with code style guidelines
- **Makefile**: Development shortcuts (make test, make lint, etc.)
- **Scripts folder**: Standard utility scripts
  - `update_toml.py` - Automatically update pyproject.toml
  - `bump_version.py` - Increase version number everywhere
  - `generate_requirements.py` - Generate requirements from pyproject.toml
- **QSS templates**: main.qss and detail.qss for Qt styling
- **Icon system**: Automatic copying of default icons
- **Enhanced README**: Complete installation and usage instructions

### Changed
- Project structure now fully PEP compliant
- Generator version: 1.0.3 → 1.0.4
- Improved gitignore with modern Python patterns
- VS Code settings with Black/Flake8/MyPy integration

### Added to generated projects
- pyproject.toml with full configuration
- Development tools setup (Black, Flake8, MyPy, pytest)
- Scripts folder with utility scripts
- Extensive documentation

## [1.0.3] - 2024-02-11

### Added
- Settings dialog for default values
- Menu system with File and Help
- Keyboard shortcuts (Enter for next, Shift+Tab for previous)
- Configurable editor path
- Help and Changelog dialogs
- About screen with version info
- Icons on all windows and menu items

### Improved
- Default author is automatically filled in
- Editor button now uses configurable path
- Better user experience with shortcuts

## [1.0.2] - 2024-02-11

### Added
- Result page after project creation
- Buttons: Open Project Folder, Open in Editor, New Project, Close
- Browsing starts by default at C:\ or configured root

### Improved
- Application no longer closes automatically
- User has full control after generation

## [1.0.1] - 2024-02-11

### Added
- Wizard interface for project creation
- Automatic folder structure generation
- Header rendering per file type
- Virtual environment support
- Export to USB script
- PyInstaller .spec template
- VS Code configuration

### Features
- Qt6 GUI
- Template-based system
- Extensible and maintainable
- Cross-platform compatible

## [1.0.0] - 2024-02-11

### Added
- Initial release
- Basic project generator functionality
