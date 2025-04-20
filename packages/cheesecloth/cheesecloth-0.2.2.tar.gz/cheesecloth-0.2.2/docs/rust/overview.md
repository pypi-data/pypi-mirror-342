# Cheesecloth Rust Core Documentation

Cheesecloth is a high-performance text analysis library with a Rust core and Python bindings. The Rust implementation provides the computational backbone for efficient text processing, particularly for large datasets.

## Architecture Overview

The Rust codebase is organized into specialized modules, each handling a specific aspect of text analysis:

```
src/
├── batch/      # Parallel processing for large datasets
├── char/       # Character-level metrics and Unicode analysis
├── compression/# Text compression metrics
├── hyper/      # Optimized all-in-one analyzer
├── patterns/   # Regex pattern matching and content detection
├── text/       # Text segmentation and structure analysis
├── token/      # ML tokenizer integration
├── unigram/    # Word-level tokenization and metrics
├── zipf/       # Statistical distribution analysis
└── lib.rs      # PyO3 bindings and public API
```

## Key Design Principles

1. **Efficiency First**: Algorithms are designed to minimize allocations and optimize for both speed and memory usage.
2. **Single-Pass Analysis**: Where possible, metrics are calculated in a single pass through the text.
3. **Iterative Processing**: Large texts can be processed in chunks to avoid memory pressure.
4. **Composability**: Low-level functions can be composed into high-level metrics.
5. **Python Integration**: All functionality is exposed through PyO3 bindings for seamless Python usage.

## Core Components

### 1. Character Analysis (`char` module)

Provides character-level metrics including:
- Basic character counts and ratios
- Unicode category analysis
- Character entropy and frequency distributions
- Unicode category n-grams (bigrams and trigrams)

### 2. Unigram Analysis (`unigram` module)

Handles word-level tokenization and analysis:
- Word boundary detection using Unicode segmentation rules
- Type-token ratio and lexical diversity metrics
- Word frequency distributions
- Token length metrics

### 3. Text Segmentation (`text` module)

Analyzes document structure:
- Line, paragraph, and sentence segmentation
- Length statistics for document components
- Whitespace and formatting analysis

### 4. Pattern Matching (`patterns` module)

Detects content characteristics:
- Question and interrogative detection
- Section headings and document structure
- Copyright and legal notices
- Code-like content detection
- Bullet points and formatted text

### 5. Compression Metrics (`compression` module)

Measures information density:
- Raw and normalized compression ratios
- Compression efficiency 
- Text complexity estimation

### 6. Statistical Analysis (`zipf` module)

Examines statistical properties:
- Zipf's law fitness calculation
- Power law exponent estimation
- Token burstiness measurement
- Vocabulary growth analysis

### 7. ML Tokenization (`token` module)

Integrates with ML tokenizers:
- BPE and WordPiece tokenization metrics
- Subword token analysis
- Tokenization efficiency metrics

### 8. Optimized Processing

Two approaches for efficient processing:
- **BatchProcessor**: Parallel execution for large datasets
- **HyperAnalyzer**: One-pass computation of all metrics

## Python Integration

All Rust functions are exposed through PyO3 bindings in `lib.rs`, which creates the Python module structure.
The bindings handle type conversions, error handling, and optional parameters to provide a Pythonic interface.

## Thread Safety and Parallelism

The library is designed to be thread-safe:
- No shared mutable state between functions
- Immutable input parameters
- Send and Sync traits respected throughout
- BatchProcessor for efficient parallel execution

## Next Steps

For detailed documentation on each module, see the individual module pages:
- [Character Module](./char.md)
- [Unigram Module](./unigram.md)
- [Text Segmentation Module](./text.md)
- [Pattern Matching Module](./patterns.md)
- [Compression Module](./compression.md)
- [Zipf Module](./zipf.md)
- [Token Module](./token.md)
- [Batch Processing Module](./batch.md)
- [Hyper Analyzer Module](./hyper.md)