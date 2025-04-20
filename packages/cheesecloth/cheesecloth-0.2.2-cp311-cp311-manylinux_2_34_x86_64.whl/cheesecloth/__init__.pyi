"""
Type stubs for the Cheesecloth library.

This file provides type annotations for IDE completion and type checking
while maintaining the high-performance Rust implementation.

The stubs are organized into sections corresponding to the module structure:
- Character metrics and classification
- Unicode category analysis
- Text segmentation
- Unigram (word) tokenization and analysis
- Token metrics for ML tokenizers
- Advanced metrics (compression, Zipf's law)
- Data processing utilities

For detailed documentation on each function and parameter,
refer to the actual implementation in Rust with PyO3 bindings.
"""

from typing import Dict, List, Union, Tuple, Set, Any

# BatchProcessor class for efficient batch processing of text metrics
class BatchProcessor:
    """
    A configurable processor for computing selected text metrics on batches of documents.

    This class allows for selective computation of metrics to optimize performance
    when only specific metrics are needed.

    Attributes:
        enabled_metrics: Set of metric names to compute
    """

    enabled_metrics: Set[str]

    def __init__(
        self,
        metrics: List[str],
        include_punctuation: bool = True,
        case_sensitive: bool = False,
    ) -> None:
        """
        Initialize a new BatchProcessor with specified metrics enabled.

        Args:
            metrics: List of metric names to compute
            include_punctuation: Whether to include punctuation in unigram metrics
            case_sensitive: Whether to treat text as case-sensitive for unigram metrics
        """
        ...

    def compute_metrics(self, text: str) -> Dict[str, Any]:
        """
        Compute all enabled metrics for a single text.

        Args:
            text: The input text to analyze

        Returns:
            Dictionary mapping metric names to their values
        """
        ...

    def compute_batch_metrics(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Compute metrics for a batch of texts.

        Args:
            texts: List of input texts to analyze

        Returns:
            List of dictionaries, each mapping metric names to their values for one text
        """
        ...

# HyperAnalyzer class for high-performance single-pass metrics calculation
class HyperAnalyzer:
    """
    A high-performance analyzer that calculates all metrics in a single text traversal.

    This class provides the most efficient approach for comprehensive text analysis
    by computing all metrics in a single pass, which is ideal when most or all metrics
    are needed.

    Attributes:
        include_punctuation: Whether to include punctuation in unigram metrics
        case_sensitive: Whether to treat text as case-sensitive for unigram metrics
    """

    include_punctuation: bool
    case_sensitive: bool

    def __init__(
        self, include_punctuation: bool = True, case_sensitive: bool = False
    ) -> None:
        """
        Initialize a new HyperAnalyzer with specified options.

        Args:
            include_punctuation: Whether to include punctuation in unigram metrics
            case_sensitive: Whether to treat text as case-sensitive for unigram metrics
        """
        ...

    def calculate_char_metrics(self, text: str) -> Dict[str, Any]:
        """
        Calculate only character metrics for a text.

        Although this method uses the full implementation internally, it only returns
        character-related metrics in the result dictionary.

        Args:
            text: The input text to analyze

        Returns:
            Dictionary of character metrics
        """
        ...

    def calculate_all_metrics(self, text: str) -> Dict[str, Any]:
        """
        Calculate all metrics for a text (character, segmentation, and unigram).

        This method performs a single pass through the text to compute all metrics
        at once, which is more efficient than calculating them separately.

        Args:
            text: The input text to analyze

        Returns:
            Dictionary containing all metrics
        """
        ...

    def calculate_batch_metrics(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Calculate metrics for a batch of texts.

        Args:
            texts: List of input texts to analyze

        Returns:
            List of dictionaries, each containing all metrics for one text
        """
        ...

# Character count functions
def count_chars(text: str) -> int:
    """
    Count the total number of characters in the text.

    Args:
        text: The input text to analyze

    Returns:
        Total number of characters
    """
    ...

def count_words(text: str) -> int:
    """
    Count the total number of words in the text.

    Args:
        text: The input text to analyze

    Returns:
        Total number of words
    """
    ...

# ASCII functions
def is_ascii(text: str) -> bool:
    """
    Check if the entire text is ASCII.

    Args:
        text: The input text to analyze

    Returns:
        True if all characters are ASCII, False otherwise
    """
    ...

def is_char_ascii(ch: str) -> bool:
    """
    Check if a character is ASCII.

    Args:
        ch: The character to check

    Returns:
        True if the character is ASCII, False otherwise
    """
    ...

def ratio_ascii(text: str) -> float:
    """
    Calculate the ratio of ASCII characters in the text.

    Args:
        text: The input text to analyze

    Returns:
        Ratio of ASCII characters to total characters (0.0 to 1.0)
    """
    ...

# Character classification functions
def is_letter(ch: str) -> bool:
    """
    Check if a character is a letter (alphabetic).

    Args:
        ch: The character to check

    Returns:
        True if the character is a letter, False otherwise
    """
    ...

def is_digit(ch: str) -> bool:
    """
    Check if a character is a digit.

    Args:
        ch: The character to check

    Returns:
        True if the character is a digit, False otherwise
    """
    ...

def is_punctuation(ch: str) -> bool:
    """
    Check if a character is a punctuation mark.

    Args:
        ch: The character to check

    Returns:
        True if the character is a punctuation mark, False otherwise
    """
    ...

def is_symbol(ch: str) -> bool:
    """
    Check if a character is a symbol (e.g., +, <, =, >, ^, |, ~, $, %, etc.).

    Args:
        ch: The character to check

    Returns:
        True if the character is a symbol, False otherwise
    """
    ...

def is_whitespace(ch: str) -> bool:
    """
    Check if a character is whitespace.

    Args:
        ch: The character to check

    Returns:
        True if the character is whitespace, False otherwise
    """
    ...

def is_uppercase(ch: str) -> bool:
    """
    Check if a character is uppercase.

    Args:
        ch: The character to check

    Returns:
        True if the character is uppercase, False otherwise
    """
    ...

def is_lowercase(ch: str) -> bool:
    """
    Check if a character is lowercase.

    Args:
        ch: The character to check

    Returns:
        True if the character is lowercase, False otherwise
    """
    ...

def is_alphanumeric(ch: str) -> bool:
    """
    Check if a character is alphanumeric (letter or digit).

    Args:
        ch: The character to check

    Returns:
        True if the character is alphanumeric, False otherwise
    """
    ...

# Character metric functions
def count_letters(text: str) -> int:
    """
    Count the number of letters (alphabetic characters) in a string.

    Args:
        text: The input text to analyze

    Returns:
        Number of letters
    """
    ...

def count_digits(text: str) -> int:
    """
    Count the number of digits in a string.

    Args:
        text: The input text to analyze

    Returns:
        Number of digits
    """
    ...

def count_punctuation(text: str) -> int:
    """
    Count the number of punctuation characters in a string.

    Args:
        text: The input text to analyze

    Returns:
        Number of punctuation characters
    """
    ...

def count_symbols(text: str) -> int:
    """
    Count the number of symbol characters in a string.

    Args:
        text: The input text to analyze

    Returns:
        Number of symbol characters
    """
    ...

def count_whitespace(text: str) -> int:
    """
    Count the number of whitespace characters in a string.

    Args:
        text: The input text to analyze

    Returns:
        Number of whitespace characters
    """
    ...

def count_non_ascii(text: str) -> int:
    """
    Count the number of non-ASCII characters in a string.

    Args:
        text: The input text to analyze

    Returns:
        Number of non-ASCII characters
    """
    ...

def count_uppercase(text: str) -> int:
    """
    Count the number of uppercase characters in a string.

    Args:
        text: The input text to analyze

    Returns:
        Number of uppercase characters
    """
    ...

def count_lowercase(text: str) -> int:
    """
    Count the number of lowercase characters in a string.

    Args:
        text: The input text to analyze

    Returns:
        Number of lowercase characters
    """
    ...

def count_alphanumeric(text: str) -> int:
    """
    Count the number of alphanumeric characters in a string.

    Args:
        text: The input text to analyze

    Returns:
        Number of alphanumeric characters
    """
    ...

def ratio_uppercase(text: str) -> float:
    """
    Calculate the ratio of uppercase characters to all letters in a string.

    Args:
        text: The input text to analyze

    Returns:
        Ratio of uppercase characters to all letters (0.0 to 1.0)
    """
    ...

def ratio_alphanumeric(text: str) -> float:
    """
    Calculate the ratio of alphanumeric characters to all characters in a string.

    Args:
        text: The input text to analyze

    Returns:
        Ratio of alphanumeric characters to all characters (0.0 to 1.0)
    """
    ...

def ratio_alpha_to_numeric(text: str) -> float:
    """
    Calculate the ratio of alphabetic to numeric characters in a string.

    Args:
        text: The input text to analyze

    Returns:
        Ratio of alphabetic to numeric characters
    """
    ...

def ratio_whitespace(text: str) -> float:
    """
    Calculate the ratio of whitespace characters to all characters in a string.

    Args:
        text: The input text to analyze

    Returns:
        Ratio of whitespace characters to all characters (0.0 to 1.0)
    """
    ...

def ratio_digits(text: str) -> float:
    """
    Calculate the ratio of digit characters to all characters in a string.

    Args:
        text: The input text to analyze

    Returns:
        Ratio of digit characters to all characters (0.0 to 1.0)
    """
    ...

def ratio_punctuation(text: str) -> float:
    """
    Calculate the ratio of punctuation characters to all characters in a string.

    Args:
        text: The input text to analyze

    Returns:
        Ratio of punctuation characters to all characters (0.0 to 1.0)
    """
    ...

def char_entropy(text: str) -> float:
    """
    Calculate the Shannon entropy of a string at the character level.

    Shannon entropy is a measure of information content or randomness.

    Args:
        text: The input text to analyze

    Returns:
        Entropy value (higher value indicates more randomness/diversity)
    """
    ...

def combined_char_metrics(text: str) -> Dict[str, int]:
    """
    Calculate various character metrics in a single pass for efficiency.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary of character metrics with counts for different character types
    """
    ...

def get_all_char_metrics(
    text: str,
) -> Dict[
    str,
    Union[
        int,
        float,
        Dict[str, float],  # For category_ratios
        Dict[str, int],  # For char_frequency
        Dict[Tuple[str, str], float],  # For bigram_ratios
    ],
]:
    """
    Calculate comprehensive character metrics in a single efficient pass.

    This function computes all available character-level metrics, including counts,
    ratios, entropy, and frequency distributions in one operation for optimal performance.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary containing all character metrics, with nested dictionaries for
        complex metrics like frequencies and ratios
    """
    ...

# Unicode category functions
def get_unicode_categories(text: str) -> List[str]:
    """
    Get a list of Unicode categories for each character in the text.

    Args:
        text: The input text to analyze

    Returns:
        List of Unicode categories (e.g., "Lu" for uppercase letters, "Nd" for decimal digits)
    """
    ...

def get_unicode_category_groups(text: str) -> List[str]:
    """
    Get a list of Unicode category groups for each character in the text.

    Unicode category groups are the first letter of the category (e.g., "L" for all letters).

    Args:
        text: The input text to analyze

    Returns:
        List of Unicode category groups (e.g., "L" for letters, "N" for numbers, etc.)
    """
    ...

def count_unicode_categories(text: str) -> Dict[str, int]:
    """
    Count occurrences of each Unicode category in the text.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary mapping Unicode categories to their counts
    """
    ...

def count_unicode_category_groups(text: str) -> Dict[str, int]:
    """
    Count occurrences of each Unicode category group in the text.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary mapping Unicode category groups to their counts
    """
    ...

def get_unicode_category_ratios(text: str) -> Dict[str, float]:
    """
    Calculate the ratio of each Unicode category in the text.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary mapping Unicode categories to their frequency ratios (0.0 to 1.0)
    """
    ...

def get_unicode_category_group_ratios(text: str) -> Dict[str, float]:
    """
    Calculate the ratio of each Unicode category group in the text.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary mapping Unicode category groups to their frequency ratios (0.0 to 1.0)
    """
    ...

# Unicode category bigram functions
def get_unicode_category_bigrams(text: str) -> Dict[Tuple[str, str], int]:
    """
    Count occurrences of each Unicode category bigram (consecutive pair) in the text.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary mapping Unicode category bigrams (pairs of categories) to their counts
    """
    ...

def get_unicode_category_bigram_ratios(text: str) -> Dict[Tuple[str, str], float]:
    """
    Calculate the ratio of each Unicode category bigram in the text.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary mapping Unicode category bigrams to their frequency ratios (0.0 to 1.0)
    """
    ...

def get_unicode_category_group_bigrams(text: str) -> Dict[Tuple[str, str], int]:
    """
    Count occurrences of each Unicode category group bigram in the text.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary mapping Unicode category group bigrams to their counts
    """
    ...

def get_unicode_category_group_bigram_ratios(
    text: str,
) -> Dict[Tuple[str, str], float]:
    """
    Calculate the ratio of each Unicode category group bigram in the text.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary mapping Unicode category group bigrams to their frequency ratios (0.0 to 1.0)
    """
    ...

# Unicode category trigram functions
def get_unicode_category_trigrams(text: str) -> Dict[Tuple[str, str, str], int]:
    """
    Count occurrences of each Unicode category trigram in the text.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary mapping Unicode category trigrams to their counts
    """
    ...

def get_unicode_category_trigram_ratios(text: str) -> Dict[Tuple[str, str, str], float]:
    """
    Calculate the ratio of each Unicode category trigram in the text.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary mapping Unicode category trigrams to their frequency ratios (0.0 to 1.0)
    """
    ...

def get_unicode_category_group_trigrams(text: str) -> Dict[Tuple[str, str, str], int]:
    """
    Count occurrences of each Unicode category group trigram in the text.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary mapping Unicode category group trigrams to their counts
    """
    ...

def get_unicode_category_group_trigram_ratios(
    text: str,
) -> Dict[Tuple[str, str, str], float]:
    """
    Calculate the ratio of each Unicode category group trigram in the text.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary mapping Unicode category group trigrams to their frequency ratios (0.0 to 1.0)
    """
    ...

# Frequency functions
def get_char_frequency(text: str) -> Dict[str, int]:
    """
    Count the frequency of each character in a string.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary mapping characters to their counts
    """
    ...

def get_char_type_frequency(text: str) -> Dict[str, int]:
    """
    Count the frequency of each character type (letter, digit, punctuation, etc.) in a string.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary mapping character types to their counts
    """
    ...

def get_unicode_category_frequency(text: str) -> Dict[str, int]:
    """
    Count the frequency of each Unicode category in a string.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary mapping Unicode categories to their counts
    """
    ...

def get_unicode_category_group_frequency(text: str) -> Dict[str, int]:
    """
    Count the frequency of each Unicode category group in a string.

    Args:
        text: The input text to analyze

    Returns:
        Dictionary mapping Unicode category groups to their counts
    """
    ...

# Text segmentation functions
def split_words(text: str) -> List[str]:
    """
    Split text into words according to Unicode segmentation rules.

    Args:
        text: The input text to analyze

    Returns:
        List of words
    """
    ...

def split_lines(text: str) -> List[str]:
    """
    Split text into lines by newline characters (CR, LF, CRLF).

    Args:
        text: The input text to analyze

    Returns:
        List of lines as string references
    """
    ...

def segment_lines(text: str) -> List[str]:
    """
    Split text into lines, returning owned strings.

    Functionally identical to split_lines but returns owned strings.

    Args:
        text: The input text to analyze

    Returns:
        List of lines as owned strings
    """
    ...

def count_lines(text: str) -> int:
    """
    Count the number of lines in text.

    Args:
        text: The input text to analyze

    Returns:
        Number of lines
    """
    ...

def average_line_length(text: str) -> float:
    """
    Calculate the average line length in characters.

    Args:
        text: The input text to analyze

    Returns:
        Average number of characters per line
    """
    ...

def split_paragraphs(text: str) -> List[str]:
    """
    Split text into paragraphs (sequences of text separated by blank lines).

    Args:
        text: The input text to analyze

    Returns:
        List of paragraphs
    """
    ...

def segment_paragraphs(text: str) -> List[str]:
    """
    Split text into paragraphs, identical to split_paragraphs.

    Provided for API consistency with other segmentation functions.

    Args:
        text: The input text to analyze

    Returns:
        List of paragraphs
    """
    ...

def count_paragraphs(text: str) -> int:
    """
    Count the number of paragraphs in text.

    Args:
        text: The input text to analyze

    Returns:
        Number of paragraphs
    """
    ...

def average_paragraph_length(text: str) -> float:
    """
    Calculate the average paragraph length in characters.

    Args:
        text: The input text to analyze

    Returns:
        Average number of characters per paragraph
    """
    ...

def average_word_length(text: str) -> float:
    """
    Calculate the average word length in characters.

    Args:
        text: The input text to analyze

    Returns:
        Average number of characters per word
    """
    ...

def segment_sentences(text: str) -> List[str]:
    """
    Segment text into sentences based on common sentence terminators.

    Uses basic heuristics to identify sentence boundaries based on
    punctuation marks like periods, question marks, and exclamation points.

    Args:
        text: The input text to analyze

    Returns:
        List of sentences
    """
    ...

def average_sentence_length(text: str) -> float:
    """
    Estimate the average sentence length in words.

    Args:
        text: The input text to analyze

    Returns:
        Average number of words per sentence
    """
    ...

# Unigram tokenization and analysis functions
def tokenize_unigrams(text: str) -> List[str]:
    """
    Tokenize text into unigrams (words) without punctuation.

    Args:
        text: The input text to analyze

    Returns:
        List of unigram tokens (words)
    """
    ...

def tokenize_unigrams_with_punctuation(text: str) -> List[str]:
    """
    Tokenize text into unigrams (words) including punctuation.

    Args:
        text: The input text to analyze

    Returns:
        List of unigram tokens including punctuation
    """
    ...

def count_unigram_tokens(text: str, include_punctuation: bool) -> int:
    """
    Count the total number of unigram tokens in the text.

    Args:
        text: The input text to analyze
        include_punctuation: Whether to include punctuation as separate tokens

    Returns:
        Total number of unigram tokens
    """
    ...

def count_unique_unigrams(
    text: str, include_punctuation: bool, case_sensitive: bool
) -> int:
    """
    Count the number of unique unigram tokens in the text.

    Args:
        text: The input text to analyze
        include_punctuation: Whether to include punctuation as separate tokens
        case_sensitive: Whether to treat different cases as different tokens

    Returns:
        Number of unique unigram tokens
    """
    ...

def unigram_type_token_ratio(
    text: str, include_punctuation: bool, case_sensitive: bool
) -> float:
    """
    Calculate the type-token ratio (TTR) of unigrams in the text.

    TTR is the ratio of unique tokens to total tokens and is a measure of
    lexical diversity.

    Args:
        text: The input text to analyze
        include_punctuation: Whether to include punctuation as separate tokens
        case_sensitive: Whether to treat different cases as different tokens

    Returns:
        Type-token ratio (0.0 to 1.0)
    """
    ...

def unigram_repetition_rate(
    text: str, include_punctuation: bool, case_sensitive: bool
) -> float:
    """
    Calculate the repetition rate of unigrams in the text.

    Repetition rate is 1 - TTR (type-token ratio) and measures how much
    repetition occurs in the text.

    Args:
        text: The input text to analyze
        include_punctuation: Whether to include punctuation as separate tokens
        case_sensitive: Whether to treat different cases as different tokens

    Returns:
        Repetition rate (0.0 to 1.0)
    """
    ...

def get_unigram_frequency(
    text: str, include_punctuation: bool, case_sensitive: bool
) -> Dict[str, int]:
    """
    Count the frequency of each unigram in the text.

    Args:
        text: The input text to analyze
        include_punctuation: Whether to include punctuation as separate tokens
        case_sensitive: Whether to treat different cases as different tokens

    Returns:
        Dictionary mapping unigrams to their counts
    """
    ...

def unigram_entropy(
    text: str, include_punctuation: bool, case_sensitive: bool
) -> float:
    """
    Calculate the Shannon entropy of unigrams in the text.

    Shannon entropy is a measure of information content or randomness.

    Args:
        text: The input text to analyze
        include_punctuation: Whether to include punctuation as separate tokens
        case_sensitive: Whether to treat different cases as different tokens

    Returns:
        Entropy value (higher value indicates more diversity)
    """
    ...

def max_unigram_frequency_ratio(
    text: str, include_punctuation: bool, case_sensitive: bool
) -> float:
    """
    Calculate the ratio of the most frequent unigram to the total token count.

    Args:
        text: The input text to analyze
        include_punctuation: Whether to include punctuation as separate tokens
        case_sensitive: Whether to treat different cases as different tokens

    Returns:
        Ratio of the most frequent unigram to total tokens (0.0 to 1.0)
    """
    ...

def hapax_legomena_ratio(
    text: str, include_punctuation: bool, case_sensitive: bool
) -> float:
    """
    Calculate the ratio of words that appear exactly once (hapax legomena) to total words.

    This measures the proportion of unique words used only once in the text.

    Args:
        text: The input text to analyze
        include_punctuation: Whether to include punctuation as separate tokens
        case_sensitive: Whether to treat different cases as different tokens

    Returns:
        Hapax legomena ratio (0.0 to 1.0)
    """
    ...

def top_5_token_coverage(
    text: str, include_punctuation: bool, case_sensitive: bool
) -> float:
    """
    Calculate the percentage of text covered by the 5 most frequent tokens.

    This measures how much of the text is dominated by the most common words.

    Args:
        text: The input text to analyze
        include_punctuation: Whether to include punctuation as separate tokens
        case_sensitive: Whether to treat different cases as different tokens

    Returns:
        Top-5 token coverage (0.0 to 1.0)
    """
    ...

def short_token_ratio(
    text: str, include_punctuation: bool, case_sensitive: bool
) -> float:
    """
    Calculate the ratio of tokens with length ≤ 3 characters to total tokens.

    This measures the proportion of short words in the text.

    Args:
        text: The input text to analyze
        include_punctuation: Whether to include punctuation as separate tokens
        case_sensitive: Whether to treat different cases as different tokens

    Returns:
        Short token ratio (0.0 to 1.0)
    """
    ...

def long_token_ratio(
    text: str, include_punctuation: bool, case_sensitive: bool
) -> float:
    """
    Calculate the ratio of tokens with length ≥ 7 characters to total tokens.

    This measures the proportion of long words in the text.

    Args:
        text: The input text to analyze
        include_punctuation: Whether to include punctuation as separate tokens
        case_sensitive: Whether to treat different cases as different tokens

    Returns:
        Long token ratio (0.0 to 1.0)
    """
    ...

def get_all_unigram_metrics(
    text: str, include_punctuation: bool, case_sensitive: bool
) -> Dict[
    str,
    Union[
        int,  # For token counts
        float,  # For ratios, entropy, average lengths
    ],
]:
    """
    Calculate all unigram metrics in a single efficient pass.

    This function computes all available unigram-level metrics, including counts,
    ratios, entropy, and type-token ratio in one operation for optimal performance.

    Args:
        text: The input text to analyze
        include_punctuation: Whether to include punctuation as separate tokens
        case_sensitive: Whether to treat different cases as different tokens

    Returns:
        Dictionary containing all unigram metrics
    """
    ...

def get_all_pattern_metrics(
    text: str, use_paragraph_processing: bool = True, max_segment_size: int = 4096
) -> Dict[str, Union[int, float, bool]]:
    """
    Calculate all pattern-based metrics efficiently using optimized processing.

    This function provides pattern-based statistics such as question counts, factual statement detection,
    and content type indicators using regex pattern matching. For large texts, it can process by paragraph
    to improve performance.

    If a paragraph is longer than max_segment_size bytes, it will be further broken down
    into line segments for even more efficient processing.

    Args:
        text: The input text to analyze
        use_paragraph_processing: Whether to process text by paragraphs for better performance (default: True)
        max_segment_size: Maximum size in bytes for text segments before breaking them down (default: 4096)

    Returns:
        Dictionary containing pattern metrics like question counts, copyright mentions, etc.
    """
    ...

def get_all_metrics(
    text: str,
    include_punctuation: bool = True,
    case_sensitive: bool = False,
    use_paragraph_processing: bool = True,
    max_segment_size: int = 4096,
) -> Dict[str, Dict[str, Union[int, float, bool, Dict[str, float], Dict[str, int]]]]:
    """
    Calculate all metrics including character, unigram, segmentation, and pattern-based metrics.

    This comprehensive function minimizes round trips from Rust to Python by calculating all
    metrics in a single call. It returns a nested dictionary with the following sections:
    - 'character': Character-level metrics (counts, ratios, entropy)
    - 'unigram': Word-level metrics (token counts, type-token ratio)
    - 'segmentation': Text structure metrics (paragraphs, lines, sentences)
    - 'patterns': Pattern-based metrics (questions, copyright mentions)

    By default, pattern-based metrics use paragraph processing for efficiency, with large paragraphs
    further broken down into line segments for better performance.

    Args:
        text: The input text to analyze
        include_punctuation: Whether to include punctuation for unigram metrics (default: True)
        case_sensitive: Whether to treat text as case-sensitive for unigram metrics (default: False)
        use_paragraph_processing: Whether to use paragraph-based processing for patterns (default: True)
        max_segment_size: Maximum segment size in bytes before breaking down paragraphs (default: 4096)

    Returns:
        Nested dictionary containing all metrics organized by category
    """
    ...
