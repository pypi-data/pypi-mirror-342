# Zipf's Law and Statistical Distribution Module

The `zipf` module provides functionality for analyzing statistical properties of word frequencies in text, particularly focusing on Zipf's law and related statistical distributions.

## Overview

This module implements metrics that analyze the statistical distribution of word frequencies, which can provide insights into text quality, authorship, and linguistic properties. A key focus is analyzing adherence to Zipf's law, a linguistic phenomenon where word frequency is inversely proportional to its frequency rank.

## Core Concepts

### Zipf's Law

Zipf's law states that the frequency of any word is inversely proportional to its rank in the frequency table. Mathematically:

```
f(r) ∝ 1/r^α
```

Where:
- `f(r)` is the frequency of the word with rank `r`
- `α` is the power law exponent (approximately 1 for natural language)

### Burstiness

Burstiness measures how words cluster or appear in bursts within text, rather than being evenly distributed:

```
burstiness = (variance - mean) / (variance + mean)
```

A higher value indicates more bursty (clustered) occurrences.

### Vocabulary Growth

Vocabulary growth analyzes how the number of unique words grows as more text is processed, which can be a marker of writing style and text complexity.

## Key Functions

### Zipf Fitness Analysis

```rust
pub fn calculate_zipf_fitness(frequencies: &HashMap<String, usize>) -> f64
```

This function quantifies how well a text's word frequency distribution follows Zipf's law, returning a value between 0 and 1, where 1 indicates perfect adherence.

### Power Law Exponent Estimation

```rust
pub fn estimate_power_law_exponent(frequencies: &HashMap<String, usize>) -> f64
```

This function estimates the exponent of the power law distribution that best fits the observed word frequencies.

### Burstiness Calculation

```rust
pub fn calculate_burstiness(text: &str, tokens_of_interest: &[&str]) -> f64
```

This function measures the burstiness of specified tokens within the text, indicating whether they appear in clusters or are evenly distributed.

### Vocabulary Growth Analysis

```rust
pub fn analyze_vocab_growth(text: &str, chunk_size: usize) -> VocabGrowthStats
```

This function analyzes how vocabulary size grows as more text is processed, dividing the text into chunks and tracking new words per chunk.

### All Zipf Metrics

```rust
pub fn get_zipf_metrics(frequencies: &HashMap<String, usize>) -> HashMap<String, f64>
```

This function calculates all Zipf-related metrics in a single operation, returning a map of metric names to values.

## Structures

### VocabGrowthStats

```rust
pub struct VocabGrowthStats {
    pub chunks_analyzed: usize,
    pub average_new_tokens_per_chunk: f64,
    pub cumulative_vocab_sizes: Vec<usize>,
}
```

This structure holds statistics about vocabulary growth throughout a text.

## Implementation Details

- Zipf fitness is calculated using a regression model on log-transformed frequency and rank data
- Burstiness calculation divides text into windows and analyzes token distribution
- Power law exponent is estimated using maximum likelihood estimation
- All functions handle edge cases like empty text or single-word documents gracefully

## Usage Examples

### Measuring Zipf's Law Adherence

```rust
use cheesecloth::unigram;
use cheesecloth::zipf;
use std::collections::HashMap;

let text = "The quick brown fox jumps over the lazy dog. The dog barks at the fox.";
let frequencies = unigram::token_frequency(text, false, false);
let fitness = zipf::calculate_zipf_fitness(&frequencies);

println!("Zipf fitness score: {:.2}", fitness); // How well the text follows Zipf's law
```

### Analyzing Word Burstiness

```rust
use cheesecloth::zipf;

let text = "The cat sat on the mat. The cat was happy on its mat. Another cat came to the mat.";
let burstiness = zipf::calculate_burstiness(text, &["cat", "mat"]);

println!("Burstiness score: {:.2}", burstiness); // Higher if "cat" and "mat" appear in clusters
```

### Vocabulary Growth Analysis

```rust
use cheesecloth::zipf;

let text = "This is a long text. It has many unique words. As we read more of the text, we encounter more and more unique words. However, the rate of new word introduction typically slows down as we progress through the text.";
let growth_stats = zipf::analyze_vocab_growth(text, 10);

println!("Average new tokens per chunk: {:.2}", growth_stats.average_new_tokens_per_chunk);
println!("Final vocabulary size: {}", growth_stats.cumulative_vocab_sizes.last().unwrap());
```

### Comprehensive Zipf Analysis

```rust
use cheesecloth::unigram;
use cheesecloth::zipf;

let text = "Natural language follows certain statistical patterns. One of the most well-known patterns is Zipf's law, which describes the relationship between word frequency and rank. Common words like 'the' and 'a' occur very frequently, while specialized terms occur rarely.";
let frequencies = unigram::token_frequency(text, false, false);
let metrics = zipf::get_zipf_metrics(&frequencies);

println!("Zipf fitness score: {:.2}", metrics["zipf_fitness_score"]);
println!("Power law exponent: {:.2}", metrics["power_law_exponent"]);
```

## Performance Considerations

- Zipf analysis requires a complete frequency distribution, which can be memory-intensive for large texts
- For very large texts, consider sampling or chunking the text
- Burstiness calculation scales with both text length and number of tokens of interest
- Vocabulary growth analysis requires tracking unique words, which uses O(n) memory where n is vocabulary size

## Python Integration

The module's functionality is exposed to Python through these functions:

```python
# Zipf's law analysis
zipf_fitness_score(text: str, include_punctuation: bool, case_sensitive: bool) -> float
power_law_exponent(text: str, include_punctuation: bool, case_sensitive: bool) -> float

# Burstiness analysis
calculate_burstiness(text: str, tokens: List[str]) -> float

# Vocabulary growth analysis
analyze_vocab_growth(text: str, chunk_size: int) -> dict
# Returns: {'chunks_analyzed': int, 'average_new_tokens_per_chunk': float, 'cumulative_vocab_sizes': List[int]}

# All Zipf metrics
get_zipf_metrics(text: str, include_punctuation: bool, case_sensitive: bool) -> dict
# Returns: {'zipf_fitness_score': float, 'power_law_exponent': float}
```

## Applications

Statistical distribution metrics are particularly useful for:

1. **Authorship Attribution**: Different authors exhibit different adherence to Zipf's law
2. **Text Quality Assessment**: Natural human text generally follows Zipf's law more closely than synthetic text
3. **Language Identification**: Different languages have different characteristic power law exponents
4. **Stylistic Analysis**: Burstiness can reveal stylistic patterns of word usage
5. **Content Complexity**: Vocabulary growth rate can indicate lexical sophistication