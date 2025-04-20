# Cheesecloth Documentation

This directory contains comprehensive documentation for the Cheesecloth text analysis library, covering both the Rust core and Python bindings.

## Documentation Structure

```
docs/
├── README.md                  # This file
├── rust/                      # Rust core documentation
│   ├── overview.md            # Overview of the Rust implementation
│   ├── char.md                # Character analysis module
│   ├── unigram.md             # Unigram tokenization and analysis
│   ├── text.md                # Text segmentation module
│   ├── patterns.md            # Pattern matching module
│   ├── compression.md         # Compression metrics module
│   ├── zipf.md                # Statistical distributions module
│   ├── token.md               # ML tokenization module
│   ├── batch.md               # Batch processing module
│   └── hyper.md               # Hyper-optimized analyzer
├── python/                    # Python API documentation
│   ├── getting_started.md     # Getting started guide
│   ├── advanced_usage.md      # Advanced usage patterns
│   ├── api_reference.md       # Complete API reference
│   └── cli.md                 # Command-line interface guide
```

## Core Documentation

- [Rust Core Overview](rust/overview.md): Overview of the Rust implementation and architecture
- [Python Getting Started](python/getting_started.md): Introduction to using Cheesecloth in Python
- [Complete Metrics List](../METRICS.md): Comprehensive list of all available metrics

## Rust Core Documentation

The Rust core provides the computational foundation for Cheesecloth, implementing all metrics with high performance:

- [Character Analysis](rust/char.md): Character-level metrics and Unicode analysis
- [Unigram Analysis](rust/unigram.md): Word tokenization and lexical diversity metrics
- [Text Segmentation](rust/text.md): Line, paragraph, and sentence segmentation
- [Pattern Matching](rust/patterns.md): Content pattern detection and analysis
- [Compression Metrics](rust/compression.md): Text complexity measures using compression
- [Statistical Distributions](rust/zipf.md): Zipf's law and statistical analysis
- [ML Tokenization](rust/token.md): Machine learning tokenizer integration
- [Batch Processing](rust/batch.md): Parallel processing for large datasets
- [Hyper Analyzer](rust/hyper.md): Optimized all-in-one metrics calculation

## Python API Documentation

The Python API provides a user-friendly interface to the Rust core:

- [Getting Started](python/getting_started.md): Basic usage and examples
- [Advanced Usage](python/advanced_usage.md): Advanced techniques and patterns
- [API Reference](python/api_reference.md): Complete reference of all Python functions
- [CLI Guide](python/cli.md): Using the command-line interface

## Additional Resources

- [Examples](../examples/): Practical examples of using Cheesecloth
- [CHANGELOG](../CHANGELOG.md): Version history and changes
- [DEVELOPING](../DEVELOPING.md): Guidelines for contributing to Cheesecloth

## Using This Documentation

- **New Users**: Start with the [Python Getting Started](python/getting_started.md) guide
- **Advanced Users**: Check the [Advanced Usage](python/advanced_usage.md) guide
- **Developers**: Explore the [Rust Core Overview](rust/overview.md) and module documentation
- **Data Scientists**: See the [CLI Guide](python/cli.md) for batch processing datasets