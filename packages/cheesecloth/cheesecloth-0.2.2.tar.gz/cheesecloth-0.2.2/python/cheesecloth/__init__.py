"""
Cheesecloth: High-Performance Text Analysis Library
==================================================

Cheesecloth is a comprehensive text analysis library that combines high-performance
Rust implementations with Python bindings to provide fast and thorough text metrics
for data science, natural language processing, and corpus analysis.

Core Components
--------------

1. Character-level Analysis
   - Character counts, ratios, and distributions
   - Unicode category classification and analysis
   - ASCII/non-ASCII metrics

2. Word-level Analysis (Unigrams)
   - Linguistic word tokenization based on Unicode boundaries
   - Type-token ratio, repetition rates, and entropy
   - Word frequency analysis

3. ML Tokenizer Analysis
   - Support for Hugging Face tokenizers
   - Subword token metrics for machine learning applications
   - Tokenization efficiency metrics

4. Text Structure Analysis
   - Line, paragraph, and sentence segmentation
   - Document structure metrics

5. Information Theory and Statistics
   - Compression-based analysis
   - Zipf's law and power law distributions
   - Burstiness and vocabulary growth metrics

6. Data Processing Utilities
   - Batch processing for large datasets
   - Support for various input formats (text, JSONL, Hugging Face datasets)
   - Efficient parallel processing

High-Performance Architecture
----------------------------

Cheesecloth is built with a dual-approach architecture:

1. BatchProcessor: For selective computation of specific metrics
2. HyperAnalyzer: For high-performance computation of all metrics in a single pass

Both approaches provide batch processing capabilities for efficient analysis of
large text corpora, with optimized implementations in Rust.

Example Usage
-----------

Basic character metrics:
```python
import cheesecloth
text = "Hello, world!"
print(cheesecloth.count_chars(text))  # 13
print(cheesecloth.is_ascii(text))     # True
```

HyperAnalyzer for comprehensive metrics:
```python
analyzer = cheesecloth.HyperAnalyzer(include_punctuation=True, case_sensitive=True)
metrics = analyzer.calculate_all_metrics("Hello, world!")
print(metrics["char_count"])        # 13
print(metrics["unigram_count"])     # 3
```

Processing a batch of texts:
```python
texts = ["First example.", "Second example with more words.", "Third!"]
results = analyzer.calculate_batch_metrics(texts)
for i, metrics in enumerate(results):
    print(f"Text {i+1} has {metrics['char_count']} characters")
```
"""

# Import all Rust binding functions
# We're keeping the star import to maintain compatibility with all the tests
# This resolves F403/F405 errors but at the cost of maintaining backward compatibility
# pylint: disable=wildcard-import, unused-wildcard-import
# flake8: noqa: F403
from .cheesecloth import *  

# Store original __doc__ and __all__ for use later
import sys
_cheesecloth_doc = sys.modules['.'.join(__name__.split('.') + ['cheesecloth'])].__doc__
_cheesecloth_all = getattr(sys.modules['.'.join(__name__.split('.') + ['cheesecloth'])], '__all__', [])

# Import data loading and processing utilities
from .data import (
    TextDataLoader,
    TextBatchProcessor,
    TokenizerWrapper,
    process_text_file,
    process_jsonl_file,
    process_huggingface_dataset,
)

# Import tokenized metrics utilities
from .tokenized_metrics import (
    TokenizedAnalyzer,
    CharMetrics,
    UnigramMetrics,
    PatternMetrics,
    SegmentationMetrics,
    AllMetrics,
    calculate_token_metrics,
    process_tokenized_text,
    process_tokenized_batch,
    process_tokenized_data,
)


# Direct implementations of the new unigram metrics
def hapax_legomena_ratio(
    text: str, include_punctuation: bool, case_sensitive: bool
) -> float:
    """
    Calculate the ratio of words that appear exactly once (hapax legomena) to total words.

    Args:
        text: The input text to analyze
        include_punctuation: Whether to include punctuation in the token count
        case_sensitive: Whether to treat uppercase and lowercase as different tokens

    Returns:
        Hapax legomena ratio (0.0 to 1.0)
    """
    # Get the frequency distribution
    freq = get_unigram_frequency(text, include_punctuation, case_sensitive)

    # Count tokens that appear exactly once
    hapax_count = sum(1 for count in freq.values() if count == 1)

    # Get total token count
    total_tokens = count_unigram_tokens(text, include_punctuation)

    # Return ratio (or 0.0 for empty text)
    return hapax_count / total_tokens if total_tokens > 0 else 0.0


def top_5_token_coverage(
    text: str, include_punctuation: bool, case_sensitive: bool
) -> float:
    """
    Calculate the percentage of text covered by the 5 most frequent tokens.

    Args:
        text: The input text to analyze
        include_punctuation: Whether to include punctuation in the token count
        case_sensitive: Whether to treat uppercase and lowercase as different tokens

    Returns:
        Top-5 token coverage (0.0 to 1.0)
    """
    # Get the frequency distribution
    freq = get_unigram_frequency(text, include_punctuation, case_sensitive)

    if not freq:
        return 0.0

    # Sort by frequency and take top 5
    sorted_counts = sorted(freq.values(), reverse=True)
    top_5_sum = sum(sorted_counts[:5])

    # Get total token count
    total_tokens = count_unigram_tokens(text, include_punctuation)

    # Return ratio
    return top_5_sum / total_tokens if total_tokens > 0 else 0.0


def short_token_ratio(
    text: str, include_punctuation: bool, case_sensitive: bool
) -> float:
    """
    Calculate the ratio of tokens with length ≤ 3 characters.

    Args:
        text: The input text to analyze
        include_punctuation: Whether to include punctuation in the token count
        case_sensitive: Whether to treat uppercase and lowercase as different tokens

    Returns:
        Short token ratio (0.0 to 1.0)
    """
    # Get the tokens
    tokens = (
        tokenize_unigrams_with_punctuation(text)
        if include_punctuation
        else tokenize_unigrams(text)
    )

    if not tokens:
        return 0.0

    # Count short tokens (≤ 3 characters)
    short_count = sum(1 for token in tokens if len(token) <= 3)

    # Return ratio
    return short_count / len(tokens)


def long_token_ratio(
    text: str, include_punctuation: bool, case_sensitive: bool
) -> float:
    """
    Calculate the ratio of tokens with length ≥ 7 characters.

    Args:
        text: The input text to analyze
        include_punctuation: Whether to include punctuation in the token count
        case_sensitive: Whether to treat uppercase and lowercase as different tokens

    Returns:
        Long token ratio (0.0 to 1.0)
    """
    # Get the tokens
    tokens = (
        tokenize_unigrams_with_punctuation(text)
        if include_punctuation
        else tokenize_unigrams(text)
    )

    if not tokens:
        return 0.0

    # Count long tokens (≥ 7 characters)
    long_count = sum(1 for token in tokens if len(token) >= 7)

    # Return ratio
    return long_count / len(tokens)


# Monkey patch get_all_unigram_metrics to include the new metrics
original_get_all_unigram_metrics = get_all_unigram_metrics


def enhanced_get_all_unigram_metrics(
    text: str, include_punctuation: bool, case_sensitive: bool
) -> dict:
    """Enhanced version of get_all_unigram_metrics that includes additional metrics."""
    # Get the original metrics
    metrics = original_get_all_unigram_metrics(
        text, include_punctuation, case_sensitive
    )

    # Add the new metrics
    metrics["hapax_legomena_ratio"] = hapax_legomena_ratio(
        text, include_punctuation, case_sensitive
    )
    metrics["top_5_token_coverage"] = top_5_token_coverage(
        text, include_punctuation, case_sensitive
    )
    metrics["short_token_ratio"] = short_token_ratio(
        text, include_punctuation, case_sensitive
    )
    metrics["long_token_ratio"] = long_token_ratio(
        text, include_punctuation, case_sensitive
    )

    return metrics


# Replace the original function with our enhanced version
get_all_unigram_metrics = enhanced_get_all_unigram_metrics


# Add version number
__version__ = "0.2.2"

# Ensure docstring is properly set
__doc__ = __doc__ or _cheesecloth_doc

# Update __all__ to include Python module additions
if _cheesecloth_all:
    __all__ = _cheesecloth_all + [
        # Data processing
        "TextDataLoader",
        "TextBatchProcessor",
        "TokenizerWrapper",
        "process_text_file",
        "process_jsonl_file",
        "process_huggingface_dataset",
        # Tokenized metrics
        "TokenizedAnalyzer",
        "CharMetrics",
        "UnigramMetrics",
        "PatternMetrics",
        "SegmentationMetrics",
        "AllMetrics",
        "calculate_token_metrics",
        "process_tokenized_text",
        "process_tokenized_batch",
        "process_tokenized_data",
        # New unigram metrics
        "hapax_legomena_ratio",
        "top_5_token_coverage",
        "short_token_ratio",
        "long_token_ratio",
    ]
