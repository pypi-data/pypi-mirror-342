# Advanced Usage of Cheesecloth in Python

This guide covers advanced usage patterns and techniques for getting the most out of Cheesecloth in your Python projects.

## Type-Safe Metrics Classes

Cheesecloth provides type-safe wrapper classes that offer attribute access, proper typing, and helper methods for metrics.

```python
from cheesecloth.tokenized_metrics import AllMetrics, CharMetrics, UnigramMetrics, PatternMetrics, SegmentationMetrics

# Get metrics dictionary and convert to typed object
char_metrics_dict = cheesecloth.get_all_char_metrics("Hello, world!")
char_metrics = CharMetrics.from_dict(char_metrics_dict)

# Now use attribute access and helper methods
print(f"ASCII ratio: {char_metrics.ascii_ratio}")
print(f"Is mostly ASCII: {char_metrics.is_mostly_ascii}")
print(f"Has high entropy: {char_metrics.has_high_entropy}")
```

### Available Wrapper Classes

1. **CharMetrics**: Character-level metrics
2. **UnigramMetrics**: Word-level metrics
3. **PatternMetrics**: Content pattern metrics
4. **SegmentationMetrics**: Document structure metrics
5. **AllMetrics**: Comprehensive wrapper for all metrics categories

### Convenience Methods

Each wrapper class provides convenience methods for common analyses:

```python
all_metrics_dict = cheesecloth.get_all_metrics(text)
metrics = AllMetrics.from_dict(all_metrics_dict)

# Calculate readability score
readability_score = metrics.calculate_readability_score()
readability_level = metrics.get_readability_level()

# Get detailed assessment with contributing factors
readability = metrics.get_readability_assessment()
word_complexity = readability['factors']['word_complexity']['raw_value']
sentence_complexity = readability['factors']['sentence_complexity']['raw_value']

# Get a high-level summary
summary = metrics.summary()
```

## Efficient Processing with HyperAnalyzer

The `HyperAnalyzer` class provides optimized computation of all metrics in a single pass:

```python
from cheesecloth import HyperAnalyzer

# Create analyzer with desired parameters
analyzer = HyperAnalyzer(include_punctuation=True, case_sensitive=False)

# Process a single text
metrics = analyzer.calculate_all_metrics(text)

# Process a batch of texts efficiently
texts = ["First example", "Second example", "Third example"]
batch_results = analyzer.calculate_batch_metrics(texts)
```

## Processing Large Datasets

For large datasets, Cheesecloth provides specialized tools:

```python
from cheesecloth import TextDataLoader, TextBatchProcessor

# Create a data loader for a JSONL file
loader = TextDataLoader("data/corpus.jsonl.gz", text_field="content")

# Create a batch processor with appropriate batch size
processor = TextBatchProcessor(
    loader, 
    batch_size=100,
    include_char_metrics=True,
    include_unigram_metrics=True,
    include_punctuation=False,
    case_sensitive=False
)

# Process the entire dataset with progress tracking
results = []
for i, batch_results in enumerate(processor.process()):
    results.extend(batch_results)
    print(f"Processed batch {i+1}: {len(batch_results)} documents")

print(f"Total documents processed: {len(results)}")
```

## Integration with ML Tokenizers

Cheesecloth supports analysis with machine learning tokenizers:

```python
# Tokenize text with a specific tokenizer
tokens = cheesecloth.tokenize_ml(text, tokenizer_path="gpt2")

# Batch tokenize multiple texts
texts = ["First example", "Second example", "Third example"]
batch_tokens = cheesecloth.batch_tokenize_ml(texts, tokenizer_path="gpt2")

# Get comprehensive token metrics
token_metrics = cheesecloth.get_token_metrics(text, tokenizer_path="gpt2")
```

### Using Custom Tokenizers

```python
from cheesecloth import TokenizerWrapper

# Create a tokenizer wrapper with a local or HF tokenizer
tokenizer_wrapper = TokenizerWrapper("gpt2")

# Process pre-tokenized text
tokenized_text = tokenizer_wrapper.tokenize("Hello, world!")
metrics = cheesecloth.process_tokenized_text(
    "Hello, world!", 
    tokenized_text,
    include_token_metrics=True,
    include_unigram_metrics=True
)
```

## Working with Tokenized Data

For pre-tokenized data (common in ML datasets):

```python
from cheesecloth import TokenizedAnalyzer

# Create a tokenized analyzer
analyzer = TokenizedAnalyzer(include_punctuation=False, case_sensitive=True)

# Calculate metrics for text and token pairs
metrics = analyzer.calculate_metrics(text, token_ids)

# Process a batch efficiently
batch_metrics = analyzer.calculate_batch_metrics(texts, batch_token_ids)
```

## Custom Analysis Pipelines

Build custom analysis pipelines with Cheesecloth's modular functions:

```python
def custom_analysis_pipeline(text):
    """Custom analysis pipeline focused on readability."""
    # Get character statistics
    char_metrics = cheesecloth.get_all_char_metrics(text)
    
    # Get unigram statistics
    unigram_metrics = cheesecloth.get_all_unigram_metrics(
        text, include_punctuation=False, case_sensitive=False
    )
    
    # Get segmentation metrics
    lines = text.split('\n')
    line_count = len(lines)
    avg_line_len = sum(len(line) for line in lines) / max(line_count, 1)
    
    # Calculate composite metrics
    readability_score = (
        0.4 * unigram_metrics["type_token_ratio"] +
        0.3 * (1.0 - unigram_metrics["short_token_ratio"]) +
        0.3 * (1.0 - char_metrics["ratio_punctuation"])
    )
    
    return {
        "readability_score": readability_score,
        "lexical_diversity": unigram_metrics["type_token_ratio"],
        "avg_line_length": avg_line_len,
        "char_entropy": char_metrics["char_entropy"],
        "token_entropy": unigram_metrics["token_entropy"],
    }
```

## Extending Cheesecloth

While Cheesecloth's core is implemented in Rust for performance, you can easily extend it with Python:

```python
def calculate_reading_time(text, words_per_minute=200):
    """Estimate reading time based on word count."""
    word_count = cheesecloth.count_unigram_tokens(text, include_punctuation=False)
    minutes = word_count / words_per_minute
    return {
        "word_count": word_count,
        "reading_time_minutes": minutes,
        "reading_time_formatted": f"{int(minutes)}:{int((minutes % 1) * 60):02d}"
    }

# Use your extension with Cheesecloth
text = "A long article that would take some time to read..."
char_metrics = cheesecloth.get_all_char_metrics(text)
reading_metrics = calculate_reading_time(text)

print(f"Character count: {char_metrics['char_count']}")
print(f"Reading time: {reading_metrics['reading_time_formatted']}")
```

## Visualizing Metrics

While Cheesecloth focuses on computation rather than visualization, you can easily use the results with visualization libraries:

```python
import matplotlib.pyplot as plt
import numpy as np

# Analyze multiple texts
texts = [text1, text2, text3, text4, text5]
results = [cheesecloth.get_all_metrics(t) for t in texts]

# Extract specific metrics for comparison
ttr_values = [r["unigram"]["type_token_ratio"] for r in results]
entropy_values = [r["character"]["char_entropy"] for r in results]
compression_values = [r["compression"]["compression_ratio"] for r in results]

# Create visualization
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(texts))
width = 0.25

ax.bar(x - width, ttr_values, width, label='Type-Token Ratio')
ax.bar(x, entropy_values, width, label='Character Entropy')
ax.bar(x + width, compression_values, width, label='Compression Ratio')

ax.set_ylabel('Value')
ax.set_title('Text Quality Metrics Comparison')
ax.set_xticks(x)
ax.set_xticklabels([f'Text {i+1}' for i in range(len(texts))])
ax.legend()

plt.tight_layout()
plt.show()
```

## Performance Tips

1. **Use Batch Processing**: Always process multiple texts in batches rather than one at a time.
2. **Use the HyperAnalyzer**: For comprehensive metrics, `HyperAnalyzer` is much faster than calling individual functions.
3. **Minimize Python ↔ Rust Transitions**: Calculate all needed metrics in a single call rather than multiple separate calls.
4. **Reuse Tokenized Results**: If you need multiple metrics on the same text, tokenize once and reuse the tokens.
5. **Memory Management**: For very large texts, consider using the pattern-based processing with paragraph segmentation.
6. **Parallel Processing**: For large datasets, use Python's multiprocessing with multiple instances of Cheesecloth.