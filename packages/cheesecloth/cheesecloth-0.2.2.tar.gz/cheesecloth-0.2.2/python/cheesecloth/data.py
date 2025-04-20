#!/usr/bin/env python3
"""
Data Loading and Processing Utilities for Cheesecloth
====================================================

This module provides a unified interface for loading and processing text data from
various sources, enabling streamlined analysis workflows for different text formats.

Key Components
-------------

1. TextDataLoader
   - Unified interface for reading text from multiple sources
   - Support for raw text files, JSONL, and Hugging Face datasets
   - Handles both raw text and tokenized text (with decoding)
   - Configurable batch processing for memory efficiency

2. TextBatchProcessor
   - Connects data loading with metric calculation
   - Processes text in optimized batches
   - Compatible with both BatchProcessor and HyperAnalyzer
   - Handles various input sources through a consistent API

3. Convenience Functions
   - process_text_file: Process a single text file
   - process_jsonl_file: Process a JSONL file with text data
   - process_huggingface_dataset: Process data from Hugging Face

Supported Input Formats
---------------------

1. Raw text files
   - Complete file as single document
   - Byte-by-byte streaming for large files

2. JSONL files
   - Text fields for raw text processing
   - Token ID fields for pre-tokenized data

3. Hugging Face datasets
   - Direct integration with datasets library
   - Support for different splits and configurations
   - Processing of both text and token fields

The module is designed to handle large-scale text processing efficiently, with
careful memory management and batch processing capabilities.
"""

import json
from pathlib import Path
from typing import (
    Any,
    Dict,
    Generator,
    Iterable,
    List,
    Literal,
    Optional,
    TypeVar,
    Union,
    cast,
)

import datasets
import tokenizers

# Type definitions
TextSource = Union[str, Path, bytes, Iterable[bytes]]
T = TypeVar("T")


class TextProcessor:
    """Base class for text processing that implements common utilities."""

    @staticmethod
    def read_bytes_from_file(
        file_path: Union[str, Path], batch_size: Optional[int] = None
    ) -> Generator[bytes, None, None]:
        """
        Read a file in byte batches.

        Args:
            file_path: Path to the file
            batch_size: Size of each batch in bytes, or None to read the entire file

        Yields:
            Batches of bytes from the file
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if batch_size is None:
            # Read the entire file as a single batch
            with open(file_path, "rb") as f:
                yield f.read()
        else:
            # Read the file in batches
            with open(file_path, "rb") as f:
                while True:
                    batch = f.read(batch_size)
                    if not batch:
                        break
                    yield batch

    @staticmethod
    def decode_bytes(
        data: bytes, encoding: str = "utf-8", errors: str = "replace"
    ) -> str:
        """
        Decode bytes to string with robust error handling.

        Args:
            data: Bytes to decode
            encoding: Text encoding to use
            errors: Error handling strategy ('strict', 'replace', 'ignore')

        Returns:
            Decoded string
        """
        return data.decode(encoding, errors=errors)


class TokenizerWrapper:
    """Wrapper for tokenizer operations with consistent interface."""

    def __init__(self, tokenizer_or_name: Union[str, tokenizers.Tokenizer]):
        """
        Initialize tokenizer wrapper.

        Args:
            tokenizer_or_name: Either a tokenizer instance or name of a pre-trained tokenizer
        """
        if isinstance(tokenizer_or_name, str):
            # Load a pre-trained tokenizer by name
            self.tokenizer = tokenizers.Tokenizer.from_pretrained(tokenizer_or_name)
        else:
            # Use the provided tokenizer
            self.tokenizer = tokenizer_or_name

    def decode(
        self, tokens: Union[List[int], List[List[int]]]
    ) -> Union[str, List[str]]:
        """
        Decode tokens to text.

        Args:
            tokens: Token IDs to decode (single sequence or batch)

        Returns:
            Decoded text string(s)
        """
        if not tokens:
            return ""

        # Handle single sequence vs batch
        if isinstance(tokens[0], list):
            # Batch of token sequences
            return [self.tokenizer.decode(t) for t in tokens]
        else:
            # Single token sequence
            return self.tokenizer.decode(cast(List[int], tokens))


class TextDataLoader:
    """
    Unified interface for loading text data from various sources.

    This class handles all the specified input cases:
    1. Raw text file sent as a single string
    2. Raw text file sent as N byte batches
    3. JSONL file with a raw text field
    4. JSONL file with a token field and a tokenizer to decode
    5. HuggingFace dataset with a raw text field
    6. HuggingFace dataset with a token field and a tokenizer to decode
    """

    def __init__(
        self,
        text_column: str = "text",
        token_column: Optional[str] = None,
        tokenizer: Optional[Union[str, tokenizers.Tokenizer]] = None,
        encoding: str = "utf-8",
        batch_size: Optional[int] = None,
    ):
        """
        Initialize the data loader.

        Args:
            text_column: Column name for text data in JSONL or datasets
            token_column: Column name for token data (if using tokens)
            tokenizer: Tokenizer to use for decoding tokens (name or instance)
            encoding: Text encoding for decoding bytes
            batch_size: Batch size in bytes for reading large files
        """
        self.text_column = text_column
        self.token_column = token_column
        self.encoding = encoding
        self.batch_size = batch_size

        # Initialize tokenizer if provided
        self.tokenizer = None
        if tokenizer is not None:
            self.tokenizer = TokenizerWrapper(tokenizer)

        # Check if we're using tokens and have a tokenizer
        if token_column is not None and self.tokenizer is None:
            raise ValueError("When using token_column, a tokenizer must be provided")

    def _process_tokens(self, tokens: Union[List[int], List[List[int]]]) -> str:
        """
        Process token data by decoding it to text.

        Args:
            tokens: Token IDs to decode

        Returns:
            Decoded text
        """
        if self.tokenizer is None:
            raise ValueError("Tokenizer is required for processing tokens")

        return cast(str, self.tokenizer.decode(tokens))

    def load_raw_text(self, text: Union[str, bytes]) -> str:
        """
        Load raw text from a string or bytes.

        Args:
            text: Raw text as string or bytes

        Returns:
            Processed text string
        """
        if isinstance(text, bytes):
            return TextProcessor.decode_bytes(text, self.encoding)
        return text

    def load_raw_text_file(self, file_path: Union[str, Path]) -> str:
        """
        Load an entire text file as a single string.

        Args:
            file_path: Path to the text file

        Returns:
            File contents as a string
        """
        data = next(TextProcessor.read_bytes_from_file(file_path))
        return TextProcessor.decode_bytes(data, self.encoding)

    def load_raw_text_batches(
        self, file_path: Union[str, Path]
    ) -> Generator[str, None, None]:
        """
        Load a text file in batches.

        Args:
            file_path: Path to the text file

        Yields:
            Batches of text from the file
        """
        if self.batch_size is None:
            # Default to a reasonable batch size if none specified
            batch_size = 1024 * 1024  # 1 MB
        else:
            batch_size = self.batch_size

        for batch in TextProcessor.read_bytes_from_file(file_path, batch_size):
            yield TextProcessor.decode_bytes(batch, self.encoding)

    def load_jsonl_file(
        self, file_path: Union[str, Path]
    ) -> Generator[str, None, None]:
        """
        Load text from a JSONL file.

        Args:
            file_path: Path to the JSONL file

        Yields:
            Text content from each JSON object
        """
        with open(file_path, "r", encoding=self.encoding) as f:
            for line in f:
                if not line.strip():
                    continue

                try:
                    data = json.loads(line)

                    # Handle token data if specified
                    if self.token_column is not None and self.token_column in data:
                        tokens = data[self.token_column]
                        yield self._process_tokens(tokens)
                    # Otherwise look for text data
                    elif self.text_column in data:
                        yield data[self.text_column]
                    else:
                        # Skip if neither column exists
                        continue
                except json.JSONDecodeError:
                    # Skip invalid JSON lines
                    continue

    def load_huggingface_dataset(
        self, dataset_name: str, config_name: Optional[str] = None, split: str = "train"
    ) -> Generator[str, None, None]:
        """
        Load text from a Hugging Face dataset.

        Args:
            dataset_name: Name of the dataset on Hugging Face Hub
            config_name: Configuration name for the dataset
            split: Dataset split to use

        Yields:
            Text content from each example
        """
        # Load the dataset
        dataset = datasets.load_dataset(dataset_name, config_name, split=split)

        # Validate that the required column exists
        column_to_use = (
            self.token_column if self.token_column is not None else self.text_column
        )
        if column_to_use not in dataset.column_names:
            raise ValueError(
                f"Column '{column_to_use}' not found in dataset. "
                f"Available columns: {dataset.column_names}"
            )

        # Process each example
        for example in dataset:
            if self.token_column is not None:
                # Handle token data
                tokens = example[self.token_column]
                yield self._process_tokens(tokens)
            else:
                # Handle text data
                yield example[self.text_column]

    def load_text_from_source(
        self,
        source: Union[str, Path, Dict[str, Any], datasets.Dataset],
        source_type: Literal["text", "file", "jsonl", "dataset"] = "text",
    ) -> Generator[str, None, None]:
        """
        Universal method to load text from various sources.

        Args:
            source: The data source
            source_type: Type of source (text, file, jsonl, dataset)

        Yields:
            Text content from the source
        """
        if source_type == "text":
            # Raw text string
            yield self.load_raw_text(cast(Union[str, bytes], source))

        elif source_type == "file":
            # Text file path
            file_path = cast(Union[str, Path], source)
            if self.batch_size is None:
                # Load entire file
                yield self.load_raw_text_file(file_path)
            else:
                # Load file in batches
                yield from self.load_raw_text_batches(file_path)

        elif source_type == "jsonl":
            # JSONL file
            yield from self.load_jsonl_file(cast(Union[str, Path], source))

        elif source_type == "dataset":
            # HuggingFace dataset
            if isinstance(source, dict):
                # Dataset parameters provided as dict
                params = cast(Dict[str, Any], source)
                dataset_name = params.get("name")
                config_name = params.get("config")
                split = params.get("split", "train")

                if dataset_name is None:
                    raise ValueError("Dataset name must be provided")

                yield from self.load_huggingface_dataset(
                    dataset_name, config_name, split
                )

            elif isinstance(source, str):
                # Just dataset name provided
                yield from self.load_huggingface_dataset(cast(str, source))

            elif isinstance(source, datasets.Dataset):
                # Dataset instance provided directly
                dataset = cast(datasets.Dataset, source)

                # Validate column exists
                column_to_use = (
                    self.token_column
                    if self.token_column is not None
                    else self.text_column
                )
                if column_to_use not in dataset.column_names:
                    raise ValueError(
                        f"Column '{column_to_use}' not found in dataset. "
                        f"Available columns: {dataset.column_names}"
                    )

                # Process each example
                for example in dataset:
                    if self.token_column is not None:
                        # Handle token data
                        tokens = example[self.token_column]
                        yield self._process_tokens(tokens)
                    else:
                        # Handle text data
                        yield example[self.text_column]
        else:
            raise ValueError(f"Unsupported source type: {source_type}")


class TextBatchProcessor:
    """
    Process text data in batches for efficient processing.

    This class provides a unified interface for processing text data from various
    sources and feeding it to the metric calculation engine in optimized batches.
    """

    def __init__(
        self,
        analyzer: Any,  # Can be BatchProcessor or HyperAnalyzer
        data_loader: Optional[TextDataLoader] = None,
        batch_size: int = 100,
        text_column: str = "text",
        token_column: Optional[str] = None,
        tokenizer: Optional[Union[str, tokenizers.Tokenizer]] = None,
    ):
        """
        Initialize the batch processor.

        Args:
            analyzer: The metric analyzer to use (BatchProcessor or HyperAnalyzer)
            data_loader: Custom data loader instance or None to create a default one
            batch_size: Number of texts to process in each batch
            text_column: Column name for text in structured data
            token_column: Column name for tokens in structured data
            tokenizer: Tokenizer to use for token decoding
        """
        self.analyzer = analyzer
        self.batch_size = batch_size

        # Create default data loader if not provided
        if data_loader is None:
            self.data_loader = TextDataLoader(
                text_column=text_column, token_column=token_column, tokenizer=tokenizer
            )
        else:
            self.data_loader = data_loader

    def _is_hyper_analyzer(self) -> bool:
        """Check if we're using a HyperAnalyzer."""
        return hasattr(self.analyzer, "calculate_batch_metrics")

    def process_texts(self, texts: Iterable[str]) -> List[Dict[str, Any]]:
        """
        Process a batch of texts.

        Args:
            texts: Iterable of text strings

        Returns:
            List of metric results for each text
        """
        # Convert to list in case it's a generator
        text_batch = list(texts)

        if not text_batch:
            return []

        if self._is_hyper_analyzer():
            # Use HyperAnalyzer
            results = self.analyzer.calculate_batch_metrics(text_batch)
            return list(results)  # Convert PyList to Python list if needed
        else:
            # Use BatchProcessor
            results = self.analyzer.compute_batch_metrics(text_batch)
            return list(results)

    def process_from_source(
        self,
        source: Union[str, Path, Dict[str, Any], datasets.Dataset, Iterable[str]],
        source_type: Literal["text", "file", "jsonl", "dataset", "texts"] = "texts",
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Process text data from any supported source.

        Args:
            source: The data source
            source_type: Type of source (text, file, jsonl, dataset, or texts for iterable of strings)

        Yields:
            Metric results for each processed text
        """
        if source_type == "texts":
            # Already a collection of texts
            texts = cast(Iterable[str], source)
            batch = []

            for text in texts:
                batch.append(text)

                if len(batch) >= self.batch_size:
                    results = self.process_texts(batch)
                    yield from results
                    batch = []

            # Process any remaining texts
            if batch:
                results = self.process_texts(batch)
                yield from results
        else:
            # Use TextDataLoader to get text from other sources
            text_gen = self.data_loader.load_text_from_source(source, source_type)
            batch = []

            for text in text_gen:
                batch.append(text)

                if len(batch) >= self.batch_size:
                    results = self.process_texts(batch)
                    yield from results
                    batch = []

            # Process any remaining texts
            if batch:
                results = self.process_texts(batch)
                yield from results


# Convenience functions for common use cases


def process_text_file(
    file_path: Union[str, Path],
    analyzer: Any,
    batch_size: int = 100,
    encoding: str = "utf-8",
) -> List[Dict[str, Any]]:
    """
    Process a text file and return metrics.

    Args:
        file_path: Path to the text file
        analyzer: The metric analyzer to use
        batch_size: Size of text batches to process
        encoding: Text encoding

    Returns:
        List of metric results
    """
    loader = TextDataLoader(encoding=encoding)
    processor = TextBatchProcessor(analyzer, data_loader=loader, batch_size=batch_size)

    return list(processor.process_from_source(file_path, "file"))


def process_jsonl_file(
    file_path: Union[str, Path],
    analyzer: Any,
    text_column: str = "text",
    token_column: Optional[str] = None,
    tokenizer: Optional[Union[str, tokenizers.Tokenizer]] = None,
    batch_size: int = 100,
) -> List[Dict[str, Any]]:
    """
    Process a JSONL file and return metrics.

    Args:
        file_path: Path to the JSONL file
        analyzer: The metric analyzer to use
        text_column: Column name for text data
        token_column: Column name for token data (if using tokens)
        tokenizer: Tokenizer to use for decoding tokens
        batch_size: Size of text batches to process

    Returns:
        List of metric results
    """
    loader = TextDataLoader(
        text_column=text_column, token_column=token_column, tokenizer=tokenizer
    )
    processor = TextBatchProcessor(analyzer, data_loader=loader, batch_size=batch_size)

    return list(processor.process_from_source(file_path, "jsonl"))


def process_huggingface_dataset(
    dataset_name: str,
    analyzer: Any,
    config_name: Optional[str] = None,
    split: str = "train",
    text_column: str = "text",
    token_column: Optional[str] = None,
    tokenizer: Optional[Union[str, tokenizers.Tokenizer]] = None,
    batch_size: int = 100,
) -> List[Dict[str, Any]]:
    """
    Process a Hugging Face dataset and return metrics.

    Args:
        dataset_name: Name of the dataset on Hugging Face Hub
        analyzer: The metric analyzer to use
        config_name: Configuration name for the dataset
        split: Dataset split to use
        text_column: Column name for text data
        token_column: Column name for token data (if using tokens)
        tokenizer: Tokenizer to use for decoding tokens
        batch_size: Size of text batches to process

    Returns:
        List of metric results
    """
    loader = TextDataLoader(
        text_column=text_column, token_column=token_column, tokenizer=tokenizer
    )
    processor = TextBatchProcessor(analyzer, data_loader=loader, batch_size=batch_size)

    source = {"name": dataset_name, "config": config_name, "split": split}

    return list(processor.process_from_source(source, "dataset"))
