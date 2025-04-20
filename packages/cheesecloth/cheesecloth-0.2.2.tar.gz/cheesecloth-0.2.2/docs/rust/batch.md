# Batch Processing Module

The `batch` module provides functionality for processing large volumes of text efficiently by parallelizing operations across multiple threads.

## Overview

This module enables the efficient processing of large datasets by distributing the computational workload across multiple CPU cores. It's particularly useful for large-scale text analysis where processing time would otherwise be prohibitive.

## Core Components

### BatchProcessor

The central component of this module is the `BatchProcessor` struct, which manages parallel execution of text analysis functions:

```rust
pub struct BatchProcessor {
    // Internal configuration and state
}
```

This struct provides methods for processing batches of text with various metrics and customization options.

## Key Methods

### Creation and Configuration

```rust
impl BatchProcessor {
    pub fn new() -> Self
    pub fn with_thread_count(mut self, thread_count: usize) -> Self
    pub fn with_metrics(mut self, metrics: Vec<String>) -> Self
    // Additional configuration methods...
}
```

These methods create and configure a `BatchProcessor` instance with specific parameters like thread count and which metrics to calculate.

### Processing Methods

```rust
impl BatchProcessor {
    pub fn process_batch(&self, texts: Vec<String>, metrics: Vec<String>) -> Vec<HashMap<String, f64>>
    pub fn process_batch_with_hyper(&self, texts: Vec<String>) -> Vec<HashMap<String, f64>>
    // Additional processing methods...
}
```

These methods process a batch of texts in parallel, either with specific metrics or using the optimized `HyperAnalyzer`.

## Implementation Details

- The module uses Rust's `rayon` crate for parallel processing
- Work is divided into chunks and distributed across available CPU cores
- Results are collected and aggregated after parallel processing
- Thread count can be customized or automatically determined based on available cores
- Individual metric calculations are isolated to prevent interference between threads

## Usage Examples

### Basic Batch Processing

```rust
use cheesecloth::batch::BatchProcessor;

let processor = BatchProcessor::new();
let texts = vec![
    "First document to analyze".to_string(),
    "Second document with different content".to_string(),
    "Third document with yet more variation".to_string(),
    // ... more texts
];

// Process with default metrics
let results = processor.process_batch(texts, vec!["char_count".to_string(), "token_count".to_string()]);

// Each result corresponds to one input text
for (i, result) in results.iter().enumerate() {
    println!("Document {}: {} characters, {} tokens", 
             i + 1, 
             result["char_count"], 
             result["token_count"]);
}
```

### Customized Batch Processing

```rust
use cheesecloth::batch::BatchProcessor;

// Create a customized batch processor
let processor = BatchProcessor::new()
    .with_thread_count(8)  // Use 8 threads
    .with_metrics(vec![    // Default metrics to calculate
        "char_count".to_string(),
        "token_count".to_string(),
        "type_token_ratio".to_string(),
    ]);

let texts = vec![
    // Large collection of texts...
];

// Process the batch
let results = processor.process_batch(texts, vec![]);  // Empty vec uses default metrics

// Aggregate some statistics
let avg_ttr: f64 = results.iter()
    .map(|r| r["type_token_ratio"])
    .sum::<f64>() / results.len() as f64;

println!("Average type-token ratio: {:.3}", avg_ttr);
```

### Using HyperAnalyzer for Comprehensive Metrics

```rust
use cheesecloth::batch::BatchProcessor;

let processor = BatchProcessor::new();
let texts = vec![
    // Collection of texts...
];

// Use HyperAnalyzer for comprehensive metrics in a single pass
let results = processor.process_batch_with_hyper(texts);

// Results contain all metrics calculated by HyperAnalyzer
for result in results {
    println!("Text complexity: {:.2}", result["char_entropy"]);
    println!("Lexical diversity: {:.2}", result["type_token_ratio"]);
    // ... other metrics
}
```

## Performance Considerations

- The optimal thread count depends on your CPU and the size of texts
- For very short texts, the overhead of parallelization might outweigh the benefits
- For very long texts, consider chunking them further to improve load balancing
- Memory usage scales with both the number of texts and the number of threads
- Some metrics are more CPU-intensive than others, which affects overall performance

## Python Integration

The module's functionality is exposed to Python through the `BatchProcessor` class:

```python
from cheesecloth import BatchProcessor

# Create a processor
processor = BatchProcessor()

# Process texts in parallel
texts = ["First document", "Second document", ...]
results = processor.process_batch(texts, ["char_count", "token_count"])

# Use HyperAnalyzer for comprehensive metrics
hyper_results = processor.process_batch_with_hyper(texts)
```

The Python API mirrors the Rust implementation while providing a Pythonic interface.

## Best Practices

1. **Right-size your batches**: Too small batches don't leverage parallelism, too large batches consume excessive memory
2. **Monitor resource usage**: Watch CPU and memory usage to find the optimal configuration
3. **Be metric-selective**: Only calculate the metrics you need to improve performance
4. **Consider data locality**: Group similar-length texts together for better load balancing
5. **Reuse processor instances**: Creating new processors has overhead, reuse them when processing multiple batches

## Applications

Batch processing is particularly useful for:

1. **Large Corpus Analysis**: Processing millions of documents efficiently
2. **Real-time Data Processing**: Handling streaming data with low latency
3. **Resource-constrained Environments**: Maximizing throughput on limited hardware
4. **Preprocessing for ML**: Preparing large datasets for machine learning models
5. **Interactive Applications**: Maintaining responsiveness while processing background data