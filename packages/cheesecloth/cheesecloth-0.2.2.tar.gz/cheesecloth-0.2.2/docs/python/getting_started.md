# Getting Started with Cheesecloth in Python

Cheesecloth provides a comprehensive Python API that makes it easy to analyze text and calculate a wide range of metrics. This guide will help you get started with using Cheesecloth in your Python projects.

## Installation

Install Cheesecloth using pip:

```bash
pip install cheesecloth
```

## Basic Usage

### Importing the Library

```python
import cheesecloth
```

### Character-Level Analysis

To analyze text at the character level:

```python
text = "Hello, world! 123 + πр漢字"

# Get all character metrics at once (most efficient)
char_metrics = cheesecloth.get_all_char_metrics(text)

# Access individual metrics
print(f"Character count: {char_metrics['char_count']}")
print(f"Letters: {char_metrics['letter_count']}")
print(f"Digits: {char_metrics['digit_count']}")
print(f"Symbols: {char_metrics['symbol_count']}")
print(f"Whitespace: {char_metrics['whitespace_count']}")
print(f"ASCII ratio: {char_metrics['ascii_ratio']:.2f}")
print(f"Character entropy: {char_metrics['char_entropy']:.2f}")
```

### Word-Level Analysis

For word-level (unigram) analysis:

```python
# Get all unigram metrics
unigram_metrics = cheesecloth.get_all_unigram_metrics(text, include_punctuation=False, case_sensitive=False)

print(f"Token count: {unigram_metrics['token_count']}")
print(f"Unique token count: {unigram_metrics['unique_token_count']}")
print(f"Type-token ratio: {unigram_metrics['type_token_ratio']:.2f}")
print(f"Token entropy: {unigram_metrics['token_entropy']:.2f}")
```

### Comprehensive Text Analysis

To get all metrics at once:

```python
all_metrics = cheesecloth.get_all_metrics(text)

# Access metrics by category
print(f"Character entropy: {all_metrics['character']['char_entropy']}")
print(f"Type-token ratio: {all_metrics['unigram']['type_token_ratio']}")
print(f"Question count: {all_metrics['patterns']['question_count']}")
print(f"Paragraph count: {all_metrics['segmentation']['paragraph_count']}")
```

## Advanced Features

### Statistical Distributions

```python
# Calculate Zipf's law metrics
zipf_metrics = cheesecloth.get_zipf_metrics(text, include_punctuation=False, case_sensitive=True)
print(f"Zipf fitness score: {zipf_metrics['zipf_fitness_score']}")
print(f"Power law exponent: {zipf_metrics['power_law_exponent']}")

# Compression metrics
compression_metrics = cheesecloth.get_compression_metrics(text)
print(f"Compression ratio: {compression_metrics['compression_ratio']}")
print(f"Normalized compression ratio: {compression_metrics['normalized_compression_ratio']}")
```

### Pattern Detection

```python
# Check for specific content patterns
print(f"Contains code characters: {cheesecloth.contains_code_characters(text)}")
print(f"Copyright mentions: {cheesecloth.count_copyright_mentions(text)}")
print(f"Section headings: {cheesecloth.count_section_strings(text)}")
print(f"Question strings: {cheesecloth.count_question_strings(text)}")
```

### Type-Safe Metrics with Object Interface

For better IDE support and attribute access:

```python
from cheesecloth.tokenized_metrics import AllMetrics, CharMetrics

# Get metrics dictionary
all_metrics_dict = cheesecloth.get_all_metrics(text)

# Convert to typed object
metrics = AllMetrics.from_dict(all_metrics_dict)

# Now use attribute access instead of dictionary keys
print(f"Character count: {metrics.character.char_count}")
print(f"Is mostly ASCII: {metrics.character.is_mostly_ascii}")
print(f"Has copyright notices: {metrics.patterns.has_copyright_notices}")
print(f"Readability level: {metrics.get_readability_level()}")
```

## Using the CLI

Cheesecloth also provides a command-line interface for analyzing text files:

```bash
# Analyze a local file
python -m cheesecloth.cli path/to/file.txt

# Analyze a JSONL.GZ file
python -m cheesecloth.cli data/corpus.jsonl.gz

# Analyze a Hugging Face dataset
python -m cheesecloth.cli imdb --text-column text
```

## Optimizing Performance

### Using the HyperAnalyzer

For the best performance, especially with large texts, use the `HyperAnalyzer`:

```python
analyzer = cheesecloth.HyperAnalyzer(include_punctuation=True, case_sensitive=False)
metrics = analyzer.calculate_all_metrics(text)

# Process a batch of texts efficiently
texts = ["First example.", "Second example with more words.", "Third!"]
batch_results = analyzer.calculate_batch_metrics(texts)
```

### Processing Large Datasets

For large datasets, use the batch processing capabilities:

```python
from cheesecloth import TextBatchProcessor, TextDataLoader

# Create a data loader
loader = TextDataLoader("path/to/dataset.jsonl.gz", text_field="content")

# Create a batch processor
processor = TextBatchProcessor(loader, batch_size=100)

# Process the dataset with progress tracking
for batch_num, result in enumerate(processor.process()):
    print(f"Processed batch {batch_num}: {len(result)} documents")
```

## Integration with ML Tokenizers

Cheesecloth supports analysis of text with machine learning tokenizers:

```python
# Get tokenizer metrics
token_metrics = cheesecloth.get_token_metrics(text, tokenizer_path="gpt2")
print(f"Subword token count: {token_metrics['subword_token_count']}")
print(f"Subword entropy: {token_metrics['subword_entropy']}")
```

## Next Steps

- Check out the [complete examples](../examples/) for more detailed usage patterns
- Read about [all available metrics](../../METRICS.md) in the metrics documentation
- Explore [advanced usage](./advanced_usage.md) for more sophisticated analysis