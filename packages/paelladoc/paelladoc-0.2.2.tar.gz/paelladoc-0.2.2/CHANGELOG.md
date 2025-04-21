# Changelog
All notable changes to PAELLADOC will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.2] - 2025-04-06

### Added
- Enhanced interactive documentation process with natural language flow
- Improved file creation reliability in PAELLA command
- More robust project memory tracking and updates

### Changed
- Refined PAELLA command to enforce strict question sequence
- Updated core rules structure for better modularity 
- Improved conversation workflows for better user experience

### Fixed
- Fixed file creation issues when using PAELLA command
- Resolved memory file update inconsistencies
- Fixed command behavior when handling multilingual projects

## [0.2.1] - 2025-04-06

### Added
- New `run_continue.py` script to improve the CONTINUE command functionality

### Changed
- Enhanced command interactivity for PAELLA and CONTINUE to present one question at a time
- Refactored underlying scripts to use relative paths instead of absolute ones
- Improved project detection in subdirectories for the CONTINUE command
- Updated `run_generate_doc.py` script for better portability

### Fixed
- Fixed command behavior to respect interactive configuration settings
- Resolved project root detection issues
- Fixed the CONTINUE script to display appropriate messages when no projects are available

## [0.2.0] - 2025-04-05

### Added
- **Dynamic Template-Based Menu System**: Replaced fixed menu with a dynamic menu generated from existing templates
- **Improved Multilingual Support**: Implemented full support for both Spanish and English in documentation generation
- New `enforce_fixed_menu.py` script modified to generate a dynamic menu from templates
- Documentation file creation now uses templates as structural guides
- Reorganized output instructions to save documentation to `/docs/generated/`
- Improved integration between dynamic menu and documentation file generation

### Changed
- GENERATE_DOC command configuration now supports additional templates
- Generated files are now always saved in `/docs/generated/` while following template structure
- Improved template organization and integration with the documentation system
- System now respects user's language selection, without forcing Spanish or English

### Fixed
- Fixed issues with documentation output file location
- Solved inconsistency between menu and available templates
- Improved documentation file saving process

## [0.1.0] - 2025-04-04

### Breaking Changes
- Implementation of repository documentation generation system (GENERATE_DOC)
- Addition of code repository analysis and documentation extraction capabilities
- Comprehensive reorganization of the `.cursor/rules` directory structure
- Enhanced modularity with clearer separation of concerns
- Addition of new interfaces and conversation workflows
- Improved documentation of the system architecture

### Added
- **Repository Analysis & Documentation**: New GENERATE_CONTEXT and GENERATE_DOC commands for code-to-documentation reverse engineering
- Repository context extraction scripts and analysis tools
- Interactive documentation generation from repository analysis
- Repository content extraction to optimized text format
- Architecture pattern detection and automatic documentation
- Multi-step repository documentation process with user guidance
- New help system in `core/help.mdc`
- User interface definitions in `features/interfaces.mdc`
- Enhanced conversation workflow in `features/conversation_workflow.mdc`
- Detailed directory structure documentation in `DIRECTORY_STRUCTURE.md`
- Feature mapping documentation in `feature_map.md`
- Configuration file for conversation flows in `paelladoc_conversation_config.json`
- New template directories:
  - `templates/conversation_flows/` for conversation configurations
  - `templates/methodologies/` for development methodologies
  - `templates/Product/` for main product documentation
  - `templates/scripts/` for template-specific scripts
  - `templates/selectors/` for selection guide templates
  - `templates/simplified_templates/` for simplified documentation
- Improved organization of code generation templates

### Changed
- Modular architecture with cleaner file organization
- Enhanced product management capabilities
- Improved code generation system
- Better documentation of the directory structure
- Enhanced mapping between features and their implementations
- Reorganized template structure for better maintainability

### Fixed
- Directory structure inconsistencies
- Feature implementation mapping gaps
- Template organization clarity
- Documentation of system architecture 