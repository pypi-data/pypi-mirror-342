#!/usr/bin/env python3
"""
Tokenized Data Processing and Analysis
=====================================

This module provides specialized functionality for analyzing pre-tokenized text data,
particularly focusing on the token sequences produced by machine learning tokenizers
like BPE (Byte-Pair Encoding), WordPiece, and SentencePiece.

Key Components
-------------

1. TokenizedAnalyzer
   - Unified analyzer for pre-tokenized text
   - Combines HyperAnalyzer functionality with token-specific metrics
   - Handles both raw text and token IDs together
   - Provides consistent naming and organization of metrics

2. Token-specific Metrics
   - Token count and unique token statistics
   - Type-token ratio for tokenized data
   - Repetition rate and entropy measures
   - Direct calculation from token IDs without requiring decoded text

3. Processing Functions
   - calculate_token_metrics: Core metrics from token IDs
   - process_tokenized_text: Process individual texts
   - process_tokenized_batch: Efficient batch processing
   - process_tokenized_data: Combined processing of text and tokens

4. Typed Metrics Classes
   - CharMetrics: Type-safe wrapper for character metrics
   - UnigramMetrics: Type-safe wrapper for unigram metrics
   - AllMetrics: Complete metrics container
   - Provide attribute access, proper typing, and helper methods

Use Cases
--------

This module is particularly valuable for:

1. Analyzing how machine learning models "see" text through their tokenization
2. Comparing linguistic (unigram) metrics with ML tokenization metrics
3. Working with pre-tokenized datasets like those used in large language models
4. Studying tokenization efficiency and behavior across different text types
5. Processing data that comes already tokenized from ML pipelines

The metrics provided help bridge the gap between traditional linguistic analysis
and machine learning approaches to text processing.
"""

import math
from collections import Counter
from dataclasses import asdict, dataclass, field
from typing import List, Dict, Any, Optional, Tuple

import cheesecloth


def calculate_token_metrics(tokens: List[int]) -> Dict[str, Any]:
    """
    Calculate metrics directly from token IDs.

    Args:
        tokens: List of token IDs

    Returns:
        Dictionary of token metrics with consistent naming
    """
    if not tokens:
        return {
            "token_count": 0,
            "unique_token_count": 0,
            "token_type_token_ratio": 0.0,
            "token_repetition_rate": 0.0,
            "token_entropy": 0.0,
        }

    # Count tokens
    token_count = len(tokens)

    # Count unique tokens
    unique_tokens = set(tokens)
    unique_token_count = len(unique_tokens)

    # Calculate type-token ratio
    type_token_ratio = unique_token_count / token_count if token_count > 0 else 0.0

    # Calculate repetition rate
    repetition_rate = 1.0 - type_token_ratio

    # Calculate token entropy
    token_freq = Counter(tokens)
    entropy = 0.0
    for count in token_freq.values():
        probability = count / token_count
        entropy -= probability * math.log2(probability)

    return {
        "token_count": token_count,
        "unique_token_count": unique_token_count,
        "token_type_token_ratio": type_token_ratio,
        "token_repetition_rate": repetition_rate,
        "token_entropy": entropy,
    }


def process_tokenized_text(
    text: str,
    include_token_metrics: bool = True,
    include_unigram_metrics: bool = True,
    include_char_metrics: bool = True,
    include_punctuation: bool = False,
    case_sensitive: bool = True,
) -> Dict[str, Any]:
    """
    Process text with multiple metric types.

    Args:
        text: The text to analyze
        include_token_metrics: Whether to include BPE token metrics
        include_unigram_metrics: Whether to include unigram metrics
        include_char_metrics: Whether to include character metrics
        include_punctuation: Whether to include punctuation in unigram analysis
        case_sensitive: Whether to perform case-sensitive analysis

    Returns:
        Dictionary of metrics with consistent naming
    """
    result = {}

    # Use HyperAnalyzer for character and unigram metrics
    if include_char_metrics or include_unigram_metrics:
        analyzer = cheesecloth.HyperAnalyzer(include_punctuation, case_sensitive)
        metrics = analyzer.calculate_all_metrics(text)

        # Filter metrics based on flags
        for key, value in metrics.items():
            if key.startswith("unigram_") and include_unigram_metrics:
                result[key] = value
            elif (
                not key.startswith("unigram_")
                and not key.startswith("token_")
                and include_char_metrics
            ):
                result[key] = value

    # For token metrics, we would need actual token IDs
    # This is handled separately with calculate_token_metrics

    return result


def process_tokenized_batch(
    texts: List[str],
    batch_size: int = 32,
    include_token_metrics: bool = True,
    include_unigram_metrics: bool = True,
    include_char_metrics: bool = True,
    include_punctuation: bool = False,
    case_sensitive: bool = True,
) -> List[Dict[str, Any]]:
    """
    Process a batch of texts with multiple metric types.

    Args:
        texts: List of texts to analyze
        batch_size: Batch size for processing
        include_token_metrics: Whether to include BPE token metrics
        include_unigram_metrics: Whether to include unigram metrics
        include_char_metrics: Whether to include character metrics
        include_punctuation: Whether to include punctuation in unigram analysis
        case_sensitive: Whether to perform case-sensitive analysis

    Returns:
        List of dictionaries with metrics for each text
    """
    results = []

    # Process in batches
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]

        # Use HyperAnalyzer for character and unigram metrics
        if include_char_metrics or include_unigram_metrics:
            analyzer = cheesecloth.HyperAnalyzer(include_punctuation, case_sensitive)
            batch_metrics = analyzer.calculate_batch_metrics(batch)

            for j, metrics in enumerate(batch_metrics):
                # Create result dict if needed
                if i + j >= len(results):
                    results.append({})

                # Filter metrics based on flags
                for key, value in metrics.items():
                    if key.startswith("unigram_") and include_unigram_metrics:
                        results[i + j][key] = value
                    elif (
                        not key.startswith("unigram_")
                        and not key.startswith("token_")
                        and include_char_metrics
                    ):
                        results[i + j][key] = value

    return results


def process_tokenized_data(
    texts: List[str],
    token_ids: List[List[int]],
    batch_size: int = 32,
    include_token_metrics: bool = True,
    include_unigram_metrics: bool = True,
    include_char_metrics: bool = True,
    include_punctuation: bool = False,
    case_sensitive: bool = True,
) -> List[Dict[str, Any]]:
    """
    Process texts and corresponding token IDs together.

    Args:
        texts: List of text strings
        token_ids: List of token ID lists corresponding to each text
        batch_size: Batch size for processing
        include_token_metrics: Whether to include BPE token metrics
        include_unigram_metrics: Whether to include unigram metrics
        include_char_metrics: Whether to include character metrics
        include_punctuation: Whether to include punctuation in unigram analysis
        case_sensitive: Whether to perform case-sensitive analysis

    Returns:
        List of dictionaries with metrics for each text
    """
    # Validate inputs
    if len(texts) != len(token_ids):
        raise ValueError(
            f"Length mismatch: {len(texts)} texts vs {len(token_ids)} token lists"
        )

    # Get text metrics
    results = process_tokenized_batch(
        texts,
        batch_size,
        include_token_metrics=False,  # We'll add token metrics separately
        include_unigram_metrics=include_unigram_metrics,
        include_char_metrics=include_char_metrics,
        include_punctuation=include_punctuation,
        case_sensitive=case_sensitive,
    )

    # Add token metrics
    if include_token_metrics:
        for i, tokens in enumerate(token_ids):
            token_metrics = calculate_token_metrics(tokens)
            results[i].update(token_metrics)

    return results


class TokenizedAnalyzer:
    """
    Analyzer for pre-tokenized data.

    This class provides a unified interface for calculating metrics on
    pre-tokenized data, such as text with corresponding BPE token IDs.
    """

    def __init__(self, include_punctuation: bool = False, case_sensitive: bool = True):
        """
        Initialize the analyzer.

        Args:
            include_punctuation: Whether to include punctuation in unigram analysis
            case_sensitive: Whether to perform case-sensitive analysis
        """
        self.include_punctuation = include_punctuation
        self.case_sensitive = case_sensitive

        # Create a HyperAnalyzer for text metrics
        self.hyper_analyzer = cheesecloth.HyperAnalyzer(
            include_punctuation, case_sensitive
        )

    def calculate_metrics(
        self, text: str, token_ids: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Calculate metrics for a single text.

        Args:
            text: The text to analyze
            token_ids: Optional token IDs for the text

        Returns:
            Dictionary of metrics
        """
        # Calculate text metrics
        result = self.hyper_analyzer.calculate_all_metrics(text)

        # Add token metrics if provided
        if token_ids is not None:
            token_metrics = calculate_token_metrics(token_ids)
            result.update(token_metrics)

        # Add advanced metrics - compression ratio and Zipf metrics
        try:
            # Add compression metrics
            compression_metrics = cheesecloth.get_compression_metrics(text)
            result.update(compression_metrics)

            # Add Zipf/power law metrics
            zipf_metrics = cheesecloth.get_zipf_metrics(
                text,
                include_punctuation=self.include_punctuation,
                case_sensitive=self.case_sensitive,
            )
            result.update(zipf_metrics)
        except Exception as e:
            # If advanced metrics fail for any reason, log it but continue
            print(f"Warning: Failed to calculate advanced metrics: {e}")

        return result

    def calculate_batch_metrics(
        self, texts: List[str], token_ids: Optional[List[List[int]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Calculate metrics for a batch of texts.

        Args:
            texts: List of texts to analyze
            token_ids: Optional list of token ID lists for each text

        Returns:
            List of dictionaries with metrics for each text
        """
        # Calculate text metrics
        results = list(self.hyper_analyzer.calculate_batch_metrics(texts))

        # Add token metrics if provided
        if token_ids is not None:
            if len(texts) != len(token_ids):
                raise ValueError(
                    f"Length mismatch: {len(texts)} texts vs {len(token_ids)} token lists"
                )

            for i, tokens in enumerate(token_ids):
                token_metrics = calculate_token_metrics(tokens)
                results[i].update(token_metrics)

        # Add advanced metrics for each text
        for i, text in enumerate(texts):
            try:
                # Add compression metrics
                compression_metrics = cheesecloth.get_compression_metrics(text)
                results[i].update(compression_metrics)

                # Add Zipf/power law metrics
                zipf_metrics = cheesecloth.get_zipf_metrics(
                    text,
                    include_punctuation=self.include_punctuation,
                    case_sensitive=self.case_sensitive,
                )
                results[i].update(zipf_metrics)
            except Exception:
                # If advanced metrics fail for any reason, continue
                pass

        return results


# Typed wrappers for cheesecloth metrics
@dataclass
class CharMetrics:
    """
    Type-safe wrapper for character metrics returned by get_all_char_metrics().

    This class provides attribute access to all character metrics with proper typing,
    convenience methods, and category-specific properties.

    Attributes:
        char_count: Total number of characters
        letter_count: Number of letter characters
        digit_count: Number of digit characters
        punctuation_count: Number of punctuation characters
        symbol_count: Number of symbol characters
        whitespace_count: Number of whitespace characters
        non_ascii_count: Number of non-ASCII characters
        uppercase_count: Number of uppercase characters
        lowercase_count: Number of lowercase characters
        alphanumeric_count: Number of alphanumeric characters
        char_type_transitions: Number of transitions between different character types
        consecutive_runs: Number of runs of consecutive same character types
        punctuation_diversity: Number of distinct punctuation characters

        ascii_ratio: Ratio of ASCII characters to total characters
        ratio_letters: Ratio of letters to total characters
        ratio_digits: Ratio of digits to total characters
        ratio_punctuation: Ratio of punctuation to total characters
        ratio_symbols: Ratio of symbols to total characters
        ratio_whitespace: Ratio of whitespace to total characters
        ratio_non_ascii: Ratio of non-ASCII to total characters
        ratio_uppercase: Ratio of uppercase to all letters
        ratio_lowercase: Ratio of lowercase to all letters
        ratio_alphanumeric: Ratio of alphanumeric to total characters
        ratio_alpha_to_numeric: Ratio of letters to digits
        case_ratio: Ratio of uppercase to lowercase letters

        char_entropy: Character-level Shannon entropy
        category_entropy: Entropy of the Unicode category distribution

        unicode_category_ratios: Distribution of Unicode categories
        unicode_category_group_ratios: Distribution of Unicode category groups
        char_frequency: Frequency of each character
        unicode_category_bigram_ratios: Distribution of Unicode category pairs
        unicode_category_group_bigram_ratios: Distribution of Unicode category group pairs
        unicode_category_trigram_ratios: Distribution of Unicode category trigrams
        unicode_category_group_trigram_ratios: Distribution of Unicode category group trigrams
    """

    # Character counts
    char_count: int
    letter_count: int
    digit_count: int
    punctuation_count: int
    symbol_count: int
    whitespace_count: int
    non_ascii_count: int
    uppercase_count: int
    lowercase_count: int
    alphanumeric_count: int

    # Ratio metrics
    ascii_ratio: float
    ratio_letters: float
    ratio_digits: float
    ratio_punctuation: float
    ratio_symbols: float
    ratio_whitespace: float
    ratio_non_ascii: float
    ratio_uppercase: float
    ratio_lowercase: float
    ratio_alphanumeric: float
    ratio_alpha_to_numeric: float

    # Entropy metrics
    char_entropy: float

    # Unicode category metrics (required fields with no defaults)
    unicode_category_ratios: Dict[str, float]
    unicode_category_group_ratios: Dict[str, float]
    char_frequency: Dict[str, int]
    unicode_category_bigram_ratios: Dict[Tuple[str, str], float]
    unicode_category_group_bigram_ratios: Dict[Tuple[str, str], float]

    # All fields with default values must come after all required fields

    # New count metrics with defaults
    char_type_transitions: int = 0
    consecutive_runs: int = 0
    punctuation_diversity: int = 0

    # New ratio metrics with defaults
    case_ratio: float = 0.0
    category_entropy: float = 0.0

    # Unicode trigram metrics with defaults
    unicode_category_trigram_ratios: Dict[Tuple[str, str, str], float] = field(
        default_factory=dict
    )
    unicode_category_group_trigram_ratios: Dict[Tuple[str, str, str], float] = field(
        default_factory=dict
    )

    @classmethod
    def from_dict(cls, metrics: Dict[str, Any]) -> "CharMetrics":
        """
        Create a CharMetrics instance from the dictionary returned by get_all_char_metrics().

        Args:
            metrics: Dictionary of metrics from get_all_char_metrics()

        Returns:
            CharMetrics instance with attribute access to all metrics
        """
        # Initialize with all fields from the metrics dictionary
        # Filter out any excess keys not in our dataclass
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_metrics = {k: v for k, v in metrics.items() if k in valid_fields}

        # No need to manually initialize fields with defaults anymore
        # Field defaults and default_factory will be used automatically

        return cls(**filtered_metrics)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the CharMetrics instance back to a dictionary.

        Returns:
            Dictionary representation of all metrics
        """
        return asdict(self)

    # Convenience properties for common analysis tasks
    @property
    def is_mostly_ascii(self) -> bool:
        """Check if the text is predominantly ASCII (>90%)."""
        return self.ascii_ratio > 0.9

    @property
    def has_high_entropy(self) -> bool:
        """Check if the text has high character entropy (>4.0)."""
        return self.char_entropy > 4.0

    @property
    def is_mostly_alphabetic(self) -> bool:
        """Check if the text is predominantly alphabetic (>70%)."""
        return self.ratio_letters > 0.7

    @property
    def has_high_punctuation(self) -> bool:
        """Check if the text has high punctuation (>15%)."""
        return self.ratio_punctuation > 0.15

    @property
    def is_mostly_uppercase(self) -> bool:
        """Check if the text is predominantly uppercase (>70%)."""
        return self.ratio_uppercase > 0.7

    @property
    def has_diverse_punctuation(self) -> bool:
        """Check if the text uses diverse punctuation (>3 unique punctuation marks)."""
        return self.punctuation_diversity > 3

    @property
    def has_complex_character_structure(self) -> bool:
        """Check if the text has complex character structure (many type transitions)."""
        return self.char_type_transitions > 0.15 * self.char_count

    @property
    def has_high_case_variation(self) -> bool:
        """Check if the text has high variation between uppercase and lowercase."""
        # Case ratio around 1.0 means balanced uppercase and lowercase
        return 0.4 < self.case_ratio < 2.5 and self.uppercase_count > 3

    @property
    def has_high_category_entropy(self) -> bool:
        """Check if the text has high Unicode category entropy (>1.5)."""
        return self.category_entropy > 1.5


@dataclass
class UnigramMetrics:
    """
    Type-safe wrapper for unigram metrics returned by get_all_unigram_metrics().

    This class provides attribute access to all unigram metrics with proper typing
    and convenience methods.

    Attributes:
        token_count: Total number of tokens
        unique_token_count: Number of unique tokens
        type_token_ratio: Ratio of unique tokens to total tokens
        repetition_rate: 1 - type_token_ratio
        token_entropy: Shannon entropy of token distribution
        max_frequency_ratio: Ratio of most frequent token count to total tokens
        average_token_length: Average length of tokens in characters
        hapax_legomena_ratio: Ratio of words appearing exactly once to total words
        top_5_token_coverage: Percentage of text covered by 5 most frequent tokens
        short_token_ratio: Ratio of tokens with length ≤ 3 characters
        long_token_ratio: Ratio of tokens with length ≥ 7 characters
    """

    token_count: int
    unique_token_count: int
    type_token_ratio: float
    repetition_rate: float
    token_entropy: float
    max_frequency_ratio: float
    average_token_length: float
    hapax_legomena_ratio: float
    top_5_token_coverage: float
    short_token_ratio: float
    long_token_ratio: float

    @classmethod
    def from_dict(cls, metrics: Dict[str, Any]) -> "UnigramMetrics":
        """
        Create a UnigramMetrics instance from the dictionary returned by get_all_unigram_metrics().

        Args:
            metrics: Dictionary of metrics from get_all_unigram_metrics()

        Returns:
            UnigramMetrics instance with attribute access to all metrics
        """
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_metrics = {k: v for k, v in metrics.items() if k in valid_fields}
        return cls(**filtered_metrics)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the UnigramMetrics instance back to a dictionary.

        Returns:
            Dictionary representation of all metrics
        """
        return asdict(self)

    # Convenience properties for common analysis tasks
    @property
    def lexical_diversity(self) -> str:
        """Return a qualitative assessment of lexical diversity."""
        if self.type_token_ratio < 0.4:
            return "Low"
        elif self.type_token_ratio < 0.7:
            return "Medium"
        else:
            return "High"

    @property
    def has_high_uniqueness(self) -> bool:
        """Check if the text has a high proportion of unique words (high hapax legomena ratio)."""
        return self.hapax_legomena_ratio > 0.6

    @property
    def has_common_word_dominance(self) -> bool:
        """Check if the text is dominated by common words (high top 5 coverage)."""
        return self.top_5_token_coverage > 0.5

    @property
    def has_complex_vocabulary(self) -> bool:
        """Check if the text has complex vocabulary (many long words)."""
        return self.long_token_ratio > 0.3

    @property
    def has_simple_vocabulary(self) -> bool:
        """Check if the text has simple vocabulary (many short words)."""
        return self.short_token_ratio > 0.6


@dataclass
class PatternMetrics:
    """
    Type-safe wrapper for pattern metrics returned by get_all_pattern_metrics().

    This class provides attribute access to all pattern metrics with proper typing
    and convenience methods.

    Attributes:
        question_count: Number of question patterns
        interrogative_question_count: Number of interrogative questions
        complex_interrogative_count: Number of complex interrogative patterns
        factual_statement_count: Number of factual statements
        logical_reasoning_count: Number of logical reasoning patterns
        section_heading_count: Number of section headings
        copyright_mention_count: Number of copyright mentions
        rights_reserved_count: Number of rights reserved mentions
        bullet_count: Number of bullet points
        ellipsis_count: Number of ellipses
        bullet_ellipsis_ratio: Ratio of bullet or ellipsis lines to total lines
        contains_code: Whether the text contains code-like patterns
    """

    # Question patterns
    question_count: int
    interrogative_question_count: int
    complex_interrogative_count: int

    # Content types
    factual_statement_count: int
    logical_reasoning_count: int
    section_heading_count: int
    copyright_mention_count: int
    rights_reserved_count: int

    # Format patterns
    bullet_count: int
    ellipsis_count: int
    bullet_ellipsis_ratio: float
    contains_code: bool

    # Optional processing metadata
    _used_paragraph_processing: bool = field(default=True)
    _paragraph_count: Optional[int] = None
    _segments_processed: Optional[int] = None
    _large_paragraphs_broken_down: Optional[int] = None
    _extremely_long_lines_chunked: Optional[int] = None
    _max_segment_size: Optional[int] = None

    @classmethod
    def from_dict(cls, metrics: Dict[str, Any]) -> "PatternMetrics":
        """
        Create a PatternMetrics instance from the dictionary returned by get_all_pattern_metrics().

        Args:
            metrics: Dictionary of metrics from get_all_pattern_metrics()

        Returns:
            PatternMetrics instance with attribute access to all metrics
        """
        # Required fields
        required_fields = {
            "question_count",
            "interrogative_question_count",
            "complex_interrogative_count",
            "factual_statement_count",
            "logical_reasoning_count",
            "section_heading_count",
            "copyright_mention_count",
            "rights_reserved_count",
            "bullet_count",
            "ellipsis_count",
            "bullet_ellipsis_ratio",
            "contains_code",
        }

        # Ensure required fields are present
        init_dict = {}
        for field_name in required_fields:
            if field_name in metrics:
                init_dict[field_name] = metrics[field_name]
            else:
                # Default to 0 or False for missing required fields
                if field_name == "contains_code":
                    init_dict[field_name] = False
                else:
                    init_dict[field_name] = 0

        # Add optional metadata if present
        for opt_field in [
            "_used_paragraph_processing",
            "_paragraph_count",
            "_segments_processed",
            "_large_paragraphs_broken_down",
            "_extremely_long_lines_chunked",
            "_max_segment_size",
        ]:
            if opt_field in metrics:
                init_dict[opt_field] = metrics[opt_field]

        return cls(**init_dict)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the PatternMetrics instance back to a dictionary.

        Returns:
            Dictionary representation of all metrics
        """
        # Filter out None values
        result = {}
        for k, v in asdict(self).items():
            if v is not None:
                result[k] = v
        return result

    # Convenience properties for common analysis tasks
    @property
    def is_educational(self) -> bool:
        """Check if the text has educational content characteristics."""
        return (
            self.factual_statement_count > 2
            or self.question_count > 3
            or self.section_heading_count > 1
        )

    @property
    def is_interactive(self) -> bool:
        """Check if the text has interactive content with many questions."""
        return self.question_count > 5

    @property
    def has_copyright_notices(self) -> bool:
        """Check if the text contains copyright notices."""
        return self.copyright_mention_count > 0 or self.rights_reserved_count > 0


@dataclass
class SegmentationMetrics:
    """
    Type-safe wrapper for segmentation metrics.

    This class provides attribute access to all segmentation metrics with proper typing
    and convenience methods.

    Attributes:
        line_count: Number of lines
        average_line_length: Average length of lines in characters
        paragraph_count: Number of paragraphs
        average_paragraph_length: Average length of paragraphs in characters
        average_sentence_length: Average length of sentences in words
    """

    line_count: int
    average_line_length: float
    paragraph_count: int
    average_paragraph_length: float
    average_sentence_length: float

    @classmethod
    def from_dict(cls, metrics: Dict[str, Any]) -> "SegmentationMetrics":
        """
        Create a SegmentationMetrics instance from a metrics dictionary.

        Args:
            metrics: Dictionary containing segmentation metrics

        Returns:
            SegmentationMetrics instance with attribute access to all metrics
        """
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_metrics = {k: v for k, v in metrics.items() if k in valid_fields}
        return cls(**filtered_metrics)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the SegmentationMetrics instance back to a dictionary.

        Returns:
            Dictionary representation of all metrics
        """
        return asdict(self)

    # Convenience properties for common analysis tasks
    @property
    def simple_readability_assessment(self) -> str:
        """
        Return a basic qualitative assessment of readability based only on sentence length.

        This is a simplified assessment that only looks at average sentence length.
        For a more comprehensive assessment, use AllMetrics.get_readability_level().

        Returns:
            A string representing a simple readability assessment
        """
        if self.average_sentence_length > 30:
            return "Complex"
        elif self.average_sentence_length > 20:
            return "Challenging"
        elif self.average_sentence_length > 12:
            return "Moderate"
        else:
            return "Simple"

    @property
    def readability_assessment(self) -> str:
        """
        Return a qualitative assessment of readability based on sentence length.

        Note: This property is kept for backward compatibility. For more accurate
        assessment, use AllMetrics.get_readability_level() which considers
        multiple factors.

        Returns:
            A string representing a simple readability assessment
        """
        return self.simple_readability_assessment

    @property
    def has_long_paragraphs(self) -> bool:
        """Check if the text has long paragraphs (>500 characters)."""
        return self.average_paragraph_length > 500

    @property
    def has_complex_structure(self) -> bool:
        """
        Check if the text has a complex structure based on sentence and paragraph length.

        Returns:
            True if the text has both long sentences and long paragraphs
        """
        return self.average_sentence_length > 20 and self.average_paragraph_length > 300


@dataclass
class AllMetrics:
    """
    Comprehensive wrapper for all metrics returned by get_all_metrics().

    This class provides structured access to all metrics categories with proper typing
    and convenience methods.

    Attributes:
        character: Character-level metrics
        unigram: Unigram-level metrics
        patterns: Pattern-based metrics
        segmentation: Text segmentation metrics
    """

    character: CharMetrics
    unigram: UnigramMetrics
    patterns: PatternMetrics
    segmentation: SegmentationMetrics

    @classmethod
    def from_dict(cls, metrics: Dict[str, Dict[str, Any]]) -> "AllMetrics":
        """
        Create an AllMetrics instance from the dictionary returned by get_all_metrics().

        Args:
            metrics: Dictionary of metrics from get_all_metrics()

        Returns:
            AllMetrics instance with structured access to all metrics categories
        """
        return cls(
            character=CharMetrics.from_dict(metrics["character"]),
            unigram=UnigramMetrics.from_dict(metrics["unigram"]),
            patterns=PatternMetrics.from_dict(metrics["patterns"]),
            segmentation=SegmentationMetrics.from_dict(metrics["segmentation"]),
        )

    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        """
        Convert the AllMetrics instance back to a dictionary.

        Returns:
            Nested dictionary representation of all metrics categories
        """
        return {
            "character": self.character.to_dict(),
            "unigram": self.unigram.to_dict(),
            "patterns": self.patterns.to_dict(),
            "segmentation": self.segmentation.to_dict(),
        }

    def calculate_readability_score(self) -> float:
        """
        Calculate readability score using a weighted linear combination of factors.

        This method analyzes multiple text characteristics to produce a readability score
        on a scale from 0.0 (very easy to read) to 1.0 (very difficult to read).
        The score considers word length, sentence structure, paragraph organization,
        and vocabulary complexity to provide a comprehensive assessment.

        Returns:
            A float between 0.0 and 1.0 where higher values indicate more difficult text
        """
        # Normalize each factor to a 0-1 scale (higher means less readable)
        # Using higher caps for technical/legal content
        norm_word_length = min(
            1.0, self.unigram.average_token_length / 10.0
        )  # Cap at 10 chars
        norm_sentence_length = min(
            1.0, self.segmentation.average_sentence_length / 50.0
        )  # Cap at 50 words
        norm_paragraph_length = min(
            1.0, self.segmentation.average_paragraph_length / 800.0
        )  # Cap at 800 chars
        norm_entropy = min(1.0, self.unigram.token_entropy / 8.0)  # Cap at entropy of 8

        # Apply weights to each factor
        weights = {
            "word_length": 0.25,
            "sentence_length": 0.35,
            "paragraph_length": 0.15,
            "entropy": 0.25,
        }

        # Calculate weighted score (0-1 scale, higher means less readable)
        score = (
            weights["word_length"] * norm_word_length
            + weights["sentence_length"] * norm_sentence_length
            + weights["paragraph_length"] * norm_paragraph_length
            + weights["entropy"] * norm_entropy
        )

        return score

    def get_readability_level(self) -> str:
        """
        Get a human-readable assessment of text readability.

        This method translates the numerical readability score into a categorical
        assessment that's easier to interpret, ranging from "Easy" to "Very Complex".

        Returns:
            A string representing the readability level
        """
        score = self.calculate_readability_score()
        if score < 0.3:
            return "Easy"
        elif score < 0.5:
            return "Moderate"
        elif score < 0.7:
            return "Challenging"
        elif score < 0.85:
            return "Complex"
        else:
            return "Very Complex"

    def get_readability_assessment(self) -> Dict[str, Any]:
        """
        Get a detailed readability assessment with score, level, and contributing factors.

        This method provides a comprehensive assessment of text readability,
        including both the overall score and level, as well as information about
        the individual factors that contribute to the assessment.

        Returns:
            A dictionary containing readability score, level, and factor details
        """
        score = self.calculate_readability_score()
        level = self.get_readability_level()

        # Normalize each factor for reporting
        norm_word_length = min(1.0, self.unigram.average_token_length / 10.0)
        norm_sentence_length = min(
            1.0, self.segmentation.average_sentence_length / 50.0
        )
        norm_paragraph_length = min(
            1.0, self.segmentation.average_paragraph_length / 800.0
        )
        norm_entropy = min(1.0, self.unigram.token_entropy / 8.0)

        return {
            "score": score,
            "level": level,
            "factors": {
                "word_complexity": {
                    "raw_value": self.unigram.average_token_length,
                    "normalized_score": norm_word_length,
                    "weight": 0.25,
                },
                "sentence_complexity": {
                    "raw_value": self.segmentation.average_sentence_length,
                    "normalized_score": norm_sentence_length,
                    "weight": 0.35,
                },
                "paragraph_complexity": {
                    "raw_value": self.segmentation.average_paragraph_length,
                    "normalized_score": norm_paragraph_length,
                    "weight": 0.15,
                },
                "vocabulary_complexity": {
                    "raw_value": self.unigram.token_entropy,
                    "normalized_score": norm_entropy,
                    "weight": 0.25,
                },
            },
        }

    def summary(self) -> Dict[str, Any]:
        """
        Generate a high-level summary of key metrics.

        Returns:
            Dictionary with key metrics and assessments
        """
        return {
            "char_count": self.character.char_count,
            "token_count": self.unigram.token_count,
            "paragraph_count": self.segmentation.paragraph_count,
            "lexical_diversity": self.unigram.lexical_diversity,
            "readability_level": self.get_readability_level(),
            "readability_score": round(self.calculate_readability_score(), 2),
            "is_educational": self.patterns.is_educational,
            "is_interactive": self.patterns.is_interactive,
            "has_copyright": self.patterns.has_copyright_notices,
            "is_mostly_ascii": self.character.is_mostly_ascii,
            "has_high_entropy": self.character.has_high_entropy,
            "char_type_transitions": self.character.char_type_transitions,
            "consecutive_runs": self.character.consecutive_runs,
            "has_diverse_punctuation": self.character.has_diverse_punctuation,
            "has_complex_character_structure": self.character.has_complex_character_structure,
            "has_high_case_variation": self.character.has_high_case_variation,
            "category_entropy": round(self.character.category_entropy, 2),
            # New unigram metrics
            "hapax_legomena_ratio": round(self.unigram.hapax_legomena_ratio, 2),
            "top_5_token_coverage": round(self.unigram.top_5_token_coverage, 2),
            "short_token_ratio": round(self.unigram.short_token_ratio, 2),
            "long_token_ratio": round(self.unigram.long_token_ratio, 2),
            "has_high_uniqueness": self.unigram.has_high_uniqueness,
            "has_common_word_dominance": self.unigram.has_common_word_dominance,
            "has_complex_vocabulary": self.unigram.has_complex_vocabulary,
            "has_simple_vocabulary": self.unigram.has_simple_vocabulary,
        }


# Example of how to use this module:
"""
# Example 1: Calculate metrics for a single text and its tokens
text = "This is an example sentence."
token_ids = [101, 2023, 2003, 2019, 6251, 6202, 102]  # Example token IDs

analyzer = TokenizedAnalyzer()
result = analyzer.calculate_metrics(text, token_ids)
print(json.dumps(result, indent=2))

# Example 2: Calculate metrics for a batch of texts
texts = ["First example.", "Second example."]
tokens_batch = [[101, 2034, 6251, 102], [101, 2117, 6251, 102]]

results = analyzer.calculate_batch_metrics(texts, tokens_batch)
for i, result in enumerate(results):
    print(f"Text {i+1} metrics:")
    print(json.dumps(result, indent=2))

# Example 3: Using the new typed wrappers
import cheesecloth

# Get character metrics
char_metrics_dict = cheesecloth.get_all_char_metrics("Hello, world!")
char_metrics = CharMetrics.from_dict(char_metrics_dict)
print(f"Character count: {char_metrics.char_count}")
print(f"Is mostly ASCII: {char_metrics.is_mostly_ascii}")

# Get all metrics
all_metrics_dict = cheesecloth.get_all_metrics("Example text with questions? Yes, it has some.")
all_metrics = AllMetrics.from_dict(all_metrics_dict)
print(f"Has questions: {all_metrics.patterns.question_count > 0}")
print(f"Summary: {all_metrics.summary()}")
"""
