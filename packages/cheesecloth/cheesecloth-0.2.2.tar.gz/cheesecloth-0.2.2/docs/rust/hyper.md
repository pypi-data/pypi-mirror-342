# HyperAnalyzer Module

The `hyper` module provides a high-performance, optimized analyzer that can calculate multiple metrics in a single pass through text, significantly improving efficiency for comprehensive text analysis.

## Overview

The HyperAnalyzer is designed for maximum efficiency when computing multiple metrics simultaneously. Unlike individual metric functions that each require a separate pass through the text, the HyperAnalyzer collects all necessary information in a single pass and then derives all metrics from that information.

## Core Components

### HyperAnalyzer Struct

The central component of this module is the `HyperAnalyzer` struct:

```rust
pub struct HyperAnalyzer {
    include_punctuation: bool,
    case_sensitive: bool,
    // Internal state and configuration...
}
```

This struct encapsulates all the logic for efficient text analysis and maintains configuration options.

### HyperTextMetrics Struct

The HyperAnalyzer produces a comprehensive metrics object:

```rust
pub struct HyperTextMetrics {
    // Character metrics
    pub char_count: usize,
    pub letter_count: usize,
    pub digit_count: usize,
    // ... many other metrics
}
```

This struct contains all calculated metrics in a structured format, which can then be converted to different output formats.

## Key Methods

### Creation and Configuration

```rust
impl HyperAnalyzer {
    pub fn new(include_punctuation: bool, case_sensitive: bool) -> Self
    // Additional configuration methods...
}
```

These methods create and configure a `HyperAnalyzer` instance with specific parameters.

### Analysis Methods

```rust
impl HyperAnalyzer {
    pub fn calculate_all_metrics(&self, text: &str) -> HashMap<String, f64>
    pub fn calculate_batch_metrics(&self, texts: &[String]) -> Vec<HashMap<String, f64>>
    // Additional analysis methods...
}
```

These methods perform the actual text analysis, either for a single text or a batch of texts.

## Implementation Details

### Single-Pass Algorithm

The HyperAnalyzer uses a single-pass algorithm that:

1. Processes each character in the text exactly once
2. Keeps track of counts, frequencies, and patterns as it goes
3. Dynamically updates Unicode category information
4. Builds token sequences for word-level analysis
5. Derives all metrics from the collected information after the pass

### Memory Efficiency

To maintain high performance even with large texts:

- The analyzer uses efficient data structures like hash maps and vectors
- It avoids unnecessary string allocations where possible
- It uses preallocated buffers for frequency counting
- It employs compact data representations for intermediate results

### Performance Optimizations

Several key optimizations enable the HyperAnalyzer's speed:

- Character type checks are optimized with lookup tables
- Token frequency calculations use specialized hash maps
- Pattern matching uses precompiled regular expressions
- The analyzer minimizes redundant calculations by sharing intermediate results

## Usage Examples

### Basic Analysis

```rust
use cheesecloth::hyper::HyperAnalyzer;

// Create an analyzer with desired settings
let analyzer = HyperAnalyzer::new(false, true);  // exclude_punctuation=false, case_sensitive=true

// Analyze a text
let text = "This is a sample text for analysis.";
let metrics = analyzer.calculate_all_metrics(text);

// Access individual metrics
println!("Character count: {}", metrics["char_count"]);
println!("Token count: {}", metrics["unigram_count"]);
println!("Type-token ratio: {:.2}", metrics["type_token_ratio"]);
println!("Character entropy: {:.2}", metrics["char_entropy"]);
```

### Batch Processing

```rust
use cheesecloth::hyper::HyperAnalyzer;

let analyzer = HyperAnalyzer::new(false, false);  // exclude_punctuation=false, case_sensitive=false

// Prepare a batch of texts
let texts = vec![
    "First document to analyze".to_string(),
    "Second document with different content".to_string(),
    "Third document for comparison".to_string(),
];

// Process the entire batch efficiently
let results = analyzer.calculate_batch_metrics(&texts);

// Compare metrics across documents
for (i, result) in results.iter().enumerate() {
    println!("Document {}: {} chars, {} tokens, {:.2} entropy",
             i + 1,
             result["char_count"],
             result["unigram_count"],
             result["char_entropy"]);
}
```

### Integration with Batch Processing

```rust
use cheesecloth::hyper::HyperAnalyzer;
use cheesecloth::batch::BatchProcessor;

// Create a hyper analyzer
let analyzer = HyperAnalyzer::new(false, true);

// Create a batch processor
let processor = BatchProcessor::new();

// Process a large collection of texts
let texts = vec![
    // Large collection of texts...
];

// Use the HyperAnalyzer via the batch processor for parallel processing
let results = processor.process_batch_with_hyper(texts);

// Analyze the results
let avg_ttr: f64 = results.iter()
    .map(|r| r["type_token_ratio"])
    .sum::<f64>() / results.len() as f64;

println!("Average type-token ratio: {:.3}", avg_ttr);
```

## Available Metrics

The HyperAnalyzer calculates a comprehensive set of metrics including:

### Character Metrics
- Character count
- Letter, digit, punctuation, symbol, whitespace counts
- Uppercase and lowercase counts
- ASCII and non-ASCII counts
- Various ratios (ASCII ratio, uppercase ratio, etc.)
- Character entropy

### Unigram Metrics
- Token count
- Unique token count
- Type-token ratio
- Token entropy
- Average token length
- Short and long token ratios

### Pattern Metrics
- *Optionally available if pattern detection is enabled*

### Segmentation Metrics
- Line and paragraph counts
- Average line and paragraph lengths
- Average sentence length

## Performance Considerations

- The HyperAnalyzer is most efficient when calculating many metrics for the same text
- For extremely large texts, memory usage could become a concern
- When processing multiple texts, batch processing is more efficient than sequential processing
- The initialization overhead is minimal, but reusing the same analyzer instance is still more efficient

## Python Integration

The module's functionality is exposed to Python through the `HyperAnalyzer` class:

```python
from cheesecloth import HyperAnalyzer

# Create an analyzer
analyzer = HyperAnalyzer(include_punctuation=False, case_sensitive=True)

# Analyze a single text
metrics = analyzer.calculate_all_metrics("Sample text to analyze.")

# Process a batch of texts
texts = ["First document", "Second document", ...]
batch_results = analyzer.calculate_batch_metrics(texts)
```

## Best Practices

1. **Reuse analyzer instances**: Create once, use many times
2. **Use for comprehensive analysis**: When you need many metrics, not just one or two
3. **Batch process when possible**: Process multiple texts in a single call
4. **Configure appropriately**: Set include_punctuation and case_sensitive according to your needs
5. **Consider memory usage**: For very large texts, monitor memory consumption

## Comparison with Individual Metrics

| Approach | Pros | Cons |
|----------|------|------|
| HyperAnalyzer | • Single pass through text<br>• Much faster for multiple metrics<br>• Consistent API for all metrics | • Higher memory usage<br>• Less flexibility for individual metrics |
| Individual functions | • Minimal memory usage<br>• More granular control<br>• Easier to understand | • Multiple passes through text<br>• Much slower for multiple metrics<br>• Inconsistent APIs |

For most applications requiring multiple metrics, the HyperAnalyzer is strongly recommended for its performance benefits.