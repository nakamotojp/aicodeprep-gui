# Changelog

# Changelog

## [0.5.0] - 2024-14-11 (Premium GUI Release)

### Added

- Premium Windows GUI Version
- Right-click context menu integration for Windows
- Enhanced file selection GUI with granular file inclusion/exclusion
- DPI awareness for better display on high-resolution screens

### New Features

- Interactive file selection before code preparation
- Checkbox-based file inclusion/exclusion
- Scalable UI with multiple theme options
- Windows Explorer context menu integration

### Changed

- Moved from free to premium model
- Lifetime license available for $7
- Enhanced configuration options
- Improved logging and error handling

## [0.2.2] - 2024-02-11

Minor tweaks and improvements

## [0.2.2] - 2024-07-11 (Nov 2nd 2024)

Minor tweaks

## [0.2.0] - 2024-02-11 (Nov 2nd 2024)

### Moved all hard coded options to the default_config.yaml file

### Added

- New `exclude_extensions` configuration option to exclude file types globally
- New `exclude_extensions` configuration option to exclude patterns like .min.js
- New `include_dirs` configuration option to explicitly include specific directories
- Enhanced priority system for file inclusion/exclusion rules
- Better support for user configuration overrides
- Updated and added some more exclusions that came up later when it would add unnecessary files

### Changed

- Improved file processing logic with clearer priority rules:
  1. Explicitly included files (highest priority)
  2. Explicitly excluded files
  3. Excluded extensions
  4. Code extensions (lowest priority)
- Enhanced directory processing logic:
  1. Explicitly included directories (highest priority)
  2. Explicitly excluded directories
  3. Normal directory processing
