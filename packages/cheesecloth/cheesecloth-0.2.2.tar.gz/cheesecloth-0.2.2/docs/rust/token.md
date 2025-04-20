# ML Tokenization Module

The `token` module provides functionality for working with machine learning tokenizers like BPE, WordPiece, and SentencePiece, and analyzing the resulting token statistics.

## Overview

This module bridges the gap between linguistic word-level analysis and machine learning tokenization approaches. It allows for the tokenization of text using popular ML tokenizers and provides metrics to analyze the tokenization quality and efficiency.

## Core Concepts

### ML Tokenizers

Machine learning tokenizers like BPE (Byte Pair Encoding), WordPiece, and SentencePiece break words into subword units, which can capture morphological patterns and handle out-of-vocabulary words better than traditional word tokenization. These tokenizers are crucial for modern language models like GPT, BERT, and T5.

### Tokenization Efficiency

Tokenization efficiency measures how well a tokenizer compresses text into tokens, which directly impacts model performance and computational efficiency.

## Key Functions

### Tokenization

```rust
pub fn tokenize(text: &str, tokenizer_path: Option<&str>) -> Result<Vec<u32>, TokenizerError>
pub fn batch_tokenize(texts: &[&str], tokenizer_path: Option<&str>) -> Result<Vec<Vec<u32>>, TokenizerError>
```

These functions tokenize text using a machine learning tokenizer, either specified by path or using a default tokenizer (typically GPT-2).

### Token Count Metrics

```rust
pub fn subword_token_count(text: &str, tokenizer_path: Option<&str>) -> Result<usize, TokenizerError>
pub fn unique_subword_count(text: &str, tokenizer_path: Option<&str>) -> Result<usize, TokenizerError>
```

These functions count the total and unique tokens produced by the tokenizer for a given text.

### Token Diversity Metrics

```rust
pub fn subword_type_token_ratio(text: &str, tokenizer_path: Option<&str>) -> Result<f64, TokenizerError>
pub fn subword_repetition_rate(text: &str, tokenizer_path: Option<&str>) -> Result<f64, TokenizerError>
```

These functions calculate lexical diversity metrics specifically for subword tokens, similar to those in the `unigram` module but applied to ML tokenizer outputs.

### Token Information Metrics

```rust
pub fn subword_entropy(text: &str, tokenizer_path: Option<&str>) -> Result<f64, TokenizerError>
pub fn subword_efficiency(text: &str, tokenizer_path: Option<&str>) -> Result<f64, TokenizerError>
```

These functions calculate information-theoretic measures of the token distribution and efficiency of the tokenization.

### Comprehensive Token Metrics

```rust
pub fn get_token_metrics(text: &str, tokenizer_path: Option<&str>) -> Result<HashMap<String, f64>, TokenizerError>
```

This function calculates all token-related metrics in a single operation, returning a map of metric names to values.

## Error Handling

The module defines a `TokenizerError` type for handling various error conditions:

```rust
pub enum TokenizerError {
    TokenizerLoadError(String),
    TokenizationError(String),
    EmptyInput,
    // Additional error variants...
}
```

All functions return a `Result` type, properly handling errors such as tokenizer loading failures or empty input.

## Implementation Details

- The module uses the `tokenizers` crate from Hugging Face for ML tokenizer integration
- Tokenizers can be loaded from a local path or from the Hugging Face model hub
- Default tokenizer is GPT-2, but any compatible tokenizer can be used
- All metrics handle edge cases like empty text or single-token documents gracefully

## Usage Examples

### Basic Tokenization

```rust
use cheesecloth::token;

let text = "Hello, world!";
let tokens = token::tokenize(text, None).unwrap(); // Uses default GPT-2 tokenizer
println!("Token IDs: {:?}", tokens);

// Batch tokenization
let texts = &["Hello, world!", "This is another example."];
let batch_tokens = token::batch_tokenize(texts, None).unwrap();
println!("Number of texts tokenized: {}", batch_tokens.len());
```

### Tokenization Analysis

```rust
use cheesecloth::token;

let text = "Natural language processing with transformers is powerful.";
let token_count = token::subword_token_count(text, None).unwrap();
let unique_count = token::unique_subword_count(text, None).unwrap();

println!("Total tokens: {}", token_count);
println!("Unique tokens: {}", unique_count);
println!("Type-token ratio: {:.2}", unique_count as f64 / token_count as f64);
```

### Using Custom Tokenizers

```rust
use cheesecloth::token;

let text = "Ein Beispiel in Deutsch."; // "An example in German."
let tokens = token::tokenize(text, Some("bert-base-german-cased")).unwrap();
println!("German BERT tokens: {:?}", tokens);
```

### Comprehensive Token Analysis

```rust
use cheesecloth::token;

let text = "Machine learning models use subword tokenization to handle unknown words efficiently.";
let metrics = token::get_token_metrics(text, None).unwrap();

println!("Token count: {}", metrics["subword_token_count"]);
println!("Token entropy: {:.2}", metrics["subword_entropy"]);
println!("Tokenization efficiency: {:.2}", metrics["subword_efficiency"]);
```

## Performance Considerations

- Loading tokenizers can be time-consuming, so reuse tokenizers when processing multiple texts
- For large datasets, use `batch_tokenize` for better performance
- Tokenizer models can be large, so be mindful of memory usage
- Consider caching tokenization results if the same text is analyzed multiple times

## Python Integration

The module's functionality is exposed to Python through these functions:

```python
# Basic tokenization
tokenize_ml(text: str, tokenizer_path: Optional[str] = None) -> List[int]
batch_tokenize_ml(texts: List[str], tokenizer_path: Optional[str] = None) -> List[List[int]]

# Token count metrics
subword_token_count(text: str, tokenizer_path: Optional[str] = None) -> int
unique_subword_count(text: str, tokenizer_path: Optional[str] = None) -> int

# Token diversity metrics
subword_type_token_ratio(text: str, tokenizer_path: Optional[str] = None) -> float
subword_repetition_rate(text: str, tokenizer_path: Optional[str] = None) -> float

# Token information metrics
subword_entropy(text: str, tokenizer_path: Optional[str] = None) -> float
subword_efficiency(text: str, tokenizer_path: Optional[str] = None) -> float

# Comprehensive token metrics
get_token_metrics(text: str, tokenizer_path: Optional[str] = None) -> dict
```

## Applications

ML tokenization metrics are particularly useful for:

1. **Tokenizer Comparison**: Evaluating different tokenizers for a specific language or domain
2. **Content Complexity**: Measuring complexity in terms of token distribution
3. **Model Efficiency**: Predicting computational requirements for processing text with LLMs
4. **Language Identification**: Different languages tokenize differently
5. **Code vs Text Detection**: Code often has distinct tokenization patterns compared to natural language
6. **Domain-Specific Analysis**: Technical texts often have different tokenization efficiency than general text