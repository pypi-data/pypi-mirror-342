#!/usr/bin/env python3
"""
Cheesecloth Command-Line Interface
=================================

A powerful command-line tool for text corpus analysis using Cheesecloth's
high-performance metrics. This tool enables quick analysis of datasets
from various sources, with comprehensive reporting options.

Key Features
-----------

1. Multiple Data Sources
   - Hugging Face datasets
   - Local JSONL files (including compressed .jsonl.gz and .jsonl.xz)
   - Local text files (including compressed .txt.gz and .txt.xz)
   - Standard input
   - Pre-tokenized data with decoder

2. Comprehensive Metrics
   - Character-level metrics (counts, ratios, entropy)
   - Unigram metrics (linguistic word-based)
   - Token metrics (for pre-tokenized data)
   - Document structure metrics
   - Advanced metrics (compression, Zipf's law)

3. Performance Options
   - Batch processing for efficiency
   - Sample mode for quick analysis of large datasets
   - Profiling capabilities for performance tuning
   - Progress reporting for long-running tasks

4. Output Formats
   - JSONL (for programmatic use)
   - CSV (for spreadsheet analysis)
   - Pretty-printed summary statistics
   - Detailed per-document metrics

Usage Examples
------------

Basic dataset analysis from Hugging Face:
```
cheesecloth-analyze "imdb" --limit 100
```

Analyzing a local JSONL file (falls back automatically):
```
cheesecloth-analyze "data.jsonl" --text-column "content"
```

Analyzing a compressed JSONL file:
```
cheesecloth-analyze "data.jsonl.gz" --text-column "content"
```

Analyzing a local text file (falls back automatically):
```
cheesecloth-analyze "my_document.txt"
```

Using with pre-tokenized data:
```
cheesecloth-analyze "alea-institute/kl3m-data-usc-sample" \\
                   --token-field "tokens" \\
                   --tokenizer-name "alea-institute/kl3m-004-128k-cased"
```

Using with local JSONL token data:
```
cheesecloth-analyze "tokens.jsonl" \\
                   --token-field "tokens" \\
                   --tokenizer-name "alea-institute/kl3m-004-128k-cased"
```

Using with compressed token data:
```
cheesecloth-analyze "tokens.jsonl.gz" \\
                   --token-field "tokens" \\
                   --tokenizer-name "alea-institute/kl3m-004-128k-cased"
```

Output to CSV with all metrics:
```
cheesecloth-analyze "imdb" --output metrics.csv --include-groups all
```

This CLI tool makes Cheesecloth's powerful analysis capabilities accessible
without requiring Python programming, enabling quick insights into text data.
It automatically falls back to local file processing when a Hugging Face dataset
cannot be loaded, making it flexible for both online and offline use.
"""

import argparse
import json
import gzip
import lzma
import sys
import datetime
import os
import cProfile
import pstats
from pstats import SortKey
import io
import signal
from pathlib import Path

try:
    from datasets import load_dataset
except ImportError:
    print(
        "Error: The 'datasets' package is required. Install it with 'pip install datasets'."
    )
    sys.exit(1)

try:
    import tokenizers
except ImportError:
    print(
        "Error: The 'tokenizers' package is required for token processing. "
        "Install it with 'pip install tokenizers'."
    )
    # Continue execution as tokenizer is optional

try:
    from tqdm import tqdm
except ImportError:
    # Define a simple fallback if tqdm is not available
    def tqdm(iterable, **_):
        """Simple fallback if tqdm is not available. Ignores all kwargs."""
        return iterable


import cheesecloth
from cheesecloth.tokenized_metrics import AllMetrics


# Helper function to get current time
def import_time():
    """Return the current datetime for tracking when imports/processing happened."""
    return datetime.datetime.now()


# Readability calculation helper functions
def calculate_readability_score(text, include_punctuation=False, case_sensitive=True):
    """Calculate readability score for a text using the AllMetrics class."""
    try:
        # Get metrics using get_all_metrics
        metrics_dict = cheesecloth.get_all_metrics(
            text,
            include_punctuation=include_punctuation,
            case_sensitive=case_sensitive,
            use_paragraph_processing=True,
        )

        # Create AllMetrics object
        all_metrics = AllMetrics.from_dict(metrics_dict)

        # Calculate and return readability score
        return all_metrics.calculate_readability_score()
    except Exception as e:
        print(f"Error calculating readability score: {e}", file=sys.stderr)
        return 0.0


def get_readability_level(text, include_punctuation=False, case_sensitive=True):
    """Get readability level label for a text using the AllMetrics class."""
    try:
        # Get metrics using get_all_metrics
        metrics_dict = cheesecloth.get_all_metrics(
            text,
            include_punctuation=include_punctuation,
            case_sensitive=case_sensitive,
            use_paragraph_processing=True,
        )

        # Create AllMetrics object
        all_metrics = AllMetrics.from_dict(metrics_dict)

        # Get and return readability level
        return all_metrics.get_readability_level()
    except Exception as e:
        print(f"Error getting readability level: {e}", file=sys.stderr)
        return "Unknown"


def get_readability_factors(text, include_punctuation=False, case_sensitive=True):
    """Get detailed readability factors for a text using the AllMetrics class."""
    try:
        # Get metrics using get_all_metrics
        metrics_dict = cheesecloth.get_all_metrics(
            text,
            include_punctuation=include_punctuation,
            case_sensitive=case_sensitive,
            use_paragraph_processing=True,
        )

        # Create AllMetrics object
        all_metrics = AllMetrics.from_dict(metrics_dict)

        # Get and return readability assessment
        return all_metrics.get_readability_assessment()
    except Exception as e:
        print(f"Error getting readability factors: {e}", file=sys.stderr)
        return {}


def run_with_profiling(func, profile_output=None):
    """Run a function with profiling enabled and save the results.

    Args:
        func: The function to profile
        profile_output: The output file path for profiling results

    Returns:
        The result of calling func()
    """
    # Set up the profiler
    profiler = cProfile.Profile()

    # Start profiling
    profiler.enable()

    try:
        # Run the function
        result = func()
    finally:
        # Stop profiling
        profiler.disable()

        # Create a StringIO object for the stats
        s = io.StringIO()

        # Get profiling stats
        ps = pstats.Stats(profiler, stream=s).sort_stats(SortKey.CUMULATIVE)
        ps.print_stats(50)  # Print top 50 most time-consuming functions

        # Write to file if specified
        if profile_output:
            # Ensure directory exists
            os.makedirs(
                os.path.dirname(os.path.abspath(profile_output)) or ".", exist_ok=True
            )

            # Save the raw profiling data for later analysis
            profiler.dump_stats(profile_output)

            # Create a human-readable text report
            text_output = profile_output + ".txt"
            with open(text_output, "w", encoding="utf-8") as f:
                ps = pstats.Stats(profiler, stream=f).sort_stats(SortKey.CUMULATIVE)
                ps.print_stats(100)  # More detailed for the file output

            print(f"Profiling data saved to {profile_output}")
            print(f"Human-readable report saved to {text_output}")

        # Print profiling summary to stderr
        print("\nProfiling Summary:", file=sys.stderr)
        print(s.getvalue(), file=sys.stderr)

    return result


# Define metric groups to align with Rust library module structure
METRIC_GROUPS = {
    # Character metrics (from char module)
    "char": [
        "char_count",
        "letter_count",
        "digit_count",
        "punctuation_count",
        "symbol_count",
        "whitespace_count",
        "non_ascii_count",
        "uppercase_count",
        "lowercase_count",
        "alphanumeric_count",
        "is_ascii",
        "ascii_ratio",
        "uppercase_ratio",
        "alphanumeric_ratio",
        "alpha_to_numeric_ratio",
        "whitespace_ratio",
        "digit_ratio",
        "punctuation_ratio",
        "char_entropy",
        "case_ratio",
        "category_entropy",
        "char_type_transitions",
        "consecutive_runs",
        "punctuation_diversity",
    ],
    # Text segmentation metrics (from text module)
    "text": [
        "word_count",
        "line_count",
        "avg_line_length",
        "paragraph_count",
        "avg_paragraph_length",
        "avg_word_length",
        "avg_sentence_length",
    ],
    # Unigram metrics (from unigram module)
    "unigram": [
        "unigram_count",
        "unique_unigram_count",
        "unigram_type_token_ratio",
        "unigram_repetition_rate",
        "unigram_frequency",
        "unigram_entropy",
    ],
    # Readability metrics (combined metrics for text analysis)
    "readability": [
        "readability_score",
        "readability_level",
        "readability_factors",
    ],
    # Pattern metrics (from patterns module)
    "patterns": [
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
    ],
    # Compression metrics (from compression module)
    "compression": [
        "compression_ratio",
        "unigram_compression_ratio",
    ],
    # Zipf's law and distribution metrics (from zipf module)
    "zipf": [
        "zipf_fitness_score",
        "power_law_exponent",
    ],
    # ML tokenization metrics (from token module)
    "token": [
        "subword_token_count",
        "unique_subword_count",
        "subword_type_token_ratio",
        "subword_repetition_rate",
        "subword_entropy",
        "subword_efficiency",
    ],
    # Frequency analyses (cross-cutting across modules)
    "frequency": [
        "char_frequency",
        "char_type_frequency",
        "unicode_category_frequency",
        "unicode_category_group_frequency",
    ],
    # Legacy groups for backward compatibility
    "basic": [
        "char_count",
        "word_count",
    ],
    "char_type": [
        "letter_count",
        "digit_count",
        "punctuation_count",
        "symbol_count",
        "whitespace_count",
        "non_ascii_count",
        "uppercase_count",
        "lowercase_count",
        "alphanumeric_count",
    ],
    "ratios": [
        "is_ascii",
        "ascii_ratio",
        "uppercase_ratio",
        "alphanumeric_ratio",
        "alpha_to_numeric_ratio",
        "whitespace_ratio",
        "digit_ratio",
        "punctuation_ratio",
    ],
    "entropy": [
        "char_entropy",
        "unigram_entropy",
    ],
    "segmentation": [
        "line_count",
        "avg_line_length",
        "paragraph_count",
        "avg_paragraph_length",
        "avg_word_length",
        "avg_sentence_length",
    ],
}

# Create a mapping from metric name to function
METRIC_FUNCTIONS = {
    #
    # Character module metrics (char)
    #
    "char_count": cheesecloth.count_chars,
    "letter_count": cheesecloth.count_letters,
    "digit_count": cheesecloth.count_digits,
    "punctuation_count": cheesecloth.count_punctuation,
    "symbol_count": cheesecloth.count_symbols,
    "whitespace_count": cheesecloth.count_whitespace,
    "non_ascii_count": cheesecloth.count_non_ascii,
    "uppercase_count": cheesecloth.count_uppercase,
    "lowercase_count": cheesecloth.count_lowercase,
    "alphanumeric_count": cheesecloth.count_alphanumeric,
    "is_ascii": cheesecloth.is_ascii,
    "ascii_ratio": cheesecloth.ratio_ascii,
    "uppercase_ratio": cheesecloth.ratio_uppercase,
    "alphanumeric_ratio": cheesecloth.ratio_alphanumeric,
    "alpha_to_numeric_ratio": cheesecloth.ratio_alpha_to_numeric,
    "whitespace_ratio": cheesecloth.ratio_whitespace,
    "digit_ratio": cheesecloth.ratio_digits,
    "punctuation_ratio": cheesecloth.ratio_punctuation,
    "char_entropy": cheesecloth.char_entropy,
    # New character metrics - access them through direct get_all_char_metrics function
    "case_ratio": lambda text: cheesecloth.get_all_char_metrics(text)["case_ratio"],
    "category_entropy": lambda text: cheesecloth.get_all_char_metrics(text)[
        "category_entropy"
    ],
    "char_type_transitions": lambda text: cheesecloth.get_all_char_metrics(text)[
        "char_type_transitions"
    ],
    "consecutive_runs": lambda text: cheesecloth.get_all_char_metrics(text)[
        "consecutive_runs"
    ],
    "punctuation_diversity": lambda text: cheesecloth.get_all_char_metrics(text)[
        "punctuation_diversity"
    ],
    #
    # Text segmentation metrics (text)
    #
    "word_count": cheesecloth.count_words,
    "line_count": cheesecloth.count_lines,
    "avg_line_length": cheesecloth.average_line_length,
    "paragraph_count": cheesecloth.count_paragraphs,
    "avg_paragraph_length": cheesecloth.average_paragraph_length,
    "avg_word_length": cheesecloth.average_word_length,
    "avg_sentence_length": cheesecloth.average_sentence_length,
    #
    # Unigram metrics (unigram)
    #
    "unigram_count": lambda text: cheesecloth.count_unigram_tokens(
        text, include_punctuation=False
    ),
    "unique_unigram_count": lambda text: cheesecloth.count_unique_unigrams(
        text, include_punctuation=False, case_sensitive=True
    ),
    "unigram_type_token_ratio": lambda text: cheesecloth.unigram_type_token_ratio(
        text, include_punctuation=False, case_sensitive=True
    ),
    "unigram_repetition_rate": lambda text: cheesecloth.unigram_repetition_rate(
        text, include_punctuation=False, case_sensitive=True
    ),
    "unigram_frequency": lambda text: cheesecloth.get_unigram_frequency(
        text, include_punctuation=False, case_sensitive=True
    ),
    "unigram_entropy": lambda text: cheesecloth.unigram_entropy(
        text, include_punctuation=False, case_sensitive=True
    ),
    #
    # Pattern-based metrics (patterns)
    #
    "question_count": cheesecloth.count_question_strings,
    "interrogative_question_count": cheesecloth.count_interrogative_questions,
    "complex_interrogative_count": cheesecloth.count_complex_interrogatives,
    "factual_statement_count": cheesecloth.count_factual_statements,
    "logical_reasoning_count": cheesecloth.count_logical_reasoning,
    "section_heading_count": cheesecloth.count_section_strings,
    "copyright_mention_count": cheesecloth.count_copyright_mentions,
    "rights_reserved_count": cheesecloth.count_rights_reserved,
    "bullet_count": lambda text: len(cheesecloth.BULLET_REGEX.findall(text))
    if hasattr(cheesecloth, "BULLET_REGEX")
    else 0,
    "ellipsis_count": lambda text: len(cheesecloth.ELLIPSIS_REGEX.findall(text))
    if hasattr(cheesecloth, "ELLIPSIS_REGEX")
    else 0,
    "bullet_ellipsis_ratio": cheesecloth.bullet_or_ellipsis_lines_ratio,
    "contains_code": cheesecloth.contains_code_characters,
    #
    # Compression metrics (compression)
    #
    "compression_ratio": cheesecloth.compression_ratio,
    "unigram_compression_ratio": lambda text: cheesecloth.unigram_compression_ratio(
        text, include_punctuation=False
    ),
    #
    # Zipf's law and distribution metrics (zipf)
    #
    "zipf_fitness_score": lambda text: cheesecloth.zipf_fitness_score(
        text, include_punctuation=False, case_sensitive=True
    ),
    "power_law_exponent": lambda text: cheesecloth.power_law_exponent(
        text, include_punctuation=False, case_sensitive=True
    ),
    #
    # ML-based tokenization metrics (token) - these require tokenizer path
    # so they're included for completeness but won't work without additional config
    #
    "subword_token_count": lambda text: cheesecloth.subword_token_count(text, None),
    "unique_subword_count": lambda text: cheesecloth.unique_subword_count(text, None),
    "subword_type_token_ratio": lambda text: cheesecloth.subword_type_token_ratio(
        text, None
    ),
    "subword_repetition_rate": lambda text: cheesecloth.subword_repetition_rate(
        text, None
    ),
    "subword_entropy": lambda text: cheesecloth.subword_entropy(text, None),
    "subword_efficiency": lambda text: cheesecloth.subword_efficiency(text, None),
    #
    # Frequency metrics (cross-cutting across modules)
    #
    "char_frequency": cheesecloth.get_char_frequency,
    "char_type_frequency": cheesecloth.get_char_type_frequency,
    "unicode_category_frequency": cheesecloth.get_unicode_category_frequency,
    "unicode_category_group_frequency": cheesecloth.get_unicode_category_group_frequency,
    #
    # Readability metrics (combined metrics using AllMetrics)
    #
    "readability_score": lambda text: calculate_readability_score(
        text, include_punctuation=False, case_sensitive=True
    ),
    "readability_level": lambda text: get_readability_level(
        text, include_punctuation=False, case_sensitive=True
    ),
    "readability_factors": lambda text: get_readability_factors(
        text, include_punctuation=False, case_sensitive=True
    ),
}


def get_enabled_metrics(args):
    """Get the list of metrics to calculate based on CLI arguments."""
    enabled_metrics = []

    # Patterns group is excluded from "all" by default due to performance impact
    # unless explicitly requested
    slow_groups = ["patterns"]

    # Include specific groups
    for group in args.include_groups:
        if group == "all":
            # Enable all groups except those explicitly excluded and slow groups
            for g, metrics in METRIC_GROUPS.items():
                if g not in args.exclude_groups and g not in slow_groups:
                    enabled_metrics.extend(metrics)

            # Output a note about excluded groups
            if not any(g in args.include_groups for g in slow_groups):
                print(
                    f"Note: Performance-intensive groups {slow_groups} are not included by default.",
                    file=sys.stderr,
                )
                print(
                    "      To include them, explicitly add them to --include-groups.",
                    file=sys.stderr,
                )
        elif group in METRIC_GROUPS:
            enabled_metrics.extend(METRIC_GROUPS[group])
        else:
            print(f"Warning: Unknown metric group '{group}'", file=sys.stderr)

    # Remove excluded groups
    for group in args.exclude_groups:
        if group in METRIC_GROUPS:
            for metric in METRIC_GROUPS[group]:
                if metric in enabled_metrics:
                    enabled_metrics.remove(metric)

    # Make sure each metric is only included once
    return list(dict.fromkeys(enabled_metrics))


def load_dataset_for_analysis(args):
    """Load and prepare the dataset for analysis.

    This function handles the dataset loading part, separated from metrics computation
    to allow for selective profiling. It will first check if the dataset string is a local file path.
    If not, it will attempt to load from a Hugging Face dataset.

    Args:
        args: Command line arguments

    Returns:
        tuple: (dataset, dataset_display_name)
    """
    # First check if the input is a local file
    file_path = args.dataset
    # Only attempt to check if the path exists when the dataset argument is actually provided
    # (this ensures we don't fail in test cases when args.dataset might be None)
    if file_path and Path(file_path).exists():
        print(f"Found local file: {file_path}", file=sys.stderr)
        # Process as local file (implementation follows later in this function)
    else:
        # Try to load from Hugging Face
        print(
            f"Local file not found. Attempting to load from Hugging Face: {args.dataset}",
            file=sys.stderr,
        )
        try:
            # Check if datasets library is available
            datasets_available = True
            try:
                # Check if datasets is imported
                if "load_dataset" not in globals():
                    datasets_available = False
                    raise ImportError("datasets library not available")
            except ImportError:
                datasets_available = False

            if datasets_available:
                # Load dataset with configuration if specified
                if args.config:
                    dataset = load_dataset(
                        args.dataset,
                        args.config,
                        split=args.split,
                        streaming=args.streaming,
                    )
                    dataset_display_name = f"{args.dataset}/{args.config}"
                else:
                    dataset = load_dataset(args.dataset, split=args.split)
                    dataset_display_name = args.dataset

                original_size = len(dataset)

                # Apply limit only if specified
                if args.limit is not None and args.limit < original_size:
                    dataset = dataset.select(range(args.limit))
                    print(
                        f"Limiting analysis to {args.limit} examples out of {original_size} total",
                        file=sys.stderr,
                    )
                else:
                    print(
                        f"Analyzing all {original_size} examples in the dataset",
                        file=sys.stderr,
                    )

                # Check if the required column exists (text_column or token_field)
                column_to_check = (
                    args.token_field if args.token_field else args.text_column
                )

                if column_to_check not in dataset.column_names:
                    print(
                        f"Error: Column '{column_to_check}' not found. Available columns: {dataset.column_names}",
                        file=sys.stderr,
                    )
                    sys.exit(1)

                # If both token_field and tokenizer_name are provided, verify tokenizer can be loaded
                if args.token_field and args.tokenizer_name:
                    try:
                        print(
                            f"Loading tokenizer: {args.tokenizer_name}", file=sys.stderr
                        )
                        tokenizers.Tokenizer.from_pretrained(args.tokenizer_name)
                    except Exception as e:
                        print(
                            f"Error loading tokenizer {args.tokenizer_name}: {e}",
                            file=sys.stderr,
                        )
                        sys.exit(1)

                return dataset, dataset_display_name

        except Exception as e:
            print(f"Error loading from Hugging Face: {e}", file=sys.stderr)
            print(
                f"Error: Neither a Hugging Face dataset nor a valid local file path: {file_path}",
                file=sys.stderr,
            )
            sys.exit(1)

    # If we get here, process as a local file

    # Create a custom dataset class to maintain the same interface
    class LocalFileDataset:
        """Dataset wrapper for local files that maintains the same interface as HF datasets."""

        def __init__(
            self, file_path, text_column, token_field, tokenizer_name, limit=None
        ):
            self.file_path = file_path
            self.text_column = text_column
            self.token_field = token_field
            self.tokenizer_name = tokenizer_name
            self.column_names = [text_column] if not token_field else [token_field]

            # Determine file type and load accordingly
            file_path_obj = Path(file_path)
            self.file_type = file_path_obj.suffix.lower()
            self.data = []
            self._load_data(limit)

        def _open_file(self, file_path):
            """Open a file with appropriate method based on extension"""
            if file_path.endswith(".gz") or file_path.endswith(".gzip"):
                print(f"Opening gzip compressed file: {file_path}", file=sys.stderr)
                return gzip.open(file_path, "rt", encoding="utf-8")
            if file_path.endswith(".xz"):
                print(f"Opening xz compressed file: {file_path}", file=sys.stderr)
                return lzma.open(file_path, "rt", encoding="utf-8")
            return open(file_path, "r", encoding="utf-8")

        def _load_data(self, limit):
            # Extract actual extension - handle multiple extensions like .jsonl.gz
            base_name = Path(self.file_path).name
            extensions = base_name.split(".")

            # Check if it's a JSON/JSONL file (compressed or not)
            is_jsonl = "jsonl" in extensions or "json" in extensions

            if is_jsonl:
                print(f"Loading JSONL file: {self.file_path}", file=sys.stderr)
                try:
                    # Load JSONL file with appropriate decompression if needed
                    with self._open_file(self.file_path) as f:
                        for i, line in enumerate(f):
                            if limit is not None and i >= limit:
                                break
                            try:
                                item = json.loads(line.strip())
                                self.data.append(item)
                            except json.JSONDecodeError:
                                print(
                                    f"Warning: Skipping invalid JSON at line {i + 1}",
                                    file=sys.stderr,
                                )
                except Exception as e:
                    print(f"Error loading JSONL file: {e}", file=sys.stderr)
                    sys.exit(1)
            else:
                # Treat as a plain text file
                print(f"Loading text file: {self.file_path}", file=sys.stderr)
                try:
                    # Try to open with appropriate decompression if needed
                    try:
                        with self._open_file(self.file_path) as f:
                            text = f.read()
                            # Create a single example with the entire file content
                            item = {self.text_column: text}
                            self.data.append(item)
                    except UnicodeDecodeError:
                        # Try with a different encoding for non-compressed files
                        if not (
                            self.file_path.endswith(".gz")
                            or self.file_path.endswith(".gzip")
                            or self.file_path.endswith(".xz")
                        ):
                            with open(self.file_path, "r", encoding="latin-1") as f:
                                text = f.read()
                                item = {self.text_column: text}
                                self.data.append(item)
                        else:
                            raise  # Re-raise for compressed files
                except Exception as e:
                    print(f"Error loading text file: {e}", file=sys.stderr)
                    sys.exit(1)

            print(f"Loaded {len(self.data)} examples from local file", file=sys.stderr)

        def __len__(self):
            return len(self.data)

        def __getitem__(self, idx):
            return self.data[idx]

    # Create the local dataset
    dataset = LocalFileDataset(
        file_path=file_path,
        text_column=args.text_column,
        token_field=args.token_field,
        tokenizer_name=args.tokenizer_name,
        limit=args.limit,
    )

    # Use the file name as the dataset display name
    dataset_display_name = Path(file_path).name

    # If both token_field and tokenizer_name are provided, verify tokenizer can be loaded
    if args.token_field and args.tokenizer_name:
        try:
            print(f"Loading tokenizer: {args.tokenizer_name}", file=sys.stderr)
            tokenizers.Tokenizer.from_pretrained(args.tokenizer_name)
        except Exception as e:
            print(
                f"Error loading tokenizer {args.tokenizer_name}: {e}", file=sys.stderr
            )
            sys.exit(1)

    return dataset, dataset_display_name


def setup_output_stream(args, dataset_display_name):
    """Set up the output stream for writing results.

    Args:
        args: Command line arguments
        dataset_display_name: Name of the dataset being analyzed

    Returns:
        tuple: (output_stream, output_file, output_file_handle)
    """
    output_file = None
    output_file_handle = None

    if args.stdout:
        # Use stdout for output, making sure to flush after each write
        output_stream = sys.stdout
        # Don't buffer stdout
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(line_buffering=True)
    else:
        # Determine output file name
        output_file = args.output
        if not output_file:
            # Generate a default filename based on dataset, config, and split
            safe_dataset_name = dataset_display_name.replace("/", "_").replace(
                "\\", "_"
            )
            output_file = f"{safe_dataset_name}_{args.split}_stats.jsonl"

        # Note: we're intentionally not using a context manager (with) here
        # because we need to keep the file open across function calls and
        # close it later in the analyze_dataset_main function
        output_file_handle = open(output_file, "w", encoding="utf-8")
        output_stream = output_file_handle
        print(f"Outputting results to {output_file}", file=sys.stderr)

    return output_stream, output_file, output_file_handle


def compute_metrics_for_dataset(dataset, args, metrics_to_calculate, output_stream):
    """Compute metrics for each example in the dataset.

    This is the core function that actually computes all metrics and should be the main
    target for profiling.

    Args:
        dataset: The dataset to analyze
        args: Command line arguments
        metrics_to_calculate: List of metrics to calculate
        output_stream: Stream to write results to

    Returns:
        tuple: (metric_sums, metric_counts, bool_metrics)
    """
    # Set up unigram function parameters based on command line args
    include_punctuation = args.unigram_include_punctuation
    case_sensitive = not args.unigram_case_insensitive

    # Determine which optimization mode to use
    all_metrics_mode = False
    optimized_metrics_mode = False

    # Check if optimized char and unigram metrics are requested
    if args.use_optimized_metrics:
        optimized_metrics_mode = True
        print(
            "Using optimized get_all_char_metrics and get_all_unigram_metrics (explicitly requested)",
            file=sys.stderr,
        )
    # Check if all metrics are requested
    elif args.use_all_metrics:
        all_metrics_mode = True
        print(
            "Using get_all_metrics (explicitly requested via --use-all-metrics)",
            file=sys.stderr,
        )
    elif args.include_groups == ["all"] and not args.exclude_groups:
        all_metrics_mode = True
        print("Using get_all_metrics for comprehensive analysis", file=sys.stderr)
    elif len(args.include_groups) >= 3 and set(args.include_groups).intersection(
        {"char", "text", "unigram", "readability"}
    ):
        # If at least 3 of the main module groups are requested, use get_all_metrics for efficiency
        all_metrics_mode = True
        print(
            "Using get_all_metrics for comprehensive analysis (multiple module groups requested)",
            file=sys.stderr,
        )
    # Legacy compatibility check
    elif set(metrics_to_calculate) >= set(
        METRIC_GROUPS["basic"]
        + METRIC_GROUPS["char_type"]
        + METRIC_GROUPS["ratios"]
        + METRIC_GROUPS["entropy"]
        + METRIC_GROUPS["segmentation"]
        + METRIC_GROUPS["unigram"]
    ):
        all_metrics_mode = True
        print(
            "Using get_all_metrics for comprehensive analysis (most legacy metric groups requested)",
            file=sys.stderr,
        )
    # Check if only char, unigram, and possibly readability metrics are requested
    elif (
        set(args.include_groups) <= set(["char", "unigram", "readability"])
        and not args.exclude_groups
    ):
        optimized_metrics_mode = True
        print(
            "Using optimized character, unigram, and readability metrics (based on requested groups)",
            file=sys.stderr,
        )

    # Set the analyzer based on the mode
    if optimized_metrics_mode:
        # Will use get_all_char_metrics and get_all_unigram_metrics directly
        analyzer = None
        print(
            "Using get_all_char_metrics and get_all_unigram_metrics for maximum performance",
            file=sys.stderr,
        )
    elif all_metrics_mode:
        # Will use get_all_metrics directly for each text
        analyzer = None
        print(
            "Using get_all_metrics for efficient combined processing", file=sys.stderr
        )
    elif args.use_hyper:
        # Create a HyperAnalyzer for ultra-efficient metric computation
        analyzer = cheesecloth.HyperAnalyzer(include_punctuation, case_sensitive)
        print("Using hyper-optimized analyzer for maximum performance", file=sys.stderr)
    else:
        # Create a standard BatchProcessor
        analyzer = cheesecloth.BatchProcessor(
            metrics_to_calculate, include_punctuation, case_sensitive
        )
        print("Using standard BatchProcessor for selective metrics", file=sys.stderr)

    # Frequency metrics to exclude from output by default
    frequency_metrics = ["char_frequency", "unigram_frequency"]

    # Keep these frequency metrics regardless of the include_frequencies flag
    always_include_frequencies = [
        "char_type_frequency",
        "unicode_category_frequency",
        "unicode_category_group_frequency",
    ]

    # Initialize tracking for averages and boolean metrics
    metric_sums = {}  # For calculating averages
    metric_counts = {}  # Number of valid values for each metric
    bool_metrics = {}  # For tracking boolean metrics

    # Set up progress bar
    print(f"Analyzing {len(dataset)} examples...", file=sys.stderr)
    progress_bar = tqdm(
        total=len(dataset),
        desc="Processing",
        unit="examples",
        file=sys.stderr,
        dynamic_ncols=True,  # Adjust to terminal size
        leave=True,  # Leave the progress bar after completion
    )

    # Use the batch size from command-line args or default
    batch_size = args.batch_size if args.batch_size else min(100, len(dataset))

    try:
        # Process dataset in batches
        for batch_start in range(0, len(dataset), batch_size):
            batch_end = min(batch_start + batch_size, len(dataset))
            batch_texts = []
            batch_indices = []

            # Collect texts for this batch
            for i in range(batch_start, batch_end):
                example = dataset[i]

                # Handle token field if specified
                if args.token_field and args.tokenizer_name:
                    tokens = example[args.token_field]
                    # Skip if not a valid token list
                    if not isinstance(tokens, list):
                        progress_bar.write(
                            f"Warning: Example {i} contains invalid token data (type: {type(tokens)}). Skipping."
                        )
                        continue

                    try:
                        # Decode tokens using tokenizer
                        # Load the tokenizer only once per batch for efficiency
                        if "tokenizer_cache" not in locals():
                            progress_bar.write(
                                f"Loading tokenizer: {args.tokenizer_name}"
                            )
                            tokenizer_cache = tokenizers.Tokenizer.from_pretrained(
                                args.tokenizer_name
                            )

                        # Decode the tokens
                        text = tokenizer_cache.decode(tokens)
                    except Exception as e:
                        progress_bar.write(
                            f"Warning: Error decoding tokens for example {i}: {e}. Skipping."
                        )
                        continue
                else:
                    # Use text column as normal
                    text = example[args.text_column]
                    if not isinstance(text, str):
                        progress_bar.write(
                            f"Warning: Example {i} contains non-string data. Skipping."
                        )
                        continue

                batch_texts.append(text)
                batch_indices.append(i)

            # Skip if batch is empty (unlikely)
            if not batch_texts:
                continue

            batch_results = []

            # Compute metrics for the entire batch at once
            if optimized_metrics_mode:
                # Process each text with optimized direct functions
                for text in batch_texts:
                    try:
                        # Use get_all_char_metrics and get_all_unigram_metrics for optimized analysis
                        flat_metrics = {}

                        # Character metrics using optimized direct function
                        char_metrics = cheesecloth.get_all_char_metrics(text)
                        for k, v in char_metrics.items():
                            flat_metrics[k] = v

                        # Unigram metrics using optimized direct function
                        unigram_metrics = cheesecloth.get_all_unigram_metrics(
                            text,
                            include_punctuation=include_punctuation,
                            case_sensitive=case_sensitive,
                        )
                        for k, v in unigram_metrics.items():
                            flat_metrics[k] = v

                        # Calculate readability metrics if needed
                        if (
                            "readability" in args.include_groups
                            or "all" in args.include_groups
                        ):
                            try:
                                # For readability metrics, we need segmentation metrics too,
                                # so get all metrics and create AllMetrics object
                                all_metrics_data = cheesecloth.get_all_metrics(
                                    text,
                                    include_punctuation=include_punctuation,
                                    case_sensitive=case_sensitive,
                                    use_paragraph_processing=True,
                                )
                                all_metrics = AllMetrics.from_dict(all_metrics_data)

                                # Add readability metrics
                                flat_metrics["readability_score"] = (
                                    all_metrics.calculate_readability_score()
                                )
                                flat_metrics["readability_level"] = (
                                    all_metrics.get_readability_level()
                                )
                                # Only include detailed factors if frequencies are included
                                if args.include_frequencies:
                                    flat_metrics["readability_factors"] = (
                                        all_metrics.get_readability_assessment()
                                    )
                            except Exception as e:
                                progress_bar.write(
                                    f"Warning: Could not calculate readability metrics in optimized mode: {e}"
                                )

                        batch_results.append(flat_metrics)
                    except Exception as e:
                        progress_bar.write(
                            f"Error computing metrics with optimized functions: {e}"
                        )
                        # Add an empty dict to maintain index alignment
                        batch_results.append({})

            elif all_metrics_mode:
                # Process each text with get_all_metrics
                for text in batch_texts:
                    try:
                        # Use get_all_metrics for comprehensive analysis
                        nested_metrics = cheesecloth.get_all_metrics(
                            text,
                            include_punctuation=include_punctuation,
                            case_sensitive=case_sensitive,
                            use_paragraph_processing=True,
                        )

                        # Flatten the nested dictionary for compatibility with existing code
                        flat_metrics = {}

                        # Character metrics
                        for k, v in nested_metrics["character"].items():
                            flat_metrics[k] = v

                        # Unigram metrics
                        for k, v in nested_metrics["unigram"].items():
                            flat_metrics[k] = v

                        # Segmentation metrics
                        for k, v in nested_metrics["segmentation"].items():
                            flat_metrics[k] = v

                        # Pattern metrics - prefix with pattern_ to avoid name conflicts
                        for k, v in nested_metrics["patterns"].items():
                            # Skip internal processing metadata unless explicitly requested
                            if k.startswith("_") and not args.include_frequencies:
                                continue
                            flat_metrics[f"pattern_{k}"] = v

                        # Add readability metrics using AllMetrics wrapper
                        try:
                            all_metrics = AllMetrics.from_dict(nested_metrics)
                            flat_metrics["readability_score"] = (
                                all_metrics.calculate_readability_score()
                            )
                            flat_metrics["readability_level"] = (
                                all_metrics.get_readability_level()
                            )
                            # Only include detailed factors if frequencies are included to avoid large output
                            if args.include_frequencies:
                                flat_metrics["readability_factors"] = (
                                    all_metrics.get_readability_assessment()
                                )
                        except Exception as e:
                            progress_bar.write(
                                f"Warning: Could not calculate readability metrics: {e}"
                            )

                        batch_results.append(flat_metrics)
                    except Exception as e:
                        progress_bar.write(
                            f"Error computing metrics with get_all_metrics: {e}"
                        )
                        # Add an empty dict to maintain index alignment
                        batch_results.append({})
            elif args.use_hyper:
                # For HyperAnalyzer
                try:
                    if len(batch_texts) == 1:
                        # For a single text, use calculate_all_metrics
                        batch_results = [analyzer.calculate_all_metrics(batch_texts[0])]
                    else:
                        # For multiple texts, use calculate_batch_metrics
                        batch_results = analyzer.calculate_batch_metrics(batch_texts)
                        batch_results = list(
                            batch_results
                        )  # Convert PyList to Python list
                except Exception as e:
                    progress_bar.write(
                        f"Error computing metrics with HyperAnalyzer: {e}"
                    )
                    continue
            else:
                # For BatchProcessor
                try:
                    if len(batch_texts) == 1:
                        # For a single text, use compute_metrics
                        batch_results = [analyzer.compute_metrics(batch_texts[0])]
                    else:
                        # For multiple texts, use compute_batch_metrics
                        batch_results = analyzer.compute_batch_metrics(batch_texts)
                        batch_results = list(
                            batch_results
                        )  # Convert PyList to Python list
                except Exception as e:
                    progress_bar.write(f"Error computing batch metrics: {e}")
                    continue

            # Process results for each text in the batch
            for example_idx, metrics in zip(batch_indices, batch_results):
                # Skip empty results (from errors)
                if not metrics:
                    continue

                # Update running sums and counts for averages
                for key, value in metrics.items():
                    if isinstance(value, bool):
                        # Handle boolean metrics
                        if key not in bool_metrics:
                            bool_metrics[key] = {"true": 0, "false": 0}
                        if value:
                            bool_metrics[key]["true"] += 1
                        else:
                            bool_metrics[key]["false"] += 1
                    elif isinstance(value, (int, float)):
                        # Handle numeric metrics
                        if key not in metric_sums:
                            metric_sums[key] = 0
                            metric_counts[key] = 0
                        metric_sums[key] += value
                        metric_counts[key] += 1

                # Filter results to only the requested metrics
                if args.use_hyper and not all_metrics_mode:
                    # When using HyperAnalyzer, filter to only include requested metrics
                    filtered_metrics = {
                        k: v for k, v in metrics.items() if k in metrics_to_calculate
                    }
                else:
                    filtered_metrics = metrics

                # Filter frequency metrics if needed
                if not args.include_frequencies:
                    # Only exclude certain frequency metrics
                    filtered_metrics = {
                        k: v
                        for k, v in filtered_metrics.items()
                        if k not in frequency_metrics or k in always_include_frequencies
                    }

                # Create and write the example record
                record = {
                    "record_type": "example",
                    "example_index": example_idx,
                }

                # Process filtered_metrics to ensure JSON serializable
                serializable_metrics = {}
                for k, v in filtered_metrics.items():
                    # Convert tuple keys to strings
                    if isinstance(v, dict) and any(
                        isinstance(dk, tuple) for dk in v.keys()
                    ):
                        serializable_v = {}
                        for dk, dv in v.items():
                            if isinstance(dk, tuple):
                                # Convert tuple to string representation
                                serializable_v[str(dk)] = dv
                            else:
                                serializable_v[dk] = dv
                        serializable_metrics[k] = serializable_v
                    else:
                        serializable_metrics[k] = v

                record.update(serializable_metrics)

                try:
                    output_stream.write(json.dumps(record) + "\n")
                except TypeError as e:
                    progress_bar.write(f"Error serializing record: {e}")
                    # Attempt more aggressive serialization fixing
                    try:
                        clean_record = {
                            k: (
                                str(v)
                                if not isinstance(
                                    v, (int, float, bool, str, list, dict, type(None))
                                )
                                else v
                            )
                            for k, v in record.items()
                        }
                        output_stream.write(json.dumps(clean_record) + "\n")
                    except Exception as e2:
                        progress_bar.write(
                            f"Failed to serialize record even after cleaning: {e2}"
                        )

            # Flush after each batch
            output_stream.flush()

            # Update progress bar
            progress_bar.update(batch_end - batch_start)
    finally:
        # Ensure progress bar is closed
        if "progress_bar" in locals() and progress_bar is not None:
            progress_bar.close()

    return metric_sums, metric_counts, bool_metrics


def analyze_dataset_main(args):
    """Main function that analyzes a dataset based on command line arguments.

    This function is separated from main() to allow for profiling.
    """
    # Load dataset (this part will not be profiled when using profile_metrics_only)
    dataset, dataset_display_name = load_dataset_for_analysis(args)

    # Determine which metrics to calculate
    metrics_to_calculate = get_enabled_metrics(args)
    print(f"Calculating metrics: {', '.join(metrics_to_calculate)}", file=sys.stderr)

    # Set up output stream
    output_stream, output_file, output_file_handle = setup_output_stream(
        args, dataset_display_name
    )

    # Write metadata record as first line
    metadata = {
        "record_type": "metadata",
        "dataset": dataset_display_name,
        "split": args.split,
        "total_examples": len(dataset),
        "metrics_calculated": metrics_to_calculate,
        "timestamp": import_time().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Add tokenizer information if provided
    if args.token_field and args.tokenizer_name:
        metadata.update(
            {
                "token_field": args.token_field,
                "tokenizer": args.tokenizer_name,
            }
        )
    output_stream.write(json.dumps(metadata) + "\n")
    output_stream.flush()

    try:
        # Perform the actual metrics computation - this is the part we want to profile separately
        if args.profile_metrics_only:
            # If profile_metrics_only is enabled, we'll profile only this function
            metric_sums, metric_counts, bool_metrics = run_with_profiling(
                lambda: compute_metrics_for_dataset(
                    dataset, args, metrics_to_calculate, output_stream
                ),
                args.profile_output,
            )
        else:
            # Normal execution without specific profiling
            metric_sums, metric_counts, bool_metrics = compute_metrics_for_dataset(
                dataset, args, metrics_to_calculate, output_stream
            )

        # Calculate averages from running sums
        avg_metrics = {
            f"avg_{k}": v / metric_counts[k]
            for k, v in metric_sums.items()
            if metric_counts[k] > 0
        }

        # Convert boolean metrics to percentages
        bool_percentages = {}
        for key, counts in bool_metrics.items():
            total = counts["true"] + counts["false"]
            if total > 0:
                bool_percentages[f"{key}_pct"] = (counts["true"] / total) * 100

        # Write summary record with averages and boolean metrics
        summary_record = {
            "record_type": "summary",
            "averages": avg_metrics,
            "bool_metrics": bool_percentages,
            "bool_counts": bool_metrics,
        }
        output_stream.write(json.dumps(summary_record) + "\n")
        output_stream.flush()

    finally:
        # Close file if we opened one
        if output_file_handle:
            output_file_handle.close()
            print(f"Results saved to {output_file}", file=sys.stderr)

    return output_file


def list_available_metrics():
    """Print available metric groups and their metrics, then exit."""
    # Define order of groups for display
    primary_groups = [
        "char",
        "text",
        "unigram",
        "readability",
        "compression",
        "zipf",
        "token",
    ]
    # Note: "patterns" group is excluded from defaults due to slower performance
    utility_groups = ["frequency"]
    legacy_groups = ["basic", "char_type", "ratios", "entropy", "segmentation"]

    print("Available metric groups based on Rust library structure:")
    print("------------------------------------------------------")

    # Print primary groups first
    for group in primary_groups:
        if group in METRIC_GROUPS:
            metrics = METRIC_GROUPS[group]
            print(f"\n{group}: ({len(metrics)} metrics)")
            for metric in metrics:
                print(f"  - {metric}")

    # Print utility groups next
    print("\nUtility groups:")
    print("-------------")
    for group in utility_groups:
        if group in METRIC_GROUPS:
            metrics = METRIC_GROUPS[group]
            print(f"\n{group}: ({len(metrics)} metrics)")
            for metric in metrics:
                print(f"  - {metric}")

    # Print legacy groups last
    print("\nLegacy groups (maintained for backward compatibility):")
    print("--------------------------------------------------")
    for group in legacy_groups:
        if group in METRIC_GROUPS:
            metrics = METRIC_GROUPS[group]
            print(f"\n{group}: ({len(metrics)} metrics)")
            for metric in metrics:
                print(f"  - {metric}")

    # Print performance notes and tips
    print("\nPerformance notes:")
    print("----------------")
    print(
        "- 'patterns' group is not included in the 'all' group by default due to slow performance"
    )
    print("- To include pattern metrics, add '--include-groups patterns' explicitly")
    print(
        "- For maximum performance, use '--use-optimized-metrics' to use get_all_char_metrics and get_all_unigram_metrics directly"
    )
    print(
        "- For comprehensive metrics, use '--use-all-metrics' to force using the optimized get_all_metrics function"
    )
    print("\nCommon usage examples:")
    print("------------------")
    print("Basic metrics:         --include-groups char text unigram")
    print("Char & unigram only:   --include-groups char unigram")
    print("With readability:      --include-groups char text unigram readability")
    print("Optimized core metrics: --use-optimized-metrics")
    print("All metrics:           --include-groups all")
    print("With pattern metrics:   --include-groups all patterns")

    sys.exit(0)


def main():
    """Main entry point for the CLI."""
    # Handle broken pipe errors gracefully (for piping to tools like head/tail)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    parser = argparse.ArgumentParser(description="Analyze text data using cheesecloth")

    # Add --list-metrics as a special flag that doesn't require dataset argument
    parser.add_argument(
        "--list-metrics",
        action="store_true",
        help="List available metric groups and exit",
    )

    # Dataset is not required if --list-metrics is provided
    parser.add_argument(
        "dataset",
        nargs="?",  # Make dataset optional
        help="Name of the Hugging Face dataset (e.g., 'imdb') or path to a local file",
    )
    parser.add_argument(
        "--config",
        help="Dataset configuration name (required for some datasets like GLUE)",
    )
    parser.add_argument(
        "--text-column", default="text", help="Column containing text (default: 'text')"
    )
    parser.add_argument(
        "--token-field", help="Column containing token IDs to be decoded by tokenizer"
    )
    parser.add_argument(
        "--tokenizer-name",
        help="Name of the tokenizer to use for decoding tokens (e.g., 'alea-institute/kl3m-004-128k-cased')",
    )
    parser.add_argument(
        "--split", default="train", help="Dataset split (default: 'train')"
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Maximum number of samples to analyze (default: process entire dataset)",
    )
    parser.add_argument(
        "--output", help="Output file path (default: {dataset}_{split}_stats.jsonl)"
    )

    # Metric group selection
    primary_groups = [
        "char",
        "text",
        "unigram",
        "readability",
        "compression",
        "zipf",
        "token",
    ]
    # Note: "patterns" group is excluded from defaults due to slower performance
    parser.add_argument(
        "--include-groups",
        nargs="+",
        default=["all"],
        help=(
            "Metric groups to include (default: 'all' except 'patterns'). "
            "Available primary groups: " + ", ".join(primary_groups) + ". "
            "Legacy groups: basic, char_type, ratios, entropy, segmentation. "
            "Utility groups: frequency. "
            "Performance-intensive group: patterns. "
            "Use --list-metrics for detailed information on all available metrics in each group. "
            "Note: 'patterns' group must be explicitly included due to performance impact."
        ),
    )
    parser.add_argument(
        "--exclude-groups",
        nargs="+",
        default=[],
        help="Metric groups to exclude (default: none). Applied after --include-groups.",
    )

    # Output options
    parser.add_argument(
        "--no-examples",
        action="store_true",
        help="Don't include individual examples in output",
    )
    parser.add_argument(
        "--example-limit",
        type=int,
        default=5,
        help="Maximum number of examples to include in output (default: 5)",
    )
    parser.add_argument(
        "--include-frequencies",
        action="store_true",
        help="Include all frequency distributions including char_frequency and unigram_frequency (can make output very large)",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print results to stdout instead of saving to a file",
    )

    # Unigram options
    parser.add_argument(
        "--unigram-include-punctuation",
        action="store_true",
        help="Include punctuation in unigram analysis",
    )
    parser.add_argument(
        "--unigram-case-insensitive",
        action="store_true",
        help="Perform case-insensitive unigram analysis",
    )

    # Performance options
    parser.add_argument(
        "--streaming",
        action="store_true",
        help="Use streaming mode for hugging face datasets (default: False)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        help="Number of examples to process in each batch (default: 100)",
    )
    parser.add_argument(
        "--use-hyper",
        action="store_true",
        help="Use the hyper-optimized analyzer for maximum performance",
    )
    parser.add_argument(
        "--use-all-metrics",
        action="store_true",
        help="Force using the get_all_metrics function which efficiently computes character, unigram, segmentation, and pattern metrics in one pass",
    )
    parser.add_argument(
        "--use-optimized-metrics",
        action="store_true",
        help="Use optimized get_all_char_metrics and get_all_unigram_metrics functions directly, without pattern metrics for maximum performance",
    )

    # Profiling options
    parser.add_argument(
        "--profile",
        action="store_true",
        help="Enable profiling to identify performance bottlenecks",
    )
    parser.add_argument(
        "--profile-metrics-only",
        action="store_true",
        help="Profile only the metric computation, excluding dataset loading",
    )
    parser.add_argument(
        "--profile-output",
        help="Output file for profiling results (default: {dataset}_{split}_profile.prof)",
    )

    args = parser.parse_args()

    # Handle --list-metrics option first
    if args.list_metrics:
        # Call the helper function that prints metrics and exits
        list_available_metrics()

    # For all other operations, dataset is required
    if not args.dataset:
        parser.error(
            "the dataset argument is required unless --list-metrics is specified"
        )

    # At this point we know args.list_metrics is False and args.dataset is not None,
    # so we can safely proceed with dataset analysis

    # Handle profiling if requested
    if args.profile:
        # Determine profiling output file
        profile_output = args.profile_output
        if not profile_output:
            # Generate default profiling output filename
            safe_dataset_name = args.dataset.replace("/", "_").replace("\\", "_")
            if args.config:
                safe_dataset_name += (
                    f"_{args.config.replace('/', '_').replace('\\', '_')}"
                )

            # Add a suffix to indicate what was profiled
            if args.profile_metrics_only:
                profile_output = (
                    f"{safe_dataset_name}_{args.split}_metrics_profile.prof"
                )
            else:
                profile_output = f"{safe_dataset_name}_{args.split}_full_profile.prof"

        # Ensure directory exists
        os.makedirs(
            os.path.dirname(os.path.abspath(profile_output)) or ".", exist_ok=True
        )

        if args.profile_metrics_only:
            print(
                f"Profiling metrics computation only. Results will be saved to: {profile_output}",
                file=sys.stderr,
            )
            # We don't run with profiling here - the profiling will be done in analyze_dataset_main for the metrics only
            args.profile_output = profile_output
            return analyze_dataset_main(args)
        print(
            f"Profiling entire analysis. Results will be saved to: {profile_output}",
            file=sys.stderr,
        )
        # Profile the whole function
        return run_with_profiling(lambda: analyze_dataset_main(args), profile_output)
    # Run the analysis normally
    return analyze_dataset_main(args)


if __name__ == "__main__":
    main()
