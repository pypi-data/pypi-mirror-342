# Text Segmentation Module

The `text` module provides functionality for segmenting and analyzing the structure of text documents, including lines, paragraphs, and sentences.

## Overview

This module focuses on identifying and analyzing the structural elements of text, which is essential for readability assessment, document structure analysis, and preprocessing for higher-level analysis.

## Core Components

The module is organized into two main parts:

1. **`mod.rs`**: Core module definitions and exports
2. **`segmentation.rs`**: Implementation of text segmentation algorithms

## Key Functions

### Line Segmentation

```rust
pub fn split_lines(text: &str) -> Vec<&str>
pub fn segment_lines(text: &str) -> Vec<String>
pub fn count_lines(text: &str) -> usize
pub fn average_line_length(text: &str) -> f64
```

These functions work with lines of text, splitting the text into lines, counting them, and calculating statistics like average line length.

### Paragraph Segmentation

```rust
pub fn split_paragraphs(text: &str) -> Vec<String>
pub fn segment_paragraphs(text: &str) -> Vec<String>
pub fn count_paragraphs(text: &str) -> usize
pub fn average_paragraph_length(text: &str) -> f64
```

These functions analyze paragraphs in text, identifying paragraph boundaries based on blank lines, and calculating statistics like paragraph count and average length.

### Sentence Segmentation

```rust
pub fn segment_sentences(text: &str) -> Vec<String>
pub fn average_sentence_length(text: &str) -> f64
```

These functions split text into sentences using heuristics for sentence boundaries (like periods, question marks, and exclamation points), and calculate statistics like average sentence length.

### Word Analysis

```rust
pub fn split_words(text: &str) -> Vec<&str>
pub fn count_words(text: &str) -> usize
pub fn average_word_length(text: &str) -> f64
```

These functions work with words in text, leveraging Unicode segmentation rules to identify word boundaries, and calculating statistics like word count and average word length.

## Implementation Details

### Line Segmentation

Lines are identified using both hard line breaks (`\n`, `\r\n`) and explicit line feeds. The module handles various newline formats across different operating systems consistently.

### Paragraph Segmentation

Paragraphs are identified by sequences of blank lines (two or more consecutive newlines). The implementation properly handles edge cases like leading and trailing blank lines.

### Sentence Segmentation

Sentence segmentation uses a combination of punctuation rules and heuristics to identify sentence boundaries. It handles:

- Terminal punctuation (`.`, `!`, `?`)
- Abbreviations and acronyms to avoid false sentence breaks
- List markers and formatting that could otherwise be confused with sentence boundaries

### Word Segmentation

Word segmentation uses the Unicode Text Segmentation algorithm (via the `unicode_segmentation` crate) to correctly handle word boundaries across different languages and scripts.

## Usage Examples

### Basic Text Segmentation

```rust
use cheesecloth::text::segmentation;

let text = "Hello, world!\nThis is a test paragraph.\n\nThis is another paragraph.";

// Count lines and paragraphs
let line_count = segmentation::count_lines(text); // 3
let paragraph_count = segmentation::count_paragraphs(text); // 2

// Get average lengths
let avg_line_length = segmentation::average_line_length(text);
let avg_paragraph_length = segmentation::average_paragraph_length(text);
```

### Splitting Text into Components

```rust
use cheesecloth::text::segmentation;

let text = "Hello, world! This is a test.";

// Split into sentences
let sentences = segmentation::segment_sentences(text);
// ["Hello, world!", "This is a test."]

// Split into words
let words = segmentation::split_words(text);
// ["Hello", "world", "This", "is", "a", "test"]
```

### Document Structure Analysis

```rust
use cheesecloth::text::segmentation;

let text = "Title\n\nFirst paragraph with multiple sentences. Another sentence here.\n\nSecond paragraph.";

// Get paragraph structure
let paragraphs = segmentation::segment_paragraphs(text);
// ["Title", "First paragraph with multiple sentences. Another sentence here.", "Second paragraph."]

// Calculate average sentence length in words
let avg_sent_len = segmentation::average_sentence_length(text); // 3.25
```

## Performance Considerations

- Most functions in this module require multiple passes through the text
- For very large texts, consider using the functions in the `batch` module
- The `segment_*` functions allocate new strings, while `split_*` functions return slices when possible
- For long documents (tens of thousands of lines), consider processing in chunks

## Python Integration

The module's functionality is exposed to Python through these functions:

```python
# Line analysis
split_lines(text: str) -> List[str]
segment_lines(text: str) -> List[str]
count_lines(text: str) -> int
average_line_length(text: str) -> float

# Paragraph analysis
split_paragraphs(text: str) -> List[str]
segment_paragraphs(text: str) -> List[str]
count_paragraphs(text: str) -> int
average_paragraph_length(text: str) -> float

# Sentence analysis
segment_sentences(text: str) -> List[str]
average_sentence_length(text: str) -> float

# Word analysis
split_words(text: str) -> List[str]
count_words(text: str) -> int
average_word_length(text: str) -> float
```