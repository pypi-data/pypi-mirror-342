# Pattern Matching Module

The `patterns` module provides functionality for detecting and analyzing specific content patterns within text, such as questions, copyright notices, and code-like constructs.

## Overview

This module uses regular expressions and pattern matching techniques to identify various textual patterns that are indicators of content type, structure, and quality. These patterns can be used for content filtering, classification, and quality assessment.

## Core Components

The module is organized in `mod.rs` and includes:

1. **Pre-compiled Regular Expressions**: Efficient regex patterns for various content indicators
2. **Pattern Counting Functions**: Functions for counting occurrences of specific patterns
3. **Content Detection Functions**: Functions for detecting the presence of particular content types
4. **Optimized All-in-One Analysis**: Functions for efficiently computing all pattern metrics at once

## Key Regular Expressions

The module defines several pre-compiled regular expressions for pattern matching:

```rust
// Question patterns
pub static ref QUESTION_REGEX: Regex = Regex::new(r"(\S.+\?)\s*").unwrap();
pub static ref INTERROGATIVE_REGEX: Regex = Regex::new(r"(^|\n|\s)(Who|What|When|Where|Why|How)\s+\S.+\?\s*").unwrap();
pub static ref COMPLEX_INTERROGATIVE_REGEX: Regex = Regex::new(r"(^|\n|\s)(How many|What is|What are|How can|What can|What would|How would|How does|Why is|Why are|Where can|Where is|Who is|Who are|When will|When did|When is|When are)\s+\S.+\?\s*").unwrap();

// Content type patterns
pub static ref FACTUAL_STATEMENT_REGEX: Regex = Regex::new(r"(^|\n|\s)(In fact|A study|Research|Studies show|According to|It is known|It is proven|Evidence|Data)").unwrap();
pub static ref LOGICAL_REASONING_REGEX: Regex = Regex::new(r"(^|\n|\s)(Therefore|Thus|Hence|Consequently|As a result|Because|Since|Given that|It follows that|So|If.+then)").unwrap();
pub static ref SECTION_HEADING_REGEX: Regex = Regex::new(r"(^|\n|\s)(Chapter|Section|Part)\s+\d+:?\s").unwrap();
pub static ref COPYRIGHT_REGEX: Regex = Regex::new(r"©|Copyright|Copr\.").unwrap();
pub static ref RIGHTS_RESERVED_REGEX: Regex = Regex::new(r"(All|Some) (R|r)ights (R|r)eserved").unwrap();

// Format patterns
pub static ref BULLET_REGEX: Regex = Regex::new(r"(^|\n)\s*[-•*]\s+").unwrap();
pub static ref ELLIPSIS_REGEX: Regex = Regex::new(r"(^|\n)\s*\.{3}\s+").unwrap();
pub static ref CODE_REGEX: Regex = Regex::new(r"[{}\[\]<>]|\bfunction\b|\bclass\b|\bdef\b|\bvar\b|\blet\b|\bconst\b|\breturn\b|\bif\b|\belse\b|\bfor\b|\bwhile\b|\bimport\b").unwrap();
```

## Key Functions

### Question Detection

```rust
pub fn count_question_strings(text: &str) -> Result<usize, regex::Error>
pub fn count_interrogative_questions(text: &str) -> Result<usize, regex::Error>
pub fn count_complex_interrogatives(text: &str) -> Result<usize, regex::Error>
```

These functions identify and count different types of questions in the text, from simple question marks to complex interrogative forms.

### Content Type Detection

```rust
pub fn count_factual_statements(text: &str) -> Result<usize, regex::Error>
pub fn count_logical_reasoning(text: &str) -> Result<usize, regex::Error>
pub fn count_section_strings(text: &str) -> Result<usize, regex::Error>
pub fn count_copyright_mentions(text: &str) -> Result<usize, regex::Error>
pub fn count_rights_reserved(text: &str) -> Result<usize, regex::Error>
```

These functions identify specific content types such as factual statements, logical reasoning expressions, section headings, and copyright notices.

### Format Detection

```rust
pub fn contains_code_characters(text: &str) -> Result<bool, regex::Error>
pub fn bullet_or_ellipsis_lines_ratio(text: &str) -> Result<f64, regex::Error>
```

These functions detect formatting elements such as code-like constructs, bullet points, and ellipses.

### Generic Pattern Matching

```rust
pub fn count_regex_matches(text: &str, pattern: &str) -> Result<usize, regex::Error>
pub fn contains_regex_pattern(text: &str, pattern: &str) -> Result<bool, regex::Error>
pub fn contains_blacklist_substring(text: &str, blacklist: &[&str]) -> bool
```

These functions provide generic pattern matching capabilities for custom patterns and blacklisted terms.

### All-in-One Analysis

```rust
pub fn get_all_pattern_metrics(
    text: &str,
    use_paragraph_processing: bool,
    max_segment_size: usize
) -> PatternMetrics
```

This function efficiently computes all pattern metrics in a single pass, with optimizations for large texts.

## Optimizations for Large Texts

The module includes special optimizations for large texts:

1. **Paragraph Processing**: For large texts, patterns can be detected at the paragraph level instead of processing the entire text at once.
2. **Segmentation**: Very large paragraphs can be further broken down into lines for more efficient processing.
3. **Chunking**: Extremely long lines can be processed in fixed-size chunks to prevent regex catastrophic backtracking.

## Usage Examples

### Basic Pattern Detection

```rust
use cheesecloth::patterns;

let text = "What is the meaning of life? This is a complex question.";

// Count questions
let question_count = patterns::count_question_strings(text).unwrap(); // 1
let complex_questions = patterns::count_complex_interrogatives(text).unwrap(); // 1

// Check for code-like content
let contains_code = patterns::contains_code_characters("function hello() { return 'world'; }").unwrap(); // true
```

### Content Classification

```rust
use cheesecloth::patterns;

let text = "Copyright © 2025 Example Corp. All Rights Reserved.";

// Check for copyright notices
let copyright_mentions = patterns::count_copyright_mentions(text).unwrap(); // 1
let rights_reserved = patterns::count_rights_reserved(text).unwrap(); // 1
```

### Custom Pattern Matching

```rust
use cheesecloth::patterns;

let text = "User data: name=John email=john@example.com";

// Check for sensitive information patterns
let contains_email = patterns::contains_regex_pattern(text, r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b").unwrap(); // true
let contains_pii = patterns::contains_blacklist_substring(text, &["SSN", "password", "credit card"]); // false
```

### Comprehensive Pattern Analysis

```rust
use cheesecloth::patterns;

let text = "Section 1: Introduction\n\nWhat is machine learning? How can we define it?\n\nIn fact, according to research, machine learning is a subset of AI...";

// Get all pattern metrics in one pass
let metrics = patterns::get_all_pattern_metrics(text, true, 4096);
println!("Questions: {}", metrics.question_count); // 2
println!("Complex questions: {}", metrics.complex_interrogative_count); // 1
println!("Factual statements: {}", metrics.factual_statement_count); // 1
println!("Section headings: {}", metrics.section_heading_count); // 1
```

## Performance Considerations

- Regular expressions are pre-compiled for optimal performance
- The module uses lazy evaluation where possible
- For large texts, use `get_all_pattern_metrics` with paragraph processing
- Regular expression matching can be expensive for very large texts or complex patterns
- Consider excluding pattern metrics when processing extremely large corpora if speed is critical

## Python Integration

The module's functionality is exposed to Python through these functions:

```python
# Question detection
count_question_strings(text: str) -> int
count_interrogative_questions(text: str) -> int
count_complex_interrogatives(text: str) -> int

# Content type detection
count_factual_statements(text: str) -> int
count_logical_reasoning(text: str) -> int
count_section_strings(text: str) -> int
count_copyright_mentions(text: str) -> int
count_rights_reserved(text: str) -> int

# Format detection
contains_code_characters(text: str) -> bool
bullet_or_ellipsis_lines_ratio(text: str) -> float

# Generic pattern matching
count_regex_matches(text: str, pattern: str) -> int
contains_regex_pattern(text: str, pattern: str) -> bool
contains_blacklist_substring(text: str, blacklist: List[str]) -> bool

# All-in-one analysis
get_all_pattern_metrics(text: str, use_paragraph_processing: bool = True, max_segment_size: int = 4096) -> dict
```