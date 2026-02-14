# Changelog

All changes to the Project Generator are documented here.

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
