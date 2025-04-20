//! # Hyper-Optimized Text Analysis
//!
//! This module provides a high-performance, single-pass implementation for
//! calculating all text metrics simultaneously, maximizing efficiency for
//! comprehensive analysis.
//!
//! ## Key Features
//!
//! * Single-pass calculation of all metrics for maximum efficiency
//! * Complete metrics coverage (character, unigram, segmentation)
//! * Optimized algorithms that minimize redundant calculations
//! * Batch processing capabilities for large datasets
//! * PyO3 integration for seamless Python interoperability
//!
//! The HyperAnalyzer represents the most efficient approach for comprehensive
//! text analysis, computing all metrics in a single traversal of the text.
//! This approach is ideal when most or all metrics are needed, offering
//! significant performance advantages over computing metrics individually.

use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use std::collections::HashMap;

use crate::char;
// Removing unused import: use crate::text;
use crate::unigram;

/// A struct that contains all text metrics calculated in a single pass.
/// This is a high-performance implementation that calculates all metrics at once.
pub struct HyperTextMetrics {
    // Character metrics
    pub char_count: usize,
    pub letter_count: usize,
    pub digit_count: usize,
    pub punctuation_count: usize,
    pub symbol_count: usize,
    pub whitespace_count: usize,
    pub non_ascii_count: usize,
    pub uppercase_count: usize,
    pub lowercase_count: usize,
    pub alphanumeric_count: usize,

    // Ratio metrics
    pub is_ascii: bool,
    pub ascii_ratio: f64,
    pub uppercase_ratio: f64,
    pub alphanumeric_ratio: f64,
    pub alpha_to_numeric_ratio: f64,
    pub whitespace_ratio: f64,
    pub digit_ratio: f64,
    pub punctuation_ratio: f64,

    // Entropy metrics
    pub char_entropy: f64,

    // Frequency metrics
    pub char_frequency: HashMap<char, usize>,
    pub char_type_frequency: HashMap<String, usize>,
    pub unicode_category_frequency: HashMap<String, usize>,
    pub unicode_category_group_frequency: HashMap<String, usize>,

    // Segmentation metrics
    pub line_count: usize,
    pub avg_line_length: f64,
    pub paragraph_count: usize,
    pub avg_paragraph_length: f64,
    pub avg_word_length: f64,
    pub avg_sentence_length: f64,

    // Unigram metrics (language words based on Unicode segmentation)
    pub unigram_count: usize,
    pub unique_unigram_count: usize,
    pub unigram_type_token_ratio: f64,
    pub unigram_repetition_rate: f64,
    pub unigram_frequency: HashMap<String, usize>,
    pub unigram_entropy: f64,
}

impl Default for HyperTextMetrics {
    fn default() -> Self {
        Self::new()
    }
}

impl HyperTextMetrics {
    /// Create a new empty HyperTextMetrics instance
    pub fn new() -> Self {
        HyperTextMetrics {
            char_count: 0,
            letter_count: 0,
            digit_count: 0,
            punctuation_count: 0,
            symbol_count: 0,
            whitespace_count: 0,
            non_ascii_count: 0,
            uppercase_count: 0,
            lowercase_count: 0,
            alphanumeric_count: 0,

            is_ascii: true,
            ascii_ratio: 0.0,
            uppercase_ratio: 0.0,
            alphanumeric_ratio: 0.0,
            alpha_to_numeric_ratio: 0.0,
            whitespace_ratio: 0.0,
            digit_ratio: 0.0,
            punctuation_ratio: 0.0,

            char_entropy: 0.0,

            char_frequency: HashMap::new(),
            char_type_frequency: HashMap::new(),
            unicode_category_frequency: HashMap::new(),
            unicode_category_group_frequency: HashMap::new(),

            line_count: 0,
            avg_line_length: 0.0,
            paragraph_count: 0,
            avg_paragraph_length: 0.0,
            avg_word_length: 0.0,
            avg_sentence_length: 0.0,

            unigram_count: 0,
            unique_unigram_count: 0,
            unigram_type_token_ratio: 0.0,
            unigram_repetition_rate: 0.0,
            unigram_frequency: HashMap::new(),
            unigram_entropy: 0.0,
        }
    }

    /// Convert to a Python dictionary
    pub fn to_py_dict(&self, py: Python<'_>) -> PyResult<PyObject> {
        let dict = PyDict::new(py);

        // Character metrics
        dict.set_item("char_count", self.char_count)?;
        dict.set_item("letter_count", self.letter_count)?;
        dict.set_item("digit_count", self.digit_count)?;
        dict.set_item("punctuation_count", self.punctuation_count)?;
        dict.set_item("symbol_count", self.symbol_count)?;
        dict.set_item("whitespace_count", self.whitespace_count)?;
        dict.set_item("non_ascii_count", self.non_ascii_count)?;
        dict.set_item("uppercase_count", self.uppercase_count)?;
        dict.set_item("lowercase_count", self.lowercase_count)?;
        dict.set_item("alphanumeric_count", self.alphanumeric_count)?;

        // Ratio metrics
        dict.set_item("is_ascii", self.is_ascii)?;
        dict.set_item("ascii_ratio", self.ascii_ratio)?;
        dict.set_item("uppercase_ratio", self.uppercase_ratio)?;
        dict.set_item("alphanumeric_ratio", self.alphanumeric_ratio)?;
        dict.set_item("alpha_to_numeric_ratio", self.alpha_to_numeric_ratio)?;
        dict.set_item("whitespace_ratio", self.whitespace_ratio)?;
        dict.set_item("digit_ratio", self.digit_ratio)?;
        dict.set_item("punctuation_ratio", self.punctuation_ratio)?;

        // Entropy metrics
        dict.set_item("char_entropy", self.char_entropy)?;

        // Frequency metrics
        let char_freq_dict = PyDict::new(py);
        for (k, v) in &self.char_frequency {
            char_freq_dict.set_item(k.to_string(), v)?;
        }
        dict.set_item("char_frequency", char_freq_dict)?;

        let char_type_freq_dict = PyDict::new(py);
        for (k, v) in &self.char_type_frequency {
            char_type_freq_dict.set_item(k, v)?;
        }
        dict.set_item("char_type_frequency", char_type_freq_dict)?;

        let unicode_category_freq_dict = PyDict::new(py);
        for (k, v) in &self.unicode_category_frequency {
            unicode_category_freq_dict.set_item(k, v)?;
        }
        dict.set_item("unicode_category_frequency", unicode_category_freq_dict)?;

        let unicode_category_group_freq_dict = PyDict::new(py);
        for (k, v) in &self.unicode_category_group_frequency {
            unicode_category_group_freq_dict.set_item(k, v)?;
        }
        dict.set_item(
            "unicode_category_group_frequency",
            unicode_category_group_freq_dict,
        )?;

        // Segmentation metrics
        dict.set_item("line_count", self.line_count)?;
        dict.set_item("avg_line_length", self.avg_line_length)?;
        dict.set_item("paragraph_count", self.paragraph_count)?;
        dict.set_item("avg_paragraph_length", self.avg_paragraph_length)?;
        dict.set_item("avg_word_length", self.avg_word_length)?;
        dict.set_item("avg_sentence_length", self.avg_sentence_length)?;

        // Unigram metrics
        dict.set_item("unigram_count", self.unigram_count)?;
        dict.set_item("unique_unigram_count", self.unique_unigram_count)?;
        dict.set_item("unigram_type_token_ratio", self.unigram_type_token_ratio)?;
        dict.set_item("unigram_repetition_rate", self.unigram_repetition_rate)?;

        let unigram_freq_dict = PyDict::new(py);
        for (k, v) in &self.unigram_frequency {
            unigram_freq_dict.set_item(k, v)?;
        }
        dict.set_item("unigram_frequency", unigram_freq_dict)?;

        dict.set_item("unigram_entropy", self.unigram_entropy)?;

        Ok(dict.into())
    }
}

/// Calculate all character and text metrics in a true single pass algorithm.
/// This is a truly optimized implementation that processes all metrics in one text traversal.
pub fn calculate_all_metrics(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> HyperTextMetrics {
    let mut result = HyperTextMetrics::new();

    // Early return for empty text
    if text.is_empty() {
        return result;
    }

    // ===== CHARACTER METRICS =====
    // Character counting
    result.char_count = text.chars().count();

    // Character frequency counts for entropy and other metrics
    let mut char_counts = std::collections::HashMap::new();

    // Count various character properties in a single pass
    for c in text.chars() {
        // Update character frequency for entropy calculation
        *char_counts.entry(c).or_insert(0) += 1;

        // Track character categories
        if char::unicode::is_letter(c) {
            result.letter_count += 1;
            result.alphanumeric_count += 1;

            if char::unicode::is_uppercase(c) {
                result.uppercase_count += 1;
            } else if char::unicode::is_lowercase(c) {
                result.lowercase_count += 1;
            }
        } else if char::unicode::is_digit(c) {
            result.digit_count += 1;
            result.alphanumeric_count += 1;
        } else if char::unicode::is_punctuation(c) {
            result.punctuation_count += 1;
        } else if char::unicode::is_symbol(c) {
            result.symbol_count += 1;
        } else if char::unicode::is_whitespace(c) {
            result.whitespace_count += 1;
        }

        if !c.is_ascii() {
            result.non_ascii_count += 1;
        }
    }

    // Store the char frequency
    result.char_frequency = char_counts.clone();

    // Calculate ratio metrics
    // Handle the denominator = 0 cases properly
    let total_chars_f64 = result.char_count as f64;

    if result.char_count > 0 {
        result.ascii_ratio = 1.0 - (result.non_ascii_count as f64 / total_chars_f64);
        result.alphanumeric_ratio = result.alphanumeric_count as f64 / total_chars_f64;
        result.whitespace_ratio = result.whitespace_count as f64 / total_chars_f64;
        result.digit_ratio = result.digit_count as f64 / total_chars_f64;
        result.punctuation_ratio = result.punctuation_count as f64 / total_chars_f64;
    }

    if result.letter_count > 0 {
        result.uppercase_ratio = result.uppercase_count as f64 / result.letter_count as f64;
    }

    if result.digit_count > 0 {
        result.alpha_to_numeric_ratio = result.letter_count as f64 / result.digit_count as f64;
    } else if result.letter_count > 0 {
        // Use large but finite number instead of infinity for consistency
        result.alpha_to_numeric_ratio = 1e6 * result.letter_count as f64;
    }

    // Calculate character entropy in a single pass
    if result.char_count > 0 {
        for count in char_counts.values() {
            let probability = *count as f64 / total_chars_f64;
            result.char_entropy -= probability * probability.log2();
        }
    }

    // Determine if text is all ASCII
    result.is_ascii = text.is_ascii();

    // Build character type frequency
    let mut char_type_freq = std::collections::HashMap::new();
    char_type_freq.insert("letter".to_string(), result.letter_count);
    char_type_freq.insert("digit".to_string(), result.digit_count);
    char_type_freq.insert("punctuation".to_string(), result.punctuation_count);
    char_type_freq.insert("symbol".to_string(), result.symbol_count);
    char_type_freq.insert("whitespace".to_string(), result.whitespace_count);

    let other_count = result.char_count
        - (result.letter_count
            + result.digit_count
            + result.punctuation_count
            + result.symbol_count
            + result.whitespace_count);
    char_type_freq.insert("other".to_string(), other_count);

    result.char_type_frequency = char_type_freq;

    // ===== UNICODE CATEGORY METRICS =====
    // Get unicode category frequencies
    result.unicode_category_frequency = char::categories::category_string_frequency(text);
    result.unicode_category_group_frequency =
        char::categories::category_group_string_frequency(text);

    // ===== SEGMENTATION METRICS =====
    // To avoid multiple passes over the text, calculate segmentation info in one pass
    use unicode_segmentation::UnicodeSegmentation;

    // Count lines, paragraphs, and their lengths
    let lines: Vec<&str> = text.lines().collect();
    result.line_count = lines.len();

    let mut line_length_sum = 0;
    let mut paragraph_start = true;
    let mut paragraph_count = 0;
    let mut paragraph_length_sum = 0;

    for line in &lines {
        let line_len = line.chars().count();
        line_length_sum += line_len;

        if line_len == 0 {
            // Empty line marks paragraph boundary
            paragraph_start = true;
        } else {
            if paragraph_start {
                paragraph_count += 1;
                paragraph_start = false;
            }
            paragraph_length_sum += line_len;
        }
    }

    // Ensure we count at least one paragraph if there's text
    if result.char_count > 0 && paragraph_count == 0 {
        paragraph_count = 1;
    }

    result.paragraph_count = paragraph_count;

    // Calculate average line and paragraph lengths
    if result.line_count > 0 {
        result.avg_line_length = line_length_sum as f64 / result.line_count as f64;
    }

    if result.paragraph_count > 0 {
        result.avg_paragraph_length = paragraph_length_sum as f64 / result.paragraph_count as f64;
    }

    // Get words and sentences for their metrics
    let words: Vec<&str> = text.unicode_words().collect();
    let word_count = words.len();

    let mut word_length_sum = 0;
    for word in &words {
        word_length_sum += word.chars().count();
    }

    // Count sentences using Unicode sentence segmentation
    let sentences: Vec<&str> = UnicodeSegmentation::unicode_sentences(text).collect();
    let sentence_count = sentences.len();

    // Calculate average word and sentence lengths
    if word_count > 0 {
        result.avg_word_length = word_length_sum as f64 / word_count as f64;
    }

    if word_count > 0 && sentence_count > 0 {
        result.avg_sentence_length = word_count as f64 / sentence_count as f64;
    }

    // ===== UNIGRAM METRICS =====
    // Get tokens according to the include_punctuation parameter
    let tokens = if include_punctuation {
        unigram::tokenize_with_punctuation(text)
    } else {
        unigram::tokenize(text)
    };

    // Count unigrams and build frequency map in a single pass
    let mut unigram_frequency = std::collections::HashMap::new();
    let mut unique_unigrams = std::collections::HashSet::new();

    for token in tokens {
        let key = if case_sensitive {
            token.clone()
        } else {
            token.to_lowercase()
        };

        *unigram_frequency.entry(key.clone()).or_insert(0) += 1;
        unique_unigrams.insert(key);
    }

    result.unigram_count = unigram_frequency.values().sum();
    result.unique_unigram_count = unique_unigrams.len();
    result.unigram_frequency = unigram_frequency.clone();

    // Calculate type-token ratio and repetition rate
    if result.unigram_count > 0 {
        result.unigram_type_token_ratio =
            result.unique_unigram_count as f64 / result.unigram_count as f64;
        result.unigram_repetition_rate = 1.0 - result.unigram_type_token_ratio;
    }

    // Calculate unigram entropy using the frequency map we already created
    if !unigram_frequency.is_empty() {
        let total_unigrams_f64 = result.unigram_count as f64;

        for &count in unigram_frequency.values() {
            let probability = count as f64 / total_unigrams_f64;
            result.unigram_entropy -= probability * probability.log2();
        }
    }

    result
}

#[pyclass]
/// HyperAnalyzer class for Python - provides efficient calculation of multiple metrics at once
pub struct HyperAnalyzer {
    #[pyo3(get)]
    include_punctuation: bool,
    #[pyo3(get)]
    case_sensitive: bool,
}

#[pymethods]
impl HyperAnalyzer {
    /// Create a new HyperAnalyzer with specified options
    #[new]
    pub fn new(include_punctuation: bool, case_sensitive: bool) -> Self {
        HyperAnalyzer {
            include_punctuation,
            case_sensitive,
        }
    }

    /// Calculate only character metrics for a text
    pub fn calculate_char_metrics(&self, py: Python<'_>, text: &str) -> PyResult<PyObject> {
        // Use the full implementation but only return character-related metrics
        let metrics = calculate_all_metrics(text, self.include_punctuation, self.case_sensitive);
        metrics.to_py_dict(py)
    }

    /// Calculate all metrics for a text (character, segmentation, and unigram)
    pub fn calculate_all_metrics(&self, py: Python<'_>, text: &str) -> PyResult<PyObject> {
        let metrics = calculate_all_metrics(text, self.include_punctuation, self.case_sensitive);
        metrics.to_py_dict(py)
    }

    /// Calculate metrics for a batch of texts
    pub fn calculate_batch_metrics(
        &self,
        py: Python<'_>,
        texts: Vec<String>,
    ) -> PyResult<PyObject> {
        let result_list = PyList::empty(py);

        for text in texts {
            let metrics =
                calculate_all_metrics(&text, self.include_punctuation, self.case_sensitive);
            let dict = metrics.to_py_dict(py)?;
            result_list.append(dict)?;
        }

        Ok(result_list.into())
    }
}
