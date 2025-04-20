# Compression Metrics Module

The `compression` module provides functionality for measuring text complexity and information density using compression-based metrics.

## Overview

This module computes compression-based metrics which serve as proxies for text complexity, redundancy, and information density. By leveraging the deflate algorithm, the module can quantify how compressible a text is, which correlates with pattern repetition and text complexity.

## Core Concepts

### Compression Ratio

The compression ratio is calculated as:

```
compression_ratio = original_size / compressed_size
```

A high compression ratio indicates more repetitive or predictable text, while a low compression ratio suggests more varied or complex content.

### Normalized Compression Ratio

To make the metric more comparable across texts of different lengths, the normalized compression ratio adjusts for text size:

```
normalized_compression_ratio = (compression_ratio - 1) / (max_theoretical_ratio - 1)
```

This scales the ratio to a value between 0 and 1, where 0 represents completely incompressible text and 1 represents maximally compressible text.

### Compression Efficiency

Compression efficiency measures how close the achieved compression is to the theoretical maximum:

```
compression_efficiency = normalized_compression_ratio * 100
```

This is expressed as a percentage, indicating how much of the theoretical maximum compression was achieved.

## Key Functions

### Compression Ratio Calculation

```rust
pub fn calculate_compression_ratio(text: &str) -> Result<f64, CompressionError>
```

This function calculates the basic compression ratio by compressing the text using the deflate algorithm and comparing the sizes.

### All Compression Metrics

```rust
pub fn get_compression_metrics(text: &str) -> Result<HashMap<String, f64>, CompressionError>
```

This function calculates all compression-related metrics in a single operation, returning a map of metric names to values.

### Unigram Compression Ratio

```rust
pub fn unigram_compression_ratio(text: &str, include_punctuation: bool) -> Result<f64, CompressionError>
```

This function calculates the compression ratio specifically for unigram tokens, which can provide insights into word-level redundancy.

## Implementation Details

The module uses the `flate2` crate to apply the deflate compression algorithm. The implementation:

1. Encodes the input text as UTF-8 bytes
2. Compresses the bytes using the deflate algorithm with default settings
3. Measures the size of the compressed data
4. Calculates various ratios based on the original and compressed sizes

## Usage Examples

### Basic Compression Ratio

```rust
use cheesecloth::compression;

let text = "This is a sample text with some repetition. This is a sample text with some repetition.";
let ratio = compression::calculate_compression_ratio(text).unwrap();
println!("Compression ratio: {:.2}", ratio); // Higher due to repetition
```

### Comparing Text Complexity

```rust
use cheesecloth::compression;

let simple_text = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
let complex_text = "The quick brown fox jumps over the lazy dog";

let simple_metrics = compression::get_compression_metrics(simple_text).unwrap();
let complex_metrics = compression::get_compression_metrics(complex_text).unwrap();

println!("Simple text compression ratio: {:.2}", simple_metrics["compression_ratio"]); // Higher, more compressible
println!("Complex text compression ratio: {:.2}", complex_metrics["compression_ratio"]); // Lower, less compressible
```

### Analyzing Word-Level Redundancy

```rust
use cheesecloth::compression;

let text = "The cat sat on the mat. The dog sat on the mat.";
let unigram_ratio = compression::unigram_compression_ratio(text, false).unwrap();
println!("Unigram compression ratio: {:.2}", unigram_ratio); // Shows redundancy in unigrams
```

### Full Compression Analysis

```rust
use cheesecloth::compression;

let text = "Natural language processing (NLP) is a field that combines linguistics and AI.";
let metrics = compression::get_compression_metrics(text).unwrap();

println!("Compression ratio: {:.2}", metrics["compression_ratio"]);
println!("Normalized compression ratio: {:.2}", metrics["normalized_compression_ratio"]);
println!("Compression efficiency: {:.2}%", metrics["compression_efficiency"]);
```

## Error Handling

The module defines a `CompressionError` type to handle various error conditions:

```rust
pub enum CompressionError {
    IoError(std::io::Error),
    EmptyInput,
    ZeroCompressedSize,
}
```

All functions return a `Result` type, properly handling errors such as IO errors or edge cases like empty input.

## Performance Considerations

- Compression is computationally more expensive than other metrics
- For large texts, consider using the `batch` module for parallel processing
- The memory usage scales with text size, but is generally efficient
- Compression ratios are more meaningful for longer texts
- Very short texts (< 20 bytes) may give less reliable results

## Python Integration

The module's functionality is exposed to Python through these functions:

```python
# Basic compression metrics
compression_ratio(text: str) -> float

# Comprehensive compression metrics
get_compression_metrics(text: str) -> dict
# Returns: {'compression_ratio': float, 'normalized_compression_ratio': float, 'compression_efficiency': float}

# Word-level compression
unigram_compression_ratio(text: str, include_punctuation: bool) -> float
```

## Applications

Compression metrics are particularly useful for:

1. **Text Quality Assessment**: Detecting highly repetitive or synthetic text
2. **Content Complexity Analysis**: Measuring information density and complexity
3. **Duplicate Detection**: Identifying near-duplicate content
4. **Language Identification**: Different languages have different natural compression ratios
5. **Entropy Estimation**: Providing a model-free entropy approximation