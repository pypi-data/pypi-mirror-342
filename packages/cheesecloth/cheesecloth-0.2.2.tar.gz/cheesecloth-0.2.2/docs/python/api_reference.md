# Cheesecloth Python API Reference

This document provides a comprehensive reference for the Python API of Cheesecloth.

## Core Functions

### Character Analysis

**Basic Character Metrics**

```python
# Count characters
count_chars(text: str) -> int

# Check if text is ASCII
is_ascii(text: str) -> bool

# Calculate ASCII ratio
ratio_ascii(text: str) -> float

# Get character metrics all at once (most efficient)
get_all_char_metrics(text: str) -> dict
```

**Character Counting Functions**

```python
count_letters(text: str) -> int
count_digits(text: str) -> int
count_punctuation(text: str) -> int
count_symbols(text: str) -> int
count_whitespace(text: str) -> int
count_non_ascii(text: str) -> int
count_uppercase(text: str) -> int
count_lowercase(text: str) -> int
count_alphanumeric(text: str) -> int
```

**Character Ratio Functions**

```python
ratio_uppercase(text: str) -> float
ratio_alphanumeric(text: str) -> float
ratio_alpha_to_numeric(text: str) -> float
ratio_whitespace(text: str) -> float
ratio_digits(text: str) -> float
ratio_punctuation(text: str) -> float
```

**Character Classification Functions**

```python
is_letter(ch: str) -> bool
is_digit(ch: str) -> bool
is_punctuation(ch: str) -> bool
is_symbol(ch: str) -> bool
is_whitespace(ch: str) -> bool
is_uppercase(ch: str) -> bool
is_lowercase(ch: str) -> bool
is_alphanumeric(ch: str) -> bool
is_char_ascii(ch: str) -> bool
```

**Unicode Category Functions**

```python
get_unicode_categories(text: str) -> List[str]
get_unicode_category_groups(text: str) -> List[str]
count_unicode_categories(text: str) -> Dict[str, int]
count_unicode_category_groups(text: str) -> Dict[str, int]
get_unicode_category_ratios(text: str) -> Dict[str, float]
get_unicode_category_group_ratios(text: str) -> Dict[str, float]
```

**Unicode Bigram/Trigram Functions**

```python
get_unicode_category_bigrams(text: str) -> Dict[Tuple[str, str], int]
get_unicode_category_bigram_ratios(text: str) -> Dict[Tuple[str, str], float]
get_unicode_category_group_bigrams(text: str) -> Dict[Tuple[str, str], int]
get_unicode_category_group_bigram_ratios(text: str) -> Dict[Tuple[str, str], float]
get_unicode_category_trigrams(text: str) -> Dict[Tuple[str, str, str], int]
get_unicode_category_trigram_ratios(text: str) -> Dict[Tuple[str, str, str], float]
get_unicode_category_group_trigrams(text: str) -> Dict[Tuple[str, str, str], int]
get_unicode_category_group_trigram_ratios(text: str) -> Dict[Tuple[str, str, str], float]
```

**Frequency Analysis**

```python
get_char_frequency(text: str) -> Dict[str, int]
get_char_type_frequency(text: str) -> Dict[str, int]
get_unicode_category_frequency(text: str) -> Dict[str, int]
get_unicode_category_group_frequency(text: str) -> Dict[str, int]
```

**Statistical Measures**

```python
char_entropy(text: str) -> float
```

### Unigram Analysis

**Tokenization Functions**

```python
tokenize_unigrams(text: str) -> List[str]
tokenize_unigrams_with_punctuation(text: str) -> List[str]
```

**Token Counting Functions**

```python
count_unigram_tokens(text: str, include_punctuation: bool) -> int
count_unique_unigrams(text: str, include_punctuation: bool, case_sensitive: bool) -> int
```

**Lexical Diversity Metrics**

```python
unigram_type_token_ratio(text: str, include_punctuation: bool, case_sensitive: bool) -> float
unigram_repetition_rate(text: str, include_punctuation: bool, case_sensitive: bool) -> float
```

**Token Frequency Analysis**

```python
get_unigram_frequency(text: str, include_punctuation: bool, case_sensitive: bool) -> Dict[str, int]
max_unigram_frequency_ratio(text: str, include_punctuation: bool, case_sensitive: bool) -> float
```

**Statistical Measures**

```python
unigram_entropy(text: str, include_punctuation: bool, case_sensitive: bool) -> float
```

**Token Length Metrics**

```python
short_token_ratio(text: str, include_punctuation: bool, case_sensitive: bool) -> float
long_token_ratio(text: str, include_punctuation: bool, case_sensitive: bool) -> float
```

**Vocabulary Richness**

```python
hapax_legomena_ratio(text: str, include_punctuation: bool, case_sensitive: bool) -> float
top_5_token_coverage(text: str, include_punctuation: bool, case_sensitive: bool) -> float
```

**All-in-One Analysis**

```python
get_all_unigram_metrics(text: str, include_punctuation: bool, case_sensitive: bool) -> dict
```

### Text Segmentation

```python
count_words(text: str) -> int
count_lines(text: str) -> int
average_line_length(text: str) -> float
count_paragraphs(text: str) -> int
average_paragraph_length(text: str) -> float
average_word_length(text: str) -> float
average_sentence_length(text: str) -> float
split_words(text: str) -> List[str]
split_lines(text: str) -> List[str]
segment_lines(text: str) -> List[str]
split_paragraphs(text: str) -> List[str]
segment_paragraphs(text: str) -> List[str]
segment_sentences(text: str) -> List[str]
```

### Pattern Matching

```python
count_regex_matches(text: str, pattern: str) -> int
contains_regex_pattern(text: str, pattern: str) -> bool
count_copyright_mentions(text: str) -> int
count_rights_reserved(text: str) -> int
count_section_strings(text: str) -> int
count_question_strings(text: str) -> int
count_interrogative_questions(text: str) -> int
count_complex_interrogatives(text: str) -> int
count_factual_statements(text: str) -> int
count_logical_reasoning(text: str) -> int
contains_code_characters(text: str) -> bool
bullet_or_ellipsis_lines_ratio(text: str) -> float
contains_blacklist_substring(text: str, blacklist: List[str]) -> bool
get_all_pattern_metrics(text: str, use_paragraph_processing: bool = True, max_segment_size: int = 4096) -> dict
```

### Compression Metrics

```python
compression_ratio(text: str) -> float
get_compression_metrics(text: str) -> dict
unigram_compression_ratio(text: str, include_punctuation: bool) -> float
```

### Statistical Distribution Metrics

```python
zipf_fitness_score(text: str, include_punctuation: bool, case_sensitive: bool) -> float
power_law_exponent(text: str, include_punctuation: bool, case_sensitive: bool) -> float
calculate_burstiness(text: str, tokens: List[str]) -> float
analyze_vocab_growth(text: str, chunk_size: int) -> dict
get_zipf_metrics(text: str, include_punctuation: bool, case_sensitive: bool) -> dict
```

### ML Tokenization

```python
tokenize_ml(text: str, tokenizer_path: Optional[str] = None) -> List[int]
batch_tokenize_ml(texts: List[str], tokenizer_path: Optional[str] = None) -> List[List[int]]
subword_token_count(text: str, tokenizer_path: Optional[str] = None) -> int
unique_subword_count(text: str, tokenizer_path: Optional[str] = None) -> int
subword_type_token_ratio(text: str, tokenizer_path: Optional[str] = None) -> float
subword_repetition_rate(text: str, tokenizer_path: Optional[str] = None) -> float
subword_entropy(text: str, tokenizer_path: Optional[str] = None) -> float
subword_efficiency(text: str, tokenizer_path: Optional[str] = None) -> float
get_token_metrics(text: str, tokenizer_path: Optional[str] = None) -> dict
```

### Comprehensive Analysis

```python
get_all_metrics(
    text: str, 
    include_punctuation: bool = True, 
    case_sensitive: bool = False, 
    use_paragraph_processing: bool = True, 
    max_segment_size: int = 4096
) -> dict
```

## Classes

### HyperAnalyzer

Optimized analyzer for calculating multiple metrics in a single pass.

```python
class HyperAnalyzer:
    def __init__(self, include_punctuation: bool = False, case_sensitive: bool = True)
    def calculate_all_metrics(self, text: str) -> dict
    def calculate_batch_metrics(self, texts: List[str]) -> List[dict]
```

### BatchProcessor

Batch processor for efficient processing of large datasets.

```python
class BatchProcessor:
    def __init__(self)
    def process_batch(self, texts: List[str], metrics: List[str]) -> List[dict]
```

### Typed Metric Classes

```python
# From cheesecloth.tokenized_metrics
class CharMetrics:
    @classmethod
    def from_dict(cls, metrics: Dict[str, Any]) -> "CharMetrics"
    def to_dict(self) -> Dict[str, Any]
    
class UnigramMetrics:
    @classmethod
    def from_dict(cls, metrics: Dict[str, Any]) -> "UnigramMetrics"
    def to_dict(self) -> Dict[str, Any]
    
class PatternMetrics:
    @classmethod
    def from_dict(cls, metrics: Dict[str, Any]) -> "PatternMetrics"
    def to_dict(self) -> Dict[str, Any]
    
class SegmentationMetrics:
    @classmethod
    def from_dict(cls, metrics: Dict[str, Any]) -> "SegmentationMetrics"
    def to_dict(self) -> Dict[str, Any]
    
class AllMetrics:
    @classmethod
    def from_dict(cls, metrics: Dict[str, Dict[str, Any]]) -> "AllMetrics"
    def to_dict(self) -> Dict[str, Dict[str, Any]]
    def calculate_readability_score(self) -> float
    def get_readability_level(self) -> str
    def get_readability_assessment(self) -> Dict[str, Any]
    def summary(self) -> Dict[str, Any]
```

### Data Processing Utilities

```python
# From cheesecloth.data
class TextDataLoader:
    def __init__(self, source: str, text_field: str = "text", split: str = "train")
    def load(self, limit: Optional[int] = None, start: int = 0) -> List[Dict[str, Any]]
    
class TextBatchProcessor:
    def __init__(
        self,
        data_loader: TextDataLoader,
        batch_size: int = 32,
        include_char_metrics: bool = True,
        include_unigram_metrics: bool = True,
        include_punctuation: bool = False,
        case_sensitive: bool = False
    )
    def process(self) -> Iterator[List[Dict[str, Any]]]
    
class TokenizerWrapper:
    def __init__(self, tokenizer_name: str)
    def tokenize(self, text: str) -> List[int]
    def batch_tokenize(self, texts: List[str]) -> List[List[int]]
    def decode(self, tokens: List[int]) -> str
    
# Processing functions
def process_text_file(file_path: str, **kwargs) -> Dict[str, Any]
def process_jsonl_file(file_path: str, text_field: str = "text", **kwargs) -> Dict[str, Any]
def process_huggingface_dataset(dataset_name: str, split: str = "train", text_field: str = "text", **kwargs) -> Dict[str, Any]
```

### Tokenized Analysis

```python
# From cheesecloth.tokenized_metrics
class TokenizedAnalyzer:
    def __init__(self, include_punctuation: bool = False, case_sensitive: bool = True)
    def calculate_metrics(self, text: str, token_ids: Optional[List[int]] = None) -> Dict[str, Any]
    def calculate_batch_metrics(self, texts: List[str], token_ids: Optional[List[List[int]]] = None) -> List[Dict[str, Any]]
    
def calculate_token_metrics(tokens: List[int]) -> Dict[str, Any]
def process_tokenized_text(
    text: str,
    include_token_metrics: bool = True,
    include_unigram_metrics: bool = True,
    include_char_metrics: bool = True,
    include_punctuation: bool = False,
    case_sensitive: bool = True
) -> Dict[str, Any]
def process_tokenized_batch(
    texts: List[str],
    batch_size: int = 32,
    include_token_metrics: bool = True,
    include_unigram_metrics: bool = True,
    include_char_metrics: bool = True,
    include_punctuation: bool = False,
    case_sensitive: bool = True
) -> List[Dict[str, Any]]
def process_tokenized_data(
    texts: List[str],
    token_ids: List[List[int]],
    batch_size: int = 32,
    include_token_metrics: bool = True,
    include_unigram_metrics: bool = True,
    include_char_metrics: bool = True,
    include_punctuation: bool = False,
    case_sensitive: bool = True
) -> List[Dict[str, Any]]
```

## Return Types

Most functions return either primitive types (`int`, `float`, `bool`), collections (`List`, `Dict`), or dictionaries of metrics. Metric dictionaries typically contain:

### Character Metrics Dictionary

```python
{
    'char_count': int,
    'letter_count': int,
    'digit_count': int,
    'punctuation_count': int,
    'symbol_count': int,
    'whitespace_count': int,
    'non_ascii_count': int,
    'uppercase_count': int,
    'lowercase_count': int,
    'alphanumeric_count': int,
    'char_type_transitions': int,
    'consecutive_runs': int,
    'punctuation_diversity': int,
    'ratio_letters': float,
    'ratio_digits': float,
    'ratio_punctuation': float,
    'ratio_symbols': float,
    'ratio_whitespace': float,
    'ratio_non_ascii': float,
    'ratio_uppercase': float,
    'ratio_lowercase': float,
    'ratio_alphanumeric': float,
    'ratio_alpha_to_numeric': float,
    'char_entropy': float,
    'case_ratio': float,
    'category_entropy': float,
    'ascii_ratio': float,
    'unicode_category_ratios': dict,
    'unicode_category_group_ratios': dict,
    'char_frequency': dict,
    'unicode_category_bigram_ratios': dict,
    'unicode_category_group_bigram_ratios': dict,
    'unicode_category_trigram_ratios': dict,
    'unicode_category_group_trigram_ratios': dict
}
```

### Unigram Metrics Dictionary

```python
{
    'token_count': int,
    'unique_token_count': int,
    'type_token_ratio': float,
    'repetition_rate': float,
    'token_entropy': float,
    'max_frequency_ratio': float,
    'average_token_length': float,
    'hapax_legomena_ratio': float,
    'top_5_token_coverage': float,
    'short_token_ratio': float,
    'long_token_ratio': float
}
```

### All Metrics Dictionary

```python
{
    'character': dict,  # Character metrics dictionary
    'unigram': dict,    # Unigram metrics dictionary
    'patterns': dict,   # Pattern metrics dictionary
    'segmentation': dict  # Segmentation metrics dictionary
}
```