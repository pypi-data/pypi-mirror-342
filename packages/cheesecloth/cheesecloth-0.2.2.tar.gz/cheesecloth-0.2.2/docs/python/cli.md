# Cheesecloth Command-Line Interface

Cheesecloth provides a powerful command-line interface (CLI) for analyzing text data from various sources, including local files, compressed JSONL files, and Hugging Face datasets.

## Installation

The CLI is included with the Cheesecloth Python package:

```bash
pip install cheesecloth
```

## Basic Usage

The basic syntax for the CLI is:

```bash
python -m cheesecloth.cli [SOURCE] [OPTIONS]
```

Where `SOURCE` can be:
- A local file path (`.txt`, `.json`, `.jsonl`, or compressed versions)
- A Hugging Face dataset name (e.g., `imdb`)
- A URL to a remote file

## Examples

### Analyzing a Local File

```bash
# Analyze a plain text file
python -m cheesecloth.cli data/sample.txt

# Analyze a JSONL file with a specific text field
python -m cheesecloth.cli data/documents.jsonl --text-column content
```

### Analyzing Compressed Files

```bash
# Analyze a compressed JSONL file (automatic decompression)
python -m cheesecloth.cli data/corpus.jsonl.gz

# Analyze a ZIP archive containing text files
python -m cheesecloth.cli data/texts.zip
```

### Analyzing Hugging Face Datasets

```bash
# Analyze the IMDB dataset (default split: 'train')
python -m cheesecloth.cli imdb --text-column text

# Analyze a specific split of a dataset
python -m cheesecloth.cli imdb --split test --text-column text

# Analyze a custom dataset
python -m cheesecloth.cli username/dataset-name --text-column document
```

### Pre-tokenized Data

```bash
# Analyze data with pre-tokenized content
python -m cheesecloth.cli dataset-name --token-field tokens --tokenizer-name gpt2
```

## Command-Line Options

### Input Options

| Option | Description |
|--------|-------------|
| `--text-column TEXT_COLUMN` | Field name containing text to analyze (for JSON/JSONL) |
| `--split SPLIT` | Dataset split to use (for Hugging Face datasets) |
| `--limit LIMIT` | Maximum number of documents to process |
| `--start START` | Index to start processing from |
| `--token-field TOKEN_FIELD` | Field name containing tokens (for pre-tokenized data) |
| `--tokenizer-name TOKENIZER_NAME` | Name or path of tokenizer to use |

### Metrics Selection

| Option | Description |
|--------|-------------|
| `--include-groups GROUPS` | Space-separated list of metric groups to include |
| `--exclude-groups GROUPS` | Space-separated list of metric groups to exclude |
| `--use-hyper` | Use optimized analyzer for faster processing |
| `--use-all-metrics` | Use get_all_metrics for comprehensive analysis |

### Output Options

| Option | Description |
|--------|-------------|
| `--output OUTPUT` | Output file path (default: derived from input) |
| `--format FORMAT` | Output format: jsonl, csv, or tsv (default: jsonl) |
| `--pretty` | Pretty-print JSON output |
| `--include-text` | Include original text in output (warning: large output) |
| `--quiet` | Suppress progress output |

## Metric Groups

You can select specific metric groups to include or exclude:

```bash
# Include only basic and entropy metrics
python -m cheesecloth.cli data.jsonl --include-groups basic entropy

# Include all metrics except frequency (which can be large)
python -m cheesecloth.cli data.jsonl --exclude-groups frequency
```

Available metric groups:

| Group | Description |
|-------|-------------|
| `basic` | Character count and word count |
| `char_type` | Letter, digit, punctuation, symbol, whitespace counts |
| `ratios` | ASCII ratio, uppercase ratio, whitespace ratio, etc. |
| `entropy` | Character and unigram entropy |
| `segmentation` | Line and paragraph counts and lengths |
| `frequency` | Character and unicode category frequencies |
| `unigram` | Word-level metrics (count, unique, TTR, etc.) |
| `all` | All available metrics (default) |

## Optimized Processing

For faster processing, especially with large files:

```bash
# Use the HyperAnalyzer for optimized processing
python -m cheesecloth.cli data/large-corpus.jsonl.gz --use-hyper

# Use get_all_metrics for comprehensive analysis
python -m cheesecloth.cli data/large-corpus.jsonl.gz --use-all-metrics
```

## Output Format

The CLI outputs a JSONL file by default, containing:

1. A metadata record with information about the dataset and metrics
2. Individual example records with metrics for each document
3. A summary record with aggregated statistics across all documents

Example of the output structure:

```json
{"type": "metadata", "source": "data.jsonl", "timestamp": "2025-04-19T15:32:10", "metrics": ["char_count", "token_count", ...]}
{"type": "example", "id": 0, "metrics": {"char_count": 1250, "token_count": 235, ...}}
{"type": "example", "id": 1, "metrics": {"char_count": 825, "token_count": 154, ...}}
...
{"type": "summary", "count": 100, "metrics": {"char_count": {"mean": 1050.5, "min": 120, "max": 5230, ...}}}
```

You can change the output format:

```bash
# Output as CSV (good for spreadsheet analysis)
python -m cheesecloth.cli data.jsonl --format csv --output results.csv

# Output as TSV (tab-separated values)
python -m cheesecloth.cli data.jsonl --format tsv
```

## Advanced Usage

### Parallel Processing

For very large datasets, you can split processing across multiple runs:

```bash
# Process the first 1000 documents
python -m cheesecloth.cli large-corpus.jsonl --limit 1000 --output part1.jsonl

# Process the next 1000 documents
python -m cheesecloth.cli large-corpus.jsonl --start 1000 --limit 1000 --output part2.jsonl
```

### Using with Pre-tokenized Data

Many ML datasets come with pre-tokenized text, which Cheesecloth can analyze efficiently:

```bash
python -m cheesecloth.cli dataset-name \
    --token-field tokens \
    --tokenizer-name gpt2 \
    --include-groups unigram frequency
```

### Pipeline Integration

The CLI can be integrated into data processing pipelines:

```bash
# Process a dataset and pipe to jq for filtering
python -m cheesecloth.cli dataset.jsonl | jq 'select(.metrics.char_entropy > 4.0)'

# Process with custom metrics and send to another tool
python -m cheesecloth.cli dataset.jsonl --include-groups basic unigram | \
    custom-processor --input - --output processed.jsonl
```

## Handling Large Files

For extremely large files, consider:

1. Using `--limit` to process manageable chunks
2. Using `--use-hyper` for optimized processing
3. Excluding large metric groups like frequency: `--exclude-groups frequency`
4. Processing in parallel across multiple machines

## Troubleshooting

If you encounter issues:

- **Memory errors**: Try reducing batch size or using `--limit`
- **Slow processing**: Use `--use-hyper` flag and exclude unnecessary metrics
- **File format errors**: Check if the input format matches what you specified
- **Missing metrics**: Ensure you haven't excluded the metric group you need
- **Tokenization errors**: Check if the tokenizer path is correct