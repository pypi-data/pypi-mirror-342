//! # Batch Text Metrics Processing
//!
//! This module provides functionality for computing text metrics efficiently across
//! batches of documents, with selective calculation of metrics for performance optimization.
//!
//! ## Key Features
//!
//! * Configurable metric selection to compute only what's needed
//! * Batch processing for efficient handling of multiple documents
//! * PyO3 integration for seamless Python interoperability
//! * Concise API for selective metric computation
//!
//! The BatchProcessor enables selective computation of text metrics, making it
//! ideal for processing large corpora where only specific metrics are needed.
//! It balances flexibility with performance to provide efficient text analysis
//! at scale.

use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use std::collections::{HashMap, HashSet};

use crate::char;
use crate::text;
use crate::unigram;

/// A struct that holds configuration for batch metric computation
#[pyclass]
pub struct BatchProcessor {
    #[pyo3(get)]
    enabled_metrics: HashSet<String>,
    include_punctuation: bool,
    case_sensitive: bool,
}

#[pymethods]
impl BatchProcessor {
    /// Create a new BatchProcessor with specified metrics enabled
    #[new]
    fn new(metrics: Vec<String>, include_punctuation: bool, case_sensitive: bool) -> Self {
        BatchProcessor {
            enabled_metrics: metrics.into_iter().collect(),
            include_punctuation,
            case_sensitive,
        }
    }

    /// Compute all enabled metrics for a single text
    fn compute_metrics(&self, py: Python<'_>, text: &str) -> PyResult<PyObject> {
        let metrics = self.compute_metrics_internal(text);

        // Convert to Python dictionary
        let dict = PyDict::new(py);
        for (key, value) in metrics {
            match value {
                MetricValue::Int(v) => dict.set_item(key, v)?,
                MetricValue::Float(v) => dict.set_item(key, v)?,
                MetricValue::Bool(v) => dict.set_item(key, v)?,
                MetricValue::StringMap(map) => {
                    let inner_dict = PyDict::new(py);
                    for (k, v) in map {
                        inner_dict.set_item(k, v)?;
                    }
                    dict.set_item(key, inner_dict)?;
                }
                MetricValue::StringMap3(map) => {
                    let inner_dict = PyDict::new(py);
                    for ((prev, current, next), v) in map {
                        // Convert the tuple key to a string representation for Python
                        let start_str = "START".to_string();
                        let end_str = "END".to_string();
                        let prev_str = prev.as_ref().unwrap_or(&start_str);
                        let next_str = next.as_ref().unwrap_or(&end_str);
                        let key_str = format!("({},{},{})", prev_str, current, next_str);
                        inner_dict.set_item(key_str, v)?;
                    }
                    dict.set_item(key, inner_dict)?;
                }
            }
        }

        Ok(dict.into())
    }

    /// Compute metrics for a batch of texts
    fn compute_batch_metrics(&self, py: Python<'_>, texts: Vec<String>) -> PyResult<PyObject> {
        let results: Vec<HashMap<String, MetricValue>> = texts
            .iter()
            .map(|text| self.compute_metrics_internal(text))
            .collect();

        // Convert results to a list of dictionaries
        let result_list = PyList::empty(py);

        for metrics in results {
            let dict = PyDict::new(py);
            for (key, value) in metrics {
                match value {
                    MetricValue::Int(v) => dict.set_item(&key, v)?,
                    MetricValue::Float(v) => dict.set_item(&key, v)?,
                    MetricValue::Bool(v) => dict.set_item(&key, v)?,
                    MetricValue::StringMap(map) => {
                        let inner_dict = PyDict::new(py);
                        for (k, v) in map {
                            inner_dict.set_item(k, v)?;
                        }
                        dict.set_item(&key, inner_dict)?;
                    }
                    MetricValue::StringMap3(map) => {
                        let inner_dict = PyDict::new(py);
                        for ((prev, current, next), v) in map {
                            // Convert the tuple key to a string representation for Python
                            let start_str = "START".to_string();
                            let end_str = "END".to_string();
                            let prev_str = prev.as_ref().unwrap_or(&start_str);
                            let next_str = next.as_ref().unwrap_or(&end_str);
                            let key_str = format!("({},{},{})", prev_str, current, next_str);
                            inner_dict.set_item(key_str, v)?;
                        }
                        dict.set_item(&key, inner_dict)?;
                    }
                }
            }
            result_list.append(dict)?;
        }

        Ok(result_list.into())
    }
}

/// Internal enum to represent different metric value types
enum MetricValue {
    Int(usize),
    Float(f64),
    Bool(bool),
    StringMap(HashMap<String, usize>),
    StringMap3(HashMap<(Option<String>, String, Option<String>), usize>),
}

impl BatchProcessor {
    /// Internal function to compute all metrics for a text
    fn compute_metrics_internal(&self, text: &str) -> HashMap<String, MetricValue> {
        let mut results = HashMap::new();

        // Basic metrics
        if self.enabled_metrics.contains("char_count") {
            results.insert(
                "char_count".to_string(),
                MetricValue::Int(char::unicode::count_chars(text)),
            );
        }

        if self.enabled_metrics.contains("word_count") {
            results.insert(
                "word_count".to_string(),
                MetricValue::Int(text::segmentation::count_words(text)),
            );
        }

        // Character type metrics
        if self.enabled_metrics.contains("letter_count") {
            results.insert(
                "letter_count".to_string(),
                MetricValue::Int(char::unicode::count_letters(text)),
            );
        }

        if self.enabled_metrics.contains("digit_count") {
            results.insert(
                "digit_count".to_string(),
                MetricValue::Int(char::unicode::count_digits(text)),
            );
        }

        if self.enabled_metrics.contains("punctuation_count") {
            results.insert(
                "punctuation_count".to_string(),
                MetricValue::Int(char::unicode::count_punctuation(text)),
            );
        }

        if self.enabled_metrics.contains("symbol_count") {
            results.insert(
                "symbol_count".to_string(),
                MetricValue::Int(char::unicode::count_symbols(text)),
            );
        }

        if self.enabled_metrics.contains("whitespace_count") {
            results.insert(
                "whitespace_count".to_string(),
                MetricValue::Int(char::unicode::count_whitespace(text)),
            );
        }

        if self.enabled_metrics.contains("non_ascii_count") {
            results.insert(
                "non_ascii_count".to_string(),
                MetricValue::Int(char::unicode::count_non_ascii(text)),
            );
        }

        if self.enabled_metrics.contains("uppercase_count") {
            results.insert(
                "uppercase_count".to_string(),
                MetricValue::Int(char::unicode::count_uppercase(text)),
            );
        }

        if self.enabled_metrics.contains("lowercase_count") {
            results.insert(
                "lowercase_count".to_string(),
                MetricValue::Int(char::unicode::count_lowercase(text)),
            );
        }

        if self.enabled_metrics.contains("alphanumeric_count") {
            results.insert(
                "alphanumeric_count".to_string(),
                MetricValue::Int(char::unicode::count_alphanumeric(text)),
            );
        }

        // Ratio metrics
        if self.enabled_metrics.contains("is_ascii") {
            results.insert(
                "is_ascii".to_string(),
                MetricValue::Bool(char::unicode::is_ascii(text)),
            );
        }

        if self.enabled_metrics.contains("ascii_ratio") {
            results.insert(
                "ascii_ratio".to_string(),
                MetricValue::Float(char::unicode::ratio_ascii(text)),
            );
        }

        if self.enabled_metrics.contains("uppercase_ratio") {
            results.insert(
                "uppercase_ratio".to_string(),
                MetricValue::Float(char::unicode::ratio_uppercase(text)),
            );
        }

        if self.enabled_metrics.contains("alphanumeric_ratio") {
            results.insert(
                "alphanumeric_ratio".to_string(),
                MetricValue::Float(char::unicode::ratio_alphanumeric(text)),
            );
        }

        if self.enabled_metrics.contains("alpha_to_numeric_ratio") {
            results.insert(
                "alpha_to_numeric_ratio".to_string(),
                MetricValue::Float(char::unicode::ratio_alpha_to_numeric(text)),
            );
        }

        if self.enabled_metrics.contains("whitespace_ratio") {
            results.insert(
                "whitespace_ratio".to_string(),
                MetricValue::Float(char::unicode::ratio_whitespace(text)),
            );
        }

        if self.enabled_metrics.contains("digit_ratio") {
            results.insert(
                "digit_ratio".to_string(),
                MetricValue::Float(char::unicode::ratio_digits(text)),
            );
        }

        if self.enabled_metrics.contains("punctuation_ratio") {
            results.insert(
                "punctuation_ratio".to_string(),
                MetricValue::Float(char::unicode::ratio_punctuation(text)),
            );
        }

        // Entropy metrics
        if self.enabled_metrics.contains("char_entropy") {
            results.insert(
                "char_entropy".to_string(),
                MetricValue::Float(char::unicode::char_entropy(text)),
            );
        }

        // Frequency metrics
        if self.enabled_metrics.contains("char_frequency") {
            let freq = char::unicode::char_frequency(text);
            // Convert char keys to string
            let string_freq: HashMap<String, usize> =
                freq.into_iter().map(|(k, v)| (k.to_string(), v)).collect();
            results.insert(
                "char_frequency".to_string(),
                MetricValue::StringMap(string_freq),
            );
        }

        if self.enabled_metrics.contains("char_type_frequency") {
            let freq = char::unicode::char_type_frequency(text);
            let string_freq: HashMap<String, usize> =
                freq.into_iter().map(|(k, v)| (k.to_string(), v)).collect();
            results.insert(
                "char_type_frequency".to_string(),
                MetricValue::StringMap(string_freq),
            );
        }

        if self.enabled_metrics.contains("unicode_category_frequency") {
            results.insert(
                "unicode_category_frequency".to_string(),
                MetricValue::StringMap(char::categories::category_string_frequency(text)),
            );
        }

        if self
            .enabled_metrics
            .contains("unicode_category_group_frequency")
        {
            results.insert(
                "unicode_category_group_frequency".to_string(),
                MetricValue::StringMap(char::categories::category_group_string_frequency(text)),
            );
        }

        if self
            .enabled_metrics
            .contains("unicode_category_trigram_frequency")
        {
            results.insert(
                "unicode_category_trigram_frequency".to_string(),
                MetricValue::StringMap3(char::categories::count_category_trigrams(text)),
            );
        }

        if self
            .enabled_metrics
            .contains("unicode_category_group_trigram_frequency")
        {
            results.insert(
                "unicode_category_group_trigram_frequency".to_string(),
                MetricValue::StringMap3(char::categories::count_category_group_trigrams(text)),
            );
        }

        // Segmentation metrics
        if self.enabled_metrics.contains("line_count") {
            results.insert(
                "line_count".to_string(),
                MetricValue::Int(text::segmentation::count_lines(text)),
            );
        }

        if self.enabled_metrics.contains("avg_line_length") {
            results.insert(
                "avg_line_length".to_string(),
                MetricValue::Float(text::segmentation::average_line_length(text)),
            );
        }

        if self.enabled_metrics.contains("paragraph_count") {
            results.insert(
                "paragraph_count".to_string(),
                MetricValue::Int(text::segmentation::count_paragraphs(text)),
            );
        }

        if self.enabled_metrics.contains("avg_paragraph_length") {
            results.insert(
                "avg_paragraph_length".to_string(),
                MetricValue::Float(text::segmentation::average_paragraph_length(text)),
            );
        }

        if self.enabled_metrics.contains("avg_word_length") {
            results.insert(
                "avg_word_length".to_string(),
                MetricValue::Float(text::segmentation::average_word_length(text)),
            );
        }

        if self.enabled_metrics.contains("avg_sentence_length") {
            results.insert(
                "avg_sentence_length".to_string(),
                MetricValue::Float(text::segmentation::average_sentence_length(text)),
            );
        }

        // Unigram metrics
        if self.enabled_metrics.contains("unigram_count") {
            results.insert(
                "unigram_count".to_string(),
                MetricValue::Int(unigram::count_tokens(text, self.include_punctuation)),
            );
        }

        if self.enabled_metrics.contains("unique_unigram_count") {
            results.insert(
                "unique_unigram_count".to_string(),
                MetricValue::Int(unigram::count_unique_tokens(
                    text,
                    self.include_punctuation,
                    self.case_sensitive,
                )),
            );
        }

        if self.enabled_metrics.contains("unigram_type_token_ratio") {
            results.insert(
                "unigram_type_token_ratio".to_string(),
                MetricValue::Float(unigram::type_token_ratio(
                    text,
                    self.include_punctuation,
                    self.case_sensitive,
                )),
            );
        }

        if self.enabled_metrics.contains("unigram_repetition_rate") {
            results.insert(
                "unigram_repetition_rate".to_string(),
                MetricValue::Float(unigram::repetition_rate(
                    text,
                    self.include_punctuation,
                    self.case_sensitive,
                )),
            );
        }

        if self.enabled_metrics.contains("unigram_entropy") {
            results.insert(
                "unigram_entropy".to_string(),
                MetricValue::Float(unigram::token_entropy(
                    text,
                    self.include_punctuation,
                    self.case_sensitive,
                )),
            );
        }

        if self.enabled_metrics.contains("unigram_frequency") {
            results.insert(
                "unigram_frequency".to_string(),
                MetricValue::StringMap(unigram::token_frequency(
                    text,
                    self.include_punctuation,
                    self.case_sensitive,
                )),
            );
        }

        results
    }
}
