# Cheesecloth

[![PyPI version](https://badge.fury.io/py/cheesecloth.svg)](https://pypi.org/project/cheesecloth/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A high-performance, Rust-powered text analysis toolkit for corpus filtering and quality assessment.**

Cheesecloth provides 100+ text metrics for:
- ⚡ Low-latency filtering of LLM pretraining datasets
- 📊 Empirical research on text quality and characteristics
- 🔍 Advanced statistical text analysis

[Installation](#installation) | [Quick Examples](#quick-examples) | [Complete Metrics](#metrics-overview) | [CLI Usage](#cli-usage) | [Documentation](#documentation)

## Installation

```bash
pip install cheesecloth
```

## Quick Examples

```python
import cheesecloth

# Basic character analysis
text = "The quick brown fox jumps over the lazy dog!"
metrics = cheesecloth.get_all_char_metrics(text)
print(f"Character count: {metrics['char_count']}")  # 44
print(f"Letters: {metrics['letter_count']}")        # 35
print(f"ASCII ratio: {metrics['ascii_ratio']:.2f}") # 1.00

# Comprehensive analysis (all metrics at once)
all_metrics = cheesecloth.get_all_metrics(text)
print(f"Questions: {all_metrics['patterns']['question_count']}")            # 0
print(f"Paragraphs: {all_metrics['segmentation']['paragraph_count']}")      # 1
print(f"Type-token ratio: {all_metrics['unigram']['type_token_ratio']:.2f}") # 0.56
```

## Metrics Overview

Cheesecloth implements 100+ text analysis metrics across categories:

| Category | Description | Examples |
|----------|-------------|----------|
| **Character** | Character-level counts and distributions | char_count, letter_count, ascii_ratio, char_entropy |
| **Segmentation** | Text structure analysis | paragraph_count, line_count, average_sentence_length |
| **Unigram** | Word-level statistics | token_count, type_token_ratio, hapax_legomena_ratio |
| **Pattern** | Specific content patterns | question_count, copyright_mention_count, contains_code |
| **Compression** | Information density measures | compression_ratio, compression_efficiency |
| **Distribution** | Statistical distributions | zipf_fitness_score, burstiness, vocab_growth |
| **Tokenizer** | ML tokenization analysis | subword_token_count, subword_efficiency |
| **Readability** | Text complexity metrics | readability_score, readability_level |

For a complete list of all implemented metrics with detailed descriptions, see our [Metrics Reference](https://github.com/alea-institute/cheesecloth/blob/main/METRICS.md).

## Development Roadmap

Cheesecloth follows a phased development approach:

### Phase 1 (Complete) - Metrics Implementation ✅
- Comprehensive suite of 100+ text metrics 
- High-performance Rust core with Python bindings
- CLI tools for dataset analysis

### Phase 2 (In Progress) - Statistical Research 🔬
- Empirical baselines from 1T token sample (KL3M Data Project)
- Statistical patterns between metrics and content quality
- Research publication (see [citation](#citation))

### Phase 3 (Pending) - Production Filters 🔄
- Configurable filtering pipelines based on Phase 2 findings
- Adaptive filtering for streaming data
- Production tools for large-scale corpus management

## Key Features

- **Rust Core**: High-performance algorithms implemented in Rust
- **Comprehensive Analysis**: 100+ metrics from basic to advanced statistical measures
- **Type-Safe Interface**: Python classes with IDE completion and convenience methods
- **LLM Integration**: Support for ML tokenizers (GPT, BERT, etc.)
- **Statistical Tools**: Analyze metric distributions across corpus samples
- **Minimal Dependencies**: Lightweight with optional integrations
- **Adaptive Processing**: Smart segmentation for large documents

## Advanced Examples

### Typed Metrics Interface

```python
import cheesecloth
from cheesecloth.tokenized_metrics import AllMetrics

text = """
Copyright © 2025 ALEA Institute. All rights reserved.

Section 1: Introduction to Natural Language Processing

What are the fundamental challenges in processing human language?
"""

# Get all metrics with typesafe interface
metrics_dict = cheesecloth.get_all_metrics(text)
metrics = AllMetrics.from_dict(metrics_dict)

# Proper type safety and attribute access
print(f"Character count: {metrics.character.char_count}")          # 174
print(f"Has copyright notices: {metrics.patterns.has_copyright_notices}")  # True
print(f"Is educational content: {metrics.patterns.is_educational}")        # True
print(f"Question count: {metrics.patterns.question_count}")                # 1
```

### Advanced Statistical Analysis

```python
import cheesecloth

text = """Natural language processing (NLP) is a subfield of linguistics, computer 
science, and artificial intelligence concerned with the interactions between 
computers and human language. The goal is to enable computers to process 
and analyze large amounts of natural language data."""

# Check Zipf's law fitness (how well word frequency follows Zipf's distribution)
zipf_metrics = cheesecloth.get_zipf_metrics(text, include_punctuation=False, case_sensitive=False)
print(f"Zipf fitness score: {zipf_metrics['zipf_fitness_score']:.2f}")  # ~0.39

# Compression-based metrics (measures text complexity/redundancy)
compression_metrics = cheesecloth.get_compression_metrics(text)
print(f"Compression ratio: {compression_metrics['compression_ratio']:.2f}")  # ~1.59
```

## CLI Usage

Analyze files and datasets with the CLI:

```bash
# Analyze a local file
python -m cheesecloth.cli data/war_and_peace.txt

# Hugging Face dataset with text in 'text' column
python -m cheesecloth.cli imdb --text-column text --limit 100

# Specific metric groups only
python -m cheesecloth.cli data/corpus.jsonl.gz --include-groups basic entropy
```

The CLI supports:
- Local text, JSON, and JSONL files (compressed or uncompressed)
- Hugging Face datasets
- Pre-tokenized data with custom tokenizers
- Filtering by metric groups
- Comprehensive or targeted analysis

## Documentation

- [Complete Metrics Reference](https://github.com/alea-institute/cheesecloth/blob/main/METRICS.md)
- [Development Guide](https://github.com/alea-institute/cheesecloth/blob/main/DEVELOPING.md)
- [Changelog](https://github.com/alea-institute/cheesecloth/blob/main/CHANGELOG.md)

## Citation

If you use Cheesecloth in your research, please cite the KL3M Data Project:

```bibtex
@misc{bommarito2025kl3mdata,
  title={The KL3M Data Project: Copyright-Clean Training Resources for Large Language Models},
  author={Bommarito II, Michael J. and Bommarito, Jillian and Katz, Daniel Martin},
  year={2025},
  eprint={2504.07854},
  archivePrefix={arXiv},
  primaryClass={cs.CL}
}
```

## About

Cheesecloth is an [ALEA Institute](https://aleainstitute.ai) project and part of our ongoing research into the development of legal, ethical, and sustainable AI systems.

Licensed under MIT License.