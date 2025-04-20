# Character Analysis Module

The `char` module forms the foundation of Cheesecloth's text analysis capabilities, providing comprehensive character-level metrics for detailed text processing.

## Overview

This module contains specialized tools for analyzing text at its most granular level - the individual character. It offers character classification, counting, frequency analysis, and statistical measures that serve as building blocks for higher-level text analysis functions.

## Architecture

The module is divided into two primary submodules:

1. **`unicode.rs`**: Core character analysis functions and metrics
2. **`categories.rs`**: Unicode category classification and analysis

## Key Features

### Character Classification

The module provides a comprehensive set of character classification functions:

```rust
pub fn is_letter(ch: char) -> bool
pub fn is_digit(ch: char) -> bool
pub fn is_punctuation(ch: char) -> bool
pub fn is_symbol(ch: char) -> bool
pub fn is_whitespace(ch: char) -> bool
pub fn is_uppercase(ch: char) -> bool
pub fn is_lowercase(ch: char) -> bool
pub fn is_alphanumeric(ch: char) -> bool
pub fn is_ascii(text: &str) -> bool
```

### Character Counting

A suite of functions for counting characters by different categories:

```rust
pub fn count_chars(text: &str) -> usize
pub fn count_letters(text: &str) -> usize
pub fn count_digits(text: &str) -> usize
pub fn count_punctuation(text: &str) -> usize
pub fn count_symbols(text: &str) -> usize
pub fn count_whitespace(text: &str) -> usize
pub fn count_non_ascii(text: &str) -> usize
pub fn count_uppercase(text: &str) -> usize
pub fn count_lowercase(text: &str) -> usize
pub fn count_alphanumeric(text: &str) -> usize
```

### Ratio Calculations

Functions for calculating the proportion of different character types:

```rust
pub fn ratio_ascii(text: &str) -> f64
pub fn ratio_uppercase(text: &str) -> f64
pub fn ratio_alphanumeric(text: &str) -> f64
pub fn ratio_alpha_to_numeric(text: &str) -> f64
pub fn ratio_whitespace(text: &str) -> f64
pub fn ratio_digits(text: &str) -> f64
pub fn ratio_punctuation(text: &str) -> f64
pub fn case_ratio(text: &str) -> f64
```

### Pattern Analysis

Functions for analyzing character patterns in text:

```rust
pub fn count_char_type_transitions(text: &str) -> usize
pub fn count_consecutive_runs(text: &str) -> usize
pub fn punctuation_diversity(text: &str) -> usize
```

### Statistical Measures

Functions for calculating statistical properties of character distributions:

```rust
pub fn char_entropy(text: &str) -> f64
pub fn category_entropy(text: &str) -> f64
pub fn char_frequency(text: &str) -> std::collections::HashMap<char, usize>
pub fn char_type_frequency(text: &str) -> std::collections::HashMap<&'static str, usize>
```

### Optimized Analysis

Efficient all-in-one functions for calculating multiple metrics in a single pass:

```rust
pub fn calculate_char_metrics(text: &str) -> CharMetrics
pub fn combined_char_metrics(text: &str) -> std::collections::HashMap<&'static str, usize>
```

## Unicode Category Analysis

The `categories.rs` submodule extends character analysis to Unicode categories and provides:

1. **Unicode Category Classification**: Maps each character to its Unicode category
2. **Bigram Analysis**: Analyzes transitions between different Unicode categories
3. **Trigram Analysis**: Captures three-character patterns of Unicode categories
4. **Frequency Analysis**: Computes frequency distributions of Unicode categories

## Design Principles

1. **Performance**: Optimized for minimum allocations and efficient processing
2. **Single Pass**: Where possible, multiple metrics are calculated in a single pass
3. **Graceful Handling**: Empty strings and edge cases are handled consistently
4. **Unicode Awareness**: Full support for non-ASCII text and Unicode categories
5. **Thread Safety**: All functions are thread-safe with no shared mutable state

## The `CharMetrics` Struct

The module defines a comprehensive `CharMetrics` struct that holds all character metrics:

```rust
pub struct CharMetrics {
    // Count metrics
    pub total_chars: usize,
    pub letters: usize,
    pub digits: usize,
    pub punctuation: usize,
    pub symbols: usize,
    pub whitespace: usize,
    pub non_ascii: usize,
    pub uppercase: usize,
    pub lowercase: usize,
    pub alphanumeric: usize,
    
    // Pattern metrics
    pub char_type_transitions: usize,
    pub consecutive_runs: usize,
    pub punctuation_diversity: usize,
    
    // Ratio metrics
    pub ratio_letters: f64,
    pub ratio_digits: f64,
    pub ratio_punctuation: f64,
    pub ratio_symbols: f64,
    pub ratio_whitespace: f64,
    pub ratio_non_ascii: f64,
    pub ratio_uppercase: f64,
    pub ratio_lowercase: f64,
    pub ratio_alphanumeric: f64,
    pub ratio_alpha_to_numeric: f64,
    pub char_entropy: f64,
    pub case_ratio: f64,
    pub category_entropy: f64,
}
```

## Usage Examples

### Basic Character Counting

```rust
let text = "Hello, World!";
let letter_count = char::unicode::count_letters(text); // 10
let uppercase_count = char::unicode::count_uppercase(text); // 2
let ascii_ratio = char::unicode::ratio_ascii(text); // 1.0
```

### Calculating Entropy

```rust
let text = "abcdefg";
let entropy = char::unicode::char_entropy(text); // Maximum for this length
```

### All-in-One Analysis

```rust
let text = "Hello, World! 123";
let metrics = char::unicode::calculate_char_metrics(text);
println!("Letters: {}", metrics.letters);
println!("Uppercase ratio: {}", metrics.ratio_uppercase);
println!("Character entropy: {}", metrics.char_entropy);
```

### Unicode Category Analysis

```rust
let text = "Hello, 世界!";
let category_counts = char::categories::count_categories(text);
let category_ratios = char::categories::category_ratios(text);
let bigrams = char::categories::category_bigram_ratios(text);
```

## Performance Considerations

- The module is optimized for both small and large text inputs
- For extremely large texts (millions of characters), consider using the `batch` module
- The `calculate_char_metrics` function is significantly more efficient than calling individual functions
- All functions are designed to be memory-efficient with minimal allocations

## Python Integration

All core functionality is exposed to Python through PyO3 bindings, providing a seamless experience for Python users while maintaining the performance benefits of Rust implementation.

```python
import cheesecloth

text = "Hello, World!"
metrics = cheesecloth.get_all_char_metrics(text)
print(f"Letters: {metrics['letter_count']}")
print(f"ASCII ratio: {metrics['ascii_ratio']}")
```