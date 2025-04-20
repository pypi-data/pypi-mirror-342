# Unigram Analysis Module

The `unigram` module provides functionality for tokenizing text into linguistic words (unigrams) and analyzing these tokens with various metrics. Unlike subword tokenization used in machine learning models, unigram tokenization follows natural language word boundaries.

## Overview

This module focuses on word-level analysis, offering several key capabilities:
- Unicode-aware word segmentation
- Word frequency analysis
- Lexical diversity metrics
- Token length statistics
- Vocabulary richness measures

## Core Functions

### Tokenization

The module provides two primary tokenization functions:

```rust
pub fn tokenize(text: &str) -> Vec<String>
pub fn tokenize_with_punctuation(text: &str) -> Vec<String>
```

The first function (`tokenize`) extracts only words based on Unicode word boundaries, while the second function (`tokenize_with_punctuation`) preserves all characters including punctuation and whitespace as separate tokens.

### Token Counting

```rust
pub fn count_tokens(text: &str, include_punctuation: bool) -> usize
pub fn count_unique_tokens(text: &str, include_punctuation: bool, case_sensitive: bool) -> usize
```

These functions count the total number of tokens and unique tokens, respectively. The `include_punctuation` parameter determines whether punctuation tokens are included, and `case_sensitive` controls whether uppercase and lowercase versions of the same word are considered distinct tokens.

### Lexical Diversity

```rust
pub fn type_token_ratio(text: &str, include_punctuation: bool, case_sensitive: bool) -> f64
pub fn repetition_rate(text: &str, include_punctuation: bool, case_sensitive: bool) -> f64
```

The type-token ratio (TTR) is a measure of lexical diversity, calculated as the ratio of unique tokens to total tokens. The repetition rate is simply 1 - TTR, indicating how repetitive the text is.

### Token Frequency Analysis

```rust
pub fn token_frequency(text: &str, include_punctuation: bool, case_sensitive: bool) -> HashMap<String, usize>
pub fn max_token_frequency_ratio(text: &str, include_punctuation: bool, case_sensitive: bool) -> f64
```

The `token_frequency` function returns a map of each token to its frequency count, while `max_token_frequency_ratio` calculates the ratio of the most frequent token's count to the total token count.

### Information Theory

```rust
pub fn token_entropy(text: &str, include_punctuation: bool, case_sensitive: bool) -> f64
```

This function calculates the Shannon entropy of the token distribution, which is a measure of information content or uncertainty.

### Token Length Metrics

```rust
pub fn short_token_ratio(text: &str, include_punctuation: bool, case_sensitive: bool, threshold: Option<usize>) -> f64
pub fn long_token_ratio(text: &str, include_punctuation: bool, case_sensitive: bool, threshold: Option<usize>) -> f64
```

These functions calculate the proportion of tokens that are short (≤ 3 characters by default) or long (≥ 7 characters by default), respectively. The optional threshold parameter allows customizing the length thresholds.

### Vocabulary Richness

```rust
pub fn hapax_legomena_ratio(text: &str, include_punctuation: bool, case_sensitive: bool) -> f64
pub fn top_5_token_coverage(text: &str, include_punctuation: bool, case_sensitive: bool) -> f64
```

The hapax legomena ratio is the proportion of words that appear exactly once in the text, which is a measure of vocabulary richness. The top-5 token coverage calculates the percentage of the text covered by the 5 most frequent tokens.

### All-in-One Analysis

```rust
pub fn calculate_all_unigram_metrics(text: &str, include_punctuation: bool, case_sensitive: bool) -> UnigramMetrics
```

This function calculates all unigram metrics in a single pass, which is much more efficient than calling individual functions separately.

## The `UnigramMetrics` Struct

The module defines a comprehensive `UnigramMetrics` struct that holds all unigram metrics:

```rust
pub struct UnigramMetrics {
    pub token_count: usize,
    pub unique_token_count: usize,
    pub type_token_ratio: f64,
    pub repetition_rate: f64,
    pub token_entropy: f64,
    pub max_frequency_ratio: f64,
    pub average_token_length: f64,
    pub hapax_legomena_ratio: f64,
    pub top_5_token_coverage: f64,
    pub short_token_ratio: f64,
    pub long_token_ratio: f64,
}
```

## Usage Examples

### Basic Tokenization

```rust
use cheesecloth::unigram;

let text = "Hello, world! This is a test.";
let tokens = unigram::tokenize(text);
// ["Hello", "world", "This", "is", "a", "test"]

let tokens_with_punct = unigram::tokenize_with_punctuation(text);
// ["Hello", ",", " ", "world", "!", " ", "This", " ", "is", " ", "a", " ", "test", "."]
```

### Calculating Lexical Diversity

```rust
use cheesecloth::unigram;

let text = "The quick brown fox jumps over the lazy dog.";
let ttr = unigram::type_token_ratio(text, false, false);
// 0.875 (7 unique words out of 8 total words)
```

### Token Frequency Analysis

```rust
use cheesecloth::unigram;

let text = "To be or not to be, that is the question.";
let freq = unigram::token_frequency(text, false, false);
// {"to": 2, "be": 2, "or": 1, "not": 1, "that": 1, "is": 1, "the": 1, "question": 1}
```

### Comprehensive Analysis

```rust
use cheesecloth::unigram;

let text = "The quick brown fox jumps over the lazy dog.";
let metrics = unigram::calculate_all_unigram_metrics(text, false, false);
println!("Token count: {}", metrics.token_count);
println!("Type-token ratio: {}", metrics.type_token_ratio);
println!("Token entropy: {}", metrics.token_entropy);
```

## Edge Cases and Considerations

- **Empty texts**: All functions handle empty texts gracefully, typically returning 0 for counts and 0.0 for ratios.
- **Unicode handling**: The module uses the `unicode_segmentation` crate to ensure proper tokenization of Unicode text, including non-Latin scripts.
- **Case sensitivity**: Many functions have a `case_sensitive` parameter that controls whether uppercase and lowercase versions of the same word are considered distinct.
- **Punctuation handling**: The `include_punctuation` parameter allows flexibility in whether punctuation marks are treated as separate tokens.

## Performance Considerations

- The module is optimized for both small and large text inputs.
- For repeated analysis of the same text with different parameters, it's more efficient to tokenize once and reuse the tokens.
- The `calculate_all_unigram_metrics` function is significantly more efficient than calling individual functions.
- For very large texts, consider processing in chunks or using the `batch` module.

## Python Integration

All functions are exposed to Python through PyO3 bindings, providing a seamless experience for Python users:

```python
import cheesecloth

text = "The quick brown fox jumps over the lazy dog."
unigram_metrics = cheesecloth.get_all_unigram_metrics(text, include_punctuation=False, case_sensitive=False)
print(f"Type-token ratio: {unigram_metrics['type_token_ratio']}")
print(f"Token entropy: {unigram_metrics['token_entropy']}")
```

## Implementation Notes

- Tokenization follows Unicode word segmentation rules from the `unicode_segmentation` crate.
- The module provides support for CJK (Chinese, Japanese, Korean) text, but tokenization may be less accurate for these languages as they don't use whitespace to separate words.
- The implementation prioritizes correctness over raw speed, though performance is still very good.