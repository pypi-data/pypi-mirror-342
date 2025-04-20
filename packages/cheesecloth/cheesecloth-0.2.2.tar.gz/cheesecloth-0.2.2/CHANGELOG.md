# Changelog

## v0.2.2 (2025-04-19)

### Features
- Added Unicode category trigram analysis for deeper text structure insights
- Implemented advanced character type transition metrics
- Enhanced `CharMetrics` class with trigram support and new convenience properties
- Improved batch processing with parallel execution capabilities
- Added comprehensive README with clear examples, badges, and navigation links

### Improvements
- Added type stubs for missing trigram functions in `__init__.pyi`
- Optimized unigram frequency analysis and improved bigram handling
- Enhanced pattern matching with more efficient regex implementations
- Expanded test coverage for Unicode category trigrams

### Documentation
- Reorganized README.md for better clarity, usability and PyPI presentation
- Added badges for PyPI version and license information
- Improved examples with verified, working code snippets and expected outputs
- Enhanced code documentation with better type annotations

## v0.2.1 (2025-04-15)

### Improvements
- Added package configuration to exclude test files and example data from distributions
- Created MANIFEST.in to control Python package contents
- Added Cargo package exclusions for cleaner builds

## v0.2.0 (2025-04-15)

### Features
- Reorganized metric groups in CLI to align with Rust library structure
- Added readability metrics group with comprehensive readability assessment
- Added typed wrapper classes with convenience methods for better IDE support
- Added optimized metrics calculation mode with `--use-optimized-metrics` flag
- Enhanced pattern matching with pre-compiled regex patterns

### Documentation
- Added comprehensive metrics documentation in IMPLEMENTED_METRICS.md
- Updated README with new functionality examples
- Added extensive Python type annotations for better developer experience

### Performance
- Excluded slow pattern group from "all" option by default
- Improved metric group detection logic
- Enhanced JSON serialization handling for complex metrics

## v0.1.0 (2025-04-14)

### Features
- Initial release with comprehensive text metrics implementation
- High-performance Rust core with Python bindings
- CLI tools for dataset analysis
- Support for character, unigram, and token-level metrics
- Integration with machine learning tokenizers