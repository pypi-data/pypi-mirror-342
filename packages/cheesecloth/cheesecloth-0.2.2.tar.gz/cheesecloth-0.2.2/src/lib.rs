//! # Cheesecloth
//!
//! A high-performance text analysis library for extracting comprehensive metrics
//! from text data. Cheesecloth combines efficient Rust implementations with Python
//! bindings to provide fast analysis of large text corpora.
//!
//! ## Core Features
//!
//! * Character-level analysis: counts, ratios, entropy, Unicode categories
//! * Unigram metrics: tokenization, frequency, diversity measures
//! * Subword/BPE token metrics: for machine learning model tokenizers
//! * Text segmentation: lines, paragraphs, sentences
//! * Information theory: entropy, compression ratios
//! * Statistical patterns: Zipf's law metrics, burstiness, vocabulary growth
//!
//! ## Architecture
//!
//! Cheesecloth is built with a modular design:
//!
//! * Individual low-level metric functions for targeted analysis
//! * BatchProcessor for computing metrics in parallel across large datasets
//! * HyperAnalyzer for efficient single-pass computation of all metrics
//! * Python bindings for seamless integration with data science workflows
//!
//! The library balances performance with usability to enable analysis of
//! large text corpora while maintaining a clear API.

use pyo3::prelude::*;
use pyo3::types::PyDict;
use std::collections::HashMap;

pub mod batch;
pub mod char;
pub mod compression;
pub mod hyper;
pub mod patterns;
pub mod text;
pub mod token;
pub mod unigram;
pub mod zipf;

/// Counts the number of characters in a string.
#[pyfunction]
fn count_chars(text: &str) -> PyResult<usize> {
    Ok(char::unicode::count_chars(text))
}

/// Counts the number of words in a string using Unicode segmentation rules.
#[pyfunction]
fn count_words(text: &str) -> PyResult<usize> {
    Ok(text::segmentation::count_words(text))
}

/// Checks if a string is ASCII.
#[pyfunction]
fn is_ascii(text: &str) -> PyResult<bool> {
    Ok(char::unicode::is_ascii(text))
}

/// Checks if a character is ASCII.
#[pyfunction]
fn is_char_ascii(ch: char) -> PyResult<bool> {
    Ok(ch.is_ascii())
}

/// Calculates the ASCII ratio of a string.
#[pyfunction]
fn ratio_ascii(text: &str) -> PyResult<f64> {
    Ok(char::unicode::ratio_ascii(text))
}

/// Checks if a character is a letter.
#[pyfunction]
fn is_letter(ch: char) -> PyResult<bool> {
    Ok(char::unicode::is_letter(ch))
}

/// Checks if a character is a digit.
#[pyfunction]
fn is_digit(ch: char) -> PyResult<bool> {
    Ok(char::unicode::is_digit(ch))
}

/// Checks if a character is punctuation.
#[pyfunction]
fn is_punctuation(ch: char) -> PyResult<bool> {
    Ok(char::unicode::is_punctuation(ch))
}

/// Checks if a character is a symbol.
#[pyfunction]
fn is_symbol(ch: char) -> PyResult<bool> {
    Ok(char::unicode::is_symbol(ch))
}

/// Checks if a character is whitespace.
#[pyfunction]
fn is_whitespace(ch: char) -> PyResult<bool> {
    Ok(char::unicode::is_whitespace(ch))
}

/// Checks if a character is uppercase.
#[pyfunction]
fn is_uppercase(ch: char) -> PyResult<bool> {
    Ok(char::unicode::is_uppercase(ch))
}

/// Checks if a character is lowercase.
#[pyfunction]
fn is_lowercase(ch: char) -> PyResult<bool> {
    Ok(char::unicode::is_lowercase(ch))
}

/// Checks if a character is alphanumeric (letter or digit).
#[pyfunction]
fn is_alphanumeric(ch: char) -> PyResult<bool> {
    Ok(char::unicode::is_alphanumeric(ch))
}

/// Counts the number of letters in a string.
#[pyfunction]
fn count_letters(text: &str) -> PyResult<usize> {
    Ok(char::unicode::count_letters(text))
}

/// Counts the number of digits in a string.
#[pyfunction]
fn count_digits(text: &str) -> PyResult<usize> {
    Ok(char::unicode::count_digits(text))
}

/// Counts the number of punctuation characters in a string.
#[pyfunction]
fn count_punctuation(text: &str) -> PyResult<usize> {
    Ok(char::unicode::count_punctuation(text))
}

/// Counts the number of symbol characters in a string.
#[pyfunction]
fn count_symbols(text: &str) -> PyResult<usize> {
    Ok(char::unicode::count_symbols(text))
}

/// Counts the number of whitespace characters in a string.
#[pyfunction]
fn count_whitespace(text: &str) -> PyResult<usize> {
    Ok(char::unicode::count_whitespace(text))
}

/// Counts the number of non-ASCII characters in a string.
#[pyfunction]
fn count_non_ascii(text: &str) -> PyResult<usize> {
    Ok(char::unicode::count_non_ascii(text))
}

/// Counts the number of uppercase characters in a string.
#[pyfunction]
fn count_uppercase(text: &str) -> PyResult<usize> {
    Ok(char::unicode::count_uppercase(text))
}

/// Counts the number of lowercase characters in a string.
#[pyfunction]
fn count_lowercase(text: &str) -> PyResult<usize> {
    Ok(char::unicode::count_lowercase(text))
}

/// Calculates the ratio of uppercase characters to all letters in a string.
#[pyfunction]
fn ratio_uppercase(text: &str) -> PyResult<f64> {
    Ok(char::unicode::ratio_uppercase(text))
}

/// Counts the number of alphanumeric characters in a string.
#[pyfunction]
fn count_alphanumeric(text: &str) -> PyResult<usize> {
    Ok(char::unicode::count_alphanumeric(text))
}

/// Calculates the ratio of alphanumeric characters to all characters in a string.
#[pyfunction]
fn ratio_alphanumeric(text: &str) -> PyResult<f64> {
    Ok(char::unicode::ratio_alphanumeric(text))
}

/// Calculates the ratio of alphabetic to numeric characters in a string.
#[pyfunction]
fn ratio_alpha_to_numeric(text: &str) -> PyResult<f64> {
    Ok(char::unicode::ratio_alpha_to_numeric(text))
}

/// Calculates the Shannon entropy of a string at the character level.
#[pyfunction]
fn char_entropy(text: &str) -> PyResult<f64> {
    Ok(char::unicode::char_entropy(text))
}

/// Calculates the ratio of whitespace characters to all characters.
#[pyfunction]
fn ratio_whitespace(text: &str) -> PyResult<f64> {
    Ok(char::unicode::ratio_whitespace(text))
}

/// Calculates the ratio of digit characters to all characters.
#[pyfunction]
fn ratio_digits(text: &str) -> PyResult<f64> {
    Ok(char::unicode::ratio_digits(text))
}

/// Calculates the ratio of punctuation characters to all characters.
#[pyfunction]
fn ratio_punctuation(text: &str) -> PyResult<f64> {
    Ok(char::unicode::ratio_punctuation(text))
}

/// Calculates all character metrics in a single pass and returns them as a dictionary.
/// This is significantly more efficient than calling each metric function separately.
/// The returned dictionary includes nested dictionaries for Unicode category ratios.
#[pyfunction]
fn get_all_char_metrics(py: Python, text: &str) -> PyResult<PyObject> {
    let metrics = char::unicode::calculate_char_metrics(text);

    // Create a Python dictionary directly instead of using a HashMap
    let dict = PyDict::new(py);

    // Count metrics
    dict.set_item("char_count", metrics.total_chars)?;
    dict.set_item("total_chars", metrics.total_chars)?; // Keep for backward compatibility
    dict.set_item("letter_count", metrics.letters)?;
    dict.set_item("letters", metrics.letters)?; // Keep for backward compatibility
    dict.set_item("digit_count", metrics.digits)?;
    dict.set_item("digits", metrics.digits)?; // Keep for backward compatibility
    dict.set_item("punctuation_count", metrics.punctuation)?;
    dict.set_item("punctuation", metrics.punctuation)?; // Keep for backward compatibility
    dict.set_item("symbol_count", metrics.symbols)?;
    dict.set_item("symbols", metrics.symbols)?; // Keep for backward compatibility
    dict.set_item("whitespace_count", metrics.whitespace)?;
    dict.set_item("whitespace", metrics.whitespace)?; // Keep for backward compatibility
    dict.set_item("non_ascii_count", metrics.non_ascii)?;
    dict.set_item("non_ascii", metrics.non_ascii)?; // Keep for backward compatibility
    dict.set_item("uppercase_count", metrics.uppercase)?;
    dict.set_item("uppercase", metrics.uppercase)?; // Keep for backward compatibility
    dict.set_item("lowercase_count", metrics.lowercase)?;
    dict.set_item("lowercase", metrics.lowercase)?; // Keep for backward compatibility
    dict.set_item("alphanumeric_count", metrics.alphanumeric)?;
    dict.set_item("alphanumeric", metrics.alphanumeric)?; // Keep for backward compatibility

    // Ratio metrics
    dict.set_item("ratio_letters", metrics.ratio_letters)?;
    dict.set_item("ratio_digits", metrics.ratio_digits)?;
    dict.set_item("ratio_punctuation", metrics.ratio_punctuation)?;
    dict.set_item("ratio_symbols", metrics.ratio_symbols)?;
    dict.set_item("ratio_whitespace", metrics.ratio_whitespace)?;
    dict.set_item("ratio_non_ascii", metrics.ratio_non_ascii)?;
    dict.set_item("ratio_uppercase", metrics.ratio_uppercase)?;
    dict.set_item("ratio_lowercase", metrics.ratio_lowercase)?;
    dict.set_item("ratio_alphanumeric", metrics.ratio_alphanumeric)?;
    dict.set_item("ratio_alpha_to_numeric", metrics.ratio_alpha_to_numeric)?;
    dict.set_item("char_entropy", metrics.char_entropy)?;
    dict.set_item("ascii_ratio", 1.0 - metrics.ratio_non_ascii)?;

    // Add new count metrics
    dict.set_item("char_type_transitions", metrics.char_type_transitions)?;
    dict.set_item("consecutive_runs", metrics.consecutive_runs)?;
    dict.set_item("punctuation_diversity", metrics.punctuation_diversity)?;

    // Add new ratio metrics
    dict.set_item("case_ratio", metrics.case_ratio)?;
    dict.set_item("category_entropy", metrics.category_entropy)?;

    // Add Unicode category ratios
    let category_ratios = char::categories::category_ratios(text);
    let category_dict = PyDict::new(py);
    for (category, ratio) in category_ratios {
        let category_str = char::categories::category_to_string(category).to_string();
        category_dict.set_item(category_str, ratio)?;
    }
    dict.set_item("unicode_category_ratios", category_dict)?;

    // Add Unicode category group ratios
    let group_ratios = char::categories::category_group_ratios(text);
    let group_dict = PyDict::new(py);
    for (group, ratio) in group_ratios {
        let group_str = char::categories::category_group_to_string(group).to_string();
        group_dict.set_item(group_str, ratio)?;
    }
    dict.set_item("unicode_category_group_ratios", group_dict)?;

    // Add character frequencies
    let char_freq = char::unicode::char_frequency(text);
    let char_freq_dict = PyDict::new(py);
    for (c, freq) in char_freq {
        char_freq_dict.set_item(c.to_string(), freq)?;
    }
    dict.set_item("char_frequency", char_freq_dict)?;

    // Add Unicode category bigram ratios
    let category_bigram_ratios = char::categories::category_bigram_ratios(text);
    let category_bigram_dict = PyDict::new(py);
    for ((prev_cat, next_cat), ratio) in category_bigram_ratios {
        // Get a tuple of (prev, next) with clean formatting using START/END for None
        let prev_str = prev_cat.unwrap_or_else(|| "START".to_string());
        let next_str = next_cat.unwrap_or_else(|| "END".to_string());

        // Create a tuple key for Python
        let key = (prev_str, next_str);
        category_bigram_dict.set_item(key, ratio)?;
    }
    dict.set_item("unicode_category_bigram_ratios", category_bigram_dict)?;

    // Add Unicode category group bigram ratios
    let group_bigram_ratios = char::categories::category_group_bigram_ratios(text);
    let group_bigram_dict = PyDict::new(py);
    for ((prev_group, next_group), ratio) in group_bigram_ratios {
        // Get a tuple of (prev, next) with clean formatting using START/END for None
        let prev_str = prev_group.unwrap_or_else(|| "START".to_string());
        let next_str = next_group.unwrap_or_else(|| "END".to_string());

        // Create a tuple key for Python
        let key = (prev_str, next_str);
        group_bigram_dict.set_item(key, ratio)?;
    }
    dict.set_item("unicode_category_group_bigram_ratios", group_bigram_dict)?;

    // Add Unicode category trigram ratios
    let category_trigram_ratios = char::categories::category_trigram_ratios(text);
    let category_trigram_dict = PyDict::new(py);
    for ((prev_cat, current_cat, next_cat), ratio) in category_trigram_ratios {
        // Get tuple elements with clean formatting using START/END for None
        let prev_str = prev_cat.unwrap_or_else(|| "START".to_string());
        let current_str = current_cat;
        let next_str = next_cat.unwrap_or_else(|| "END".to_string());

        // Create a tuple key for Python
        let key = (prev_str, current_str, next_str);
        category_trigram_dict.set_item(key, ratio)?;
    }
    dict.set_item("unicode_category_trigram_ratios", category_trigram_dict)?;

    // Add Unicode category group trigram ratios
    let group_trigram_ratios = char::categories::category_group_trigram_ratios(text);
    let group_trigram_dict = PyDict::new(py);
    for ((prev_group, current_group, next_group), ratio) in group_trigram_ratios {
        // Get tuple elements with clean formatting using START/END for None
        let prev_str = prev_group.unwrap_or_else(|| "START".to_string());
        let current_str = current_group;
        let next_str = next_group.unwrap_or_else(|| "END".to_string());

        // Create a tuple key for Python
        let key = (prev_str, current_str, next_str);
        group_trigram_dict.set_item(key, ratio)?;
    }
    dict.set_item("unicode_category_group_trigram_ratios", group_trigram_dict)?;

    // Convert the Python dictionary to a PyObject and return it
    Ok(dict.into())
}

/// Gets the Unicode category for each character in a string.
#[pyfunction]
fn get_unicode_categories(text: &str) -> PyResult<Vec<String>> {
    let categories = char::categories::to_category_vector(text);
    let py_categories = categories
        .into_iter()
        .map(|c| char::categories::category_to_string(c).to_string())
        .collect();
    Ok(py_categories)
}

/// Gets the Unicode category group for each character in a string.
#[pyfunction]
fn get_unicode_category_groups(text: &str) -> PyResult<Vec<String>> {
    let groups = char::categories::to_category_group_vector(text);
    let py_groups = groups
        .into_iter()
        .map(|g| char::categories::category_group_to_string(g).to_string())
        .collect();
    Ok(py_groups)
}

/// Counts the number of occurrences of each Unicode category in a string.
#[pyfunction]
fn count_unicode_categories(text: &str) -> PyResult<HashMap<String, usize>> {
    let counts = char::categories::count_categories(text);
    let py_counts = counts
        .into_iter()
        .map(|(k, v)| (char::categories::category_to_string(k).to_string(), v))
        .collect();
    Ok(py_counts)
}

/// Counts the number of occurrences of each Unicode category group in a string.
#[pyfunction]
fn count_unicode_category_groups(text: &str) -> PyResult<HashMap<String, usize>> {
    let counts = char::categories::count_category_groups(text);
    let py_counts = counts
        .into_iter()
        .map(|(k, v)| (char::categories::category_group_to_string(k).to_string(), v))
        .collect();
    Ok(py_counts)
}

/// Calculates the ratio of each Unicode category in a string.
#[pyfunction]
fn get_unicode_category_ratios(text: &str) -> PyResult<HashMap<String, f64>> {
    let ratios = char::categories::category_ratios(text);
    let py_ratios = ratios
        .into_iter()
        .map(|(k, v)| (char::categories::category_to_string(k).to_string(), v))
        .collect();
    Ok(py_ratios)
}

/// Calculates the ratio of each Unicode category group in a string.
#[pyfunction]
fn get_unicode_category_group_ratios(text: &str) -> PyResult<HashMap<String, f64>> {
    let ratios = char::categories::category_group_ratios(text);
    let py_ratios = ratios
        .into_iter()
        .map(|(k, v)| (char::categories::category_group_to_string(k).to_string(), v))
        .collect();
    Ok(py_ratios)
}

/// Gets frequencies of Unicode category bigrams in a string.
/// Each bigram is a tuple of (previous category, next category).
/// For the first character, the previous category is "START".
/// For the last character, the next category is "END".
#[pyfunction]
fn get_unicode_category_bigrams(py: Python, text: &str) -> PyResult<PyObject> {
    let bigrams = char::categories::count_category_bigrams(text);
    let dict = PyDict::new(py);

    for ((prev_cat, next_cat), count) in bigrams {
        // Get a tuple of (prev, next) with clean formatting using START/END for None
        let prev_str = prev_cat.unwrap_or_else(|| "START".to_string());
        let next_str = next_cat.unwrap_or_else(|| "END".to_string());

        // Create a tuple key for Python
        let key = (prev_str, next_str);
        dict.set_item(key, count)?;
    }

    Ok(dict.into())
}

/// Gets ratios of Unicode category bigrams in a string.
#[pyfunction]
fn get_unicode_category_bigram_ratios(py: Python, text: &str) -> PyResult<PyObject> {
    let ratios = char::categories::category_bigram_ratios(text);
    let dict = PyDict::new(py);

    for ((prev_cat, next_cat), ratio) in ratios {
        // Get a tuple of (prev, next) with clean formatting using START/END for None
        let prev_str = prev_cat.unwrap_or_else(|| "START".to_string());
        let next_str = next_cat.unwrap_or_else(|| "END".to_string());

        // Create a tuple key for Python
        let key = (prev_str, next_str);
        dict.set_item(key, ratio)?;
    }

    Ok(dict.into())
}

/// Gets frequencies of Unicode category group bigrams in a string.
/// Each bigram is a tuple of (previous group, next group).
/// For the first character, the previous group is "START".
/// For the last character, the next group is "END".
#[pyfunction]
fn get_unicode_category_group_bigrams(py: Python, text: &str) -> PyResult<PyObject> {
    let bigrams = char::categories::count_category_group_bigrams(text);
    let dict = PyDict::new(py);

    for ((prev_group, next_group), count) in bigrams {
        // Get a tuple of (prev, next) with clean formatting using START/END for None
        let prev_str = prev_group.unwrap_or_else(|| "START".to_string());
        let next_str = next_group.unwrap_or_else(|| "END".to_string());

        // Create a tuple key for Python
        let key = (prev_str, next_str);
        dict.set_item(key, count)?;
    }

    Ok(dict.into())
}

/// Gets ratios of Unicode category group bigrams in a string.
#[pyfunction]
fn get_unicode_category_group_bigram_ratios(py: Python, text: &str) -> PyResult<PyObject> {
    let ratios = char::categories::category_group_bigram_ratios(text);
    let dict = PyDict::new(py);

    for ((prev_group, next_group), ratio) in ratios {
        // Get a tuple of (prev, next) with clean formatting using START/END for None
        let prev_str = prev_group.unwrap_or_else(|| "START".to_string());
        let next_str = next_group.unwrap_or_else(|| "END".to_string());

        // Create a tuple key for Python
        let key = (prev_str, next_str);
        dict.set_item(key, ratio)?;
    }

    Ok(dict.into())
}

/// Calculate Unicode category trigrams with "START" and "END" markers
#[pyfunction]
fn get_unicode_category_trigrams(py: Python, text: &str) -> PyResult<PyObject> {
    let trigram_map = char::categories::count_category_trigrams(text);
    let dict = PyDict::new(py);

    // Convert special None values to "START" and "END" strings for Python interface
    for ((prev, current, next), count) in trigram_map {
        let prev_str = prev.unwrap_or_else(|| "START".to_string());
        let next_str = next.unwrap_or_else(|| "END".to_string());
        let key = (prev_str, current, next_str);
        dict.set_item(key, count)?;
    }

    Ok(dict.into())
}

/// Calculate Unicode category trigram ratios with "START" and "END" markers
#[pyfunction]
fn get_unicode_category_trigram_ratios(py: Python, text: &str) -> PyResult<PyObject> {
    let trigram_map = char::categories::category_trigram_ratios(text);
    let dict = PyDict::new(py);

    // Convert special None values to "START" and "END" strings for Python interface
    for ((prev, current, next), ratio) in trigram_map {
        let prev_str = prev.unwrap_or_else(|| "START".to_string());
        let next_str = next.unwrap_or_else(|| "END".to_string());
        let key = (prev_str, current, next_str);
        dict.set_item(key, ratio)?;
    }

    Ok(dict.into())
}

/// Calculate Unicode category group trigrams with "START" and "END" markers
#[pyfunction]
fn get_unicode_category_group_trigrams(py: Python, text: &str) -> PyResult<PyObject> {
    let trigram_map = char::categories::count_category_group_trigrams(text);
    let dict = PyDict::new(py);

    // Convert special None values to "START" and "END" strings for Python interface
    for ((prev, current, next), count) in trigram_map {
        let prev_str = prev.unwrap_or_else(|| "START".to_string());
        let next_str = next.unwrap_or_else(|| "END".to_string());
        let key = (prev_str, current, next_str);
        dict.set_item(key, count)?;
    }

    Ok(dict.into())
}

/// Calculate Unicode category group trigram ratios with "START" and "END" markers
#[pyfunction]
fn get_unicode_category_group_trigram_ratios(py: Python, text: &str) -> PyResult<PyObject> {
    let trigram_map = char::categories::category_group_trigram_ratios(text);
    let dict = PyDict::new(py);

    // Convert special None values to "START" and "END" strings for Python interface
    for ((prev, current, next), ratio) in trigram_map {
        let prev_str = prev.unwrap_or_else(|| "START".to_string());
        let next_str = next.unwrap_or_else(|| "END".to_string());
        let key = (prev_str, current, next_str);
        dict.set_item(key, ratio)?;
    }

    Ok(dict.into())
}

/// Gets character frequency counts for a string
#[pyfunction]
fn get_char_frequency(text: &str) -> PyResult<HashMap<String, usize>> {
    let freq = char::unicode::char_frequency(text);
    // Convert char keys to string for Python compatibility
    let py_freq = freq.into_iter().map(|(k, v)| (k.to_string(), v)).collect();
    Ok(py_freq)
}

/// Gets character type frequency counts for a string
#[pyfunction]
fn get_char_type_frequency(text: &str) -> PyResult<HashMap<String, usize>> {
    let freq = char::unicode::char_type_frequency(text);
    // Convert &str keys to string for Python compatibility
    let py_freq = freq.into_iter().map(|(k, v)| (k.to_string(), v)).collect();
    Ok(py_freq)
}

/// Combined character metrics in a single pass (optimized Rust implementation)
#[pyfunction]
fn combined_char_metrics(text: &str) -> PyResult<HashMap<String, usize>> {
    let metrics = char::unicode::combined_char_metrics(text);
    // Convert &str keys to string for Python compatibility
    let py_metrics = metrics
        .into_iter()
        .map(|(k, v)| (k.to_string(), v))
        .collect();
    Ok(py_metrics)
}

/// Gets Unicode category frequency counts for a string (optimized)
#[pyfunction]
fn get_unicode_category_frequency(text: &str) -> PyResult<HashMap<String, usize>> {
    Ok(char::categories::category_string_frequency(text))
}

/// Gets Unicode category group frequency counts for a string (optimized)
#[pyfunction]
fn get_unicode_category_group_frequency(text: &str) -> PyResult<HashMap<String, usize>> {
    Ok(char::categories::category_group_string_frequency(text))
}

/// Splits text into words according to Unicode segmentation rules
#[pyfunction]
fn split_words(text: &str) -> PyResult<Vec<String>> {
    let words = text::segmentation::split_words(text);
    Ok(words.into_iter().map(|s| s.to_string()).collect())
}

/// Splits text into lines
#[pyfunction]
fn split_lines(text: &str) -> PyResult<Vec<String>> {
    let lines = text::segmentation::split_lines(text);
    Ok(lines.into_iter().map(|s| s.to_string()).collect())
}

/// Counts the number of lines in text
#[pyfunction]
fn count_lines(text: &str) -> PyResult<usize> {
    Ok(text::segmentation::count_lines(text))
}

/// Calculates the average line length in characters
#[pyfunction]
fn average_line_length(text: &str) -> PyResult<f64> {
    Ok(text::segmentation::average_line_length(text))
}

/// Splits text into paragraphs
#[pyfunction]
fn split_paragraphs(text: &str) -> PyResult<Vec<String>> {
    Ok(text::segmentation::split_paragraphs(text))
}

/// Counts the number of paragraphs in text
#[pyfunction]
fn count_paragraphs(text: &str) -> PyResult<usize> {
    Ok(text::segmentation::count_paragraphs(text))
}

/// Calculates the average paragraph length in characters
#[pyfunction]
fn average_paragraph_length(text: &str) -> PyResult<f64> {
    Ok(text::segmentation::average_paragraph_length(text))
}

/// Calculates the average word length in characters
#[pyfunction]
fn average_word_length(text: &str) -> PyResult<f64> {
    Ok(text::segmentation::average_word_length(text))
}

/// Calculates the average sentence length in words
#[pyfunction]
fn average_sentence_length(text: &str) -> PyResult<f64> {
    Ok(text::segmentation::average_sentence_length(text))
}

/// Segments text into lines (consistent naming with segment_paragraphs and segment_sentences)
#[pyfunction]
fn segment_lines(text: &str) -> PyResult<Vec<String>> {
    Ok(text::segmentation::segment_lines(text))
}

/// Segments text into paragraphs
#[pyfunction]
fn segment_paragraphs(text: &str) -> PyResult<Vec<String>> {
    Ok(text::segmentation::segment_paragraphs(text))
}

/// Segments text into sentences
#[pyfunction]
fn segment_sentences(text: &str) -> PyResult<Vec<String>> {
    Ok(text::segmentation::segment_sentences(text))
}

// Unigram tokenization functions

/// Tokenizes a text into unigram tokens (words only).
#[pyfunction]
fn tokenize_unigrams(text: &str) -> PyResult<Vec<String>> {
    Ok(unigram::tokenize(text))
}

/// Tokenizes a text into unigram tokens, including punctuation and whitespace.
#[pyfunction]
fn tokenize_unigrams_with_punctuation(text: &str) -> PyResult<Vec<String>> {
    Ok(unigram::tokenize_with_punctuation(text))
}

/// Counts the total number of unigram tokens in a text.
#[pyfunction]
fn count_unigram_tokens(text: &str, include_punctuation: bool) -> PyResult<usize> {
    Ok(unigram::count_tokens(text, include_punctuation))
}

/// Counts the number of unique unigram tokens in a text.
#[pyfunction]
fn count_unique_unigrams(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> PyResult<usize> {
    Ok(unigram::count_unique_tokens(
        text,
        include_punctuation,
        case_sensitive,
    ))
}

/// Calculates the type-token ratio (unique tokens / total tokens) for unigram tokens.
#[pyfunction]
fn unigram_type_token_ratio(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> PyResult<f64> {
    Ok(unigram::type_token_ratio(
        text,
        include_punctuation,
        case_sensitive,
    ))
}

/// Calculates the repetition rate (1 - unique tokens / total tokens) for unigram tokens.
#[pyfunction]
fn unigram_repetition_rate(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> PyResult<f64> {
    Ok(unigram::repetition_rate(
        text,
        include_punctuation,
        case_sensitive,
    ))
}

/// Counts the frequency of each unigram token in the text.
#[pyfunction]
fn get_unigram_frequency(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> PyResult<HashMap<String, usize>> {
    Ok(unigram::token_frequency(
        text,
        include_punctuation,
        case_sensitive,
    ))
}

/// Calculates the Shannon entropy of the unigram token distribution.
#[pyfunction]
fn unigram_entropy(text: &str, include_punctuation: bool, case_sensitive: bool) -> PyResult<f64> {
    Ok(unigram::token_entropy(
        text,
        include_punctuation,
        case_sensitive,
    ))
}

/// Calculates the maximum token frequency ratio in a text.
#[pyfunction]
fn max_unigram_frequency_ratio(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> PyResult<f64> {
    Ok(unigram::max_token_frequency_ratio(
        text,
        include_punctuation,
        case_sensitive,
    ))
}

/// Calculates all unigram metrics in a single pass, significantly improving performance.
/// This minimizes passes between Python and Rust for large texts.
#[pyfunction]
fn get_all_unigram_metrics(
    py: Python,
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> PyResult<PyObject> {
    // Get all metrics in a single pass
    let metrics = unigram::calculate_all_unigram_metrics(text, include_punctuation, case_sensitive);

    // Create a Python dictionary
    let dict = PyDict::new(py);

    // Add count metrics
    dict.set_item("token_count", metrics.token_count)?;
    dict.set_item("unique_token_count", metrics.unique_token_count)?;

    // Add ratio metrics
    dict.set_item("type_token_ratio", metrics.type_token_ratio)?;
    dict.set_item("repetition_rate", metrics.repetition_rate)?;
    dict.set_item("token_entropy", metrics.token_entropy)?;
    dict.set_item("max_frequency_ratio", metrics.max_frequency_ratio)?;
    dict.set_item("average_token_length", metrics.average_token_length)?;

    // Add new metrics
    dict.set_item("hapax_legomena_ratio", metrics.hapax_legomena_ratio)?;
    dict.set_item("top_5_token_coverage", metrics.top_5_token_coverage)?;
    dict.set_item("short_token_ratio", metrics.short_token_ratio)?;
    dict.set_item("long_token_ratio", metrics.long_token_ratio)?;

    // We no longer expose the token frequency dictionary
    // to keep the output more concise
    // Users can call get_unigram_frequency separately if needed

    // Return the Python dictionary
    Ok(dict.into())
}

// ML-based tokenization functions

/// Calculates the hapax legomena ratio in a text.
/// Hapax legomena are words that appear exactly once in the text.
#[pyfunction]
fn hapax_legomena_ratio(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> PyResult<f64> {
    Ok(unigram::hapax_legomena_ratio(
        text,
        include_punctuation,
        case_sensitive,
    ))
}

/// Calculates the top-5 token coverage in a text.
/// This is the percentage of the text covered by the 5 most frequent tokens.
#[pyfunction]
fn top_5_token_coverage(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> PyResult<f64> {
    Ok(unigram::top_5_token_coverage(
        text,
        include_punctuation,
        case_sensitive,
    ))
}

/// Calculates the ratio of short tokens (3 characters or fewer) in a text.
#[pyfunction]
fn short_token_ratio(text: &str, include_punctuation: bool, case_sensitive: bool) -> PyResult<f64> {
    Ok(unigram::short_token_ratio_default(
        text,
        include_punctuation,
        case_sensitive,
    ))
}

/// Calculates the ratio of short tokens in a text with a custom length threshold.
#[allow(dead_code)]
#[pyfunction]
fn short_token_ratio_with_threshold(
    text: &str, 
    include_punctuation: bool, 
    case_sensitive: bool,
    threshold: usize,
) -> PyResult<f64> {
    Ok(unigram::short_token_ratio(
        text,
        include_punctuation,
        case_sensitive,
        Some(threshold),
    ))
}

/// Calculates the ratio of long tokens (7 characters or more) in a text.
#[pyfunction]
fn long_token_ratio(text: &str, include_punctuation: bool, case_sensitive: bool) -> PyResult<f64> {
    Ok(unigram::long_token_ratio_default(
        text,
        include_punctuation,
        case_sensitive,
    ))
}

/// Calculates the ratio of long tokens in a text with a custom length threshold.
#[allow(dead_code)]
#[pyfunction]
fn long_token_ratio_with_threshold(
    text: &str, 
    include_punctuation: bool, 
    case_sensitive: bool,
    threshold: usize,
) -> PyResult<f64> {
    Ok(unigram::long_token_ratio(
        text,
        include_punctuation,
        case_sensitive,
        Some(threshold),
    ))
}

/// Tokenizes text using an ML tokenizer and returns the token IDs.
#[pyfunction]
fn tokenize_ml(text: &str, tokenizer_path: Option<&str>) -> PyResult<Vec<u32>> {
    match token::tokenize(text, tokenizer_path) {
        Ok(tokens) => Ok(tokens),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Batch tokenizes multiple texts using an ML tokenizer (more efficient).
#[pyfunction]
fn batch_tokenize_ml(texts: Vec<String>, tokenizer_path: Option<&str>) -> PyResult<Vec<Vec<u32>>> {
    // Convert Vec<String> to Vec<&str> for the Rust function
    let text_refs: Vec<&str> = texts.iter().map(|s| s.as_str()).collect();

    match token::batch_tokenize(&text_refs, tokenizer_path) {
        Ok(tokens) => Ok(tokens),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Counts the total number of ML tokenizer tokens in a text.
#[pyfunction]
fn subword_token_count(text: &str, tokenizer_path: Option<&str>) -> PyResult<usize> {
    match token::subword_token_count(text, tokenizer_path) {
        Ok(count) => Ok(count),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Counts the number of unique ML tokenizer tokens in a text.
#[pyfunction]
fn unique_subword_count(text: &str, tokenizer_path: Option<&str>) -> PyResult<usize> {
    match token::unique_subword_count(text, tokenizer_path) {
        Ok(count) => Ok(count),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Calculates the type-token ratio for ML tokenizer tokens.
#[pyfunction]
fn subword_type_token_ratio(text: &str, tokenizer_path: Option<&str>) -> PyResult<f64> {
    match token::subword_type_token_ratio(text, tokenizer_path) {
        Ok(ratio) => Ok(ratio),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Calculates the repetition rate for ML tokenizer tokens.
#[pyfunction]
fn subword_repetition_rate(text: &str, tokenizer_path: Option<&str>) -> PyResult<f64> {
    match token::subword_repetition_rate(text, tokenizer_path) {
        Ok(rate) => Ok(rate),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Calculates the Shannon entropy of ML tokenizer token distribution.
#[pyfunction]
fn subword_entropy(text: &str, tokenizer_path: Option<&str>) -> PyResult<f64> {
    match token::subword_entropy(text, tokenizer_path) {
        Ok(entropy) => Ok(entropy),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Calculates the tokenization efficiency for ML tokenizer tokens.
#[pyfunction]
fn subword_efficiency(text: &str, tokenizer_path: Option<&str>) -> PyResult<f64> {
    match token::subword_efficiency(text, tokenizer_path) {
        Ok(efficiency) => Ok(efficiency),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Gets comprehensive ML tokenizer metrics for a text in a single function call.
#[pyfunction]
fn get_token_metrics(py: Python, text: &str, tokenizer_path: Option<&str>) -> PyResult<PyObject> {
    match token::get_token_metrics(text, tokenizer_path) {
        Ok(metrics) => {
            let dict = PyDict::new(py);

            for (key, value) in metrics {
                dict.set_item(key, value)?;
            }

            Ok(dict.into())
        }
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Calculates the compression ratio of text using the deflate algorithm.
/// This is the ratio of original text size to compressed text size.
/// Higher values indicate more compressible (redundant) text.
#[pyfunction]
fn compression_ratio(text: &str) -> PyResult<f64> {
    match compression::calculate_compression_ratio(text) {
        Ok(ratio) => Ok(ratio),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Gets comprehensive compression metrics for a text in a single function call.
#[pyfunction]
fn get_compression_metrics(py: Python, text: &str) -> PyResult<PyObject> {
    match compression::get_compression_metrics(text) {
        Ok(metrics) => {
            let dict = PyDict::new(py);

            for (key, value) in metrics {
                dict.set_item(key, value)?;
            }

            Ok(dict.into())
        }
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Calculates the unigram compression ratio of text.
/// This uses the deflate algorithm specifically on word tokens.
#[pyfunction]
fn unigram_compression_ratio(text: &str, include_punctuation: bool) -> PyResult<f64> {
    match compression::unigram_compression_ratio(text, include_punctuation) {
        Ok(ratio) => Ok(ratio),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

// Pattern matching functions

/// Counts occurrences of a regex pattern in text
#[pyfunction]
fn count_regex_matches(text: &str, pattern: &str) -> PyResult<usize> {
    match patterns::count_regex_matches(text, pattern) {
        Ok(count) => Ok(count),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Checks if text contains matches for a regex pattern
#[pyfunction]
fn contains_regex_pattern(text: &str, pattern: &str) -> PyResult<bool> {
    match patterns::contains_regex_pattern(text, pattern) {
        Ok(contains) => Ok(contains),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Counts copyright mentions in text
#[pyfunction]
fn count_copyright_mentions(text: &str) -> PyResult<usize> {
    match patterns::count_copyright_mentions(text) {
        Ok(count) => Ok(count),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Counts "rights reserved" mentions in text
#[pyfunction]
fn count_rights_reserved(text: &str) -> PyResult<usize> {
    match patterns::count_rights_reserved(text) {
        Ok(count) => Ok(count),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Counts section headings in text
#[pyfunction]
fn count_section_strings(text: &str) -> PyResult<usize> {
    match patterns::count_section_strings(text) {
        Ok(count) => Ok(count),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Counts question phrases/sentences in text
#[pyfunction]
fn count_question_strings(text: &str) -> PyResult<usize> {
    match patterns::count_question_strings(text) {
        Ok(count) => Ok(count),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Counts interrogative question forms in text (who, what, when, where, why, how, etc.)
/// Only matches questions that begin with properly capitalized interrogative words
#[pyfunction]
fn count_interrogative_questions(text: &str) -> PyResult<usize> {
    match patterns::count_interrogative_questions(text) {
        Ok(count) => Ok(count),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Counts complex interrogative phrases with expanded variations
/// Matches a comprehensive set of question patterns like "How many", "What can", etc.
#[pyfunction]
fn count_complex_interrogatives(text: &str) -> PyResult<usize> {
    match patterns::count_complex_interrogatives(text) {
        Ok(count) => Ok(count),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Counts factual statements in text (often seen in educational content)
#[pyfunction]
fn count_factual_statements(text: &str) -> PyResult<usize> {
    match patterns::count_factual_statements(text) {
        Ok(count) => Ok(count),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Counts logical reasoning and argumentation expressions in text
#[pyfunction]
fn count_logical_reasoning(text: &str) -> PyResult<usize> {
    match patterns::count_logical_reasoning(text) {
        Ok(count) => Ok(count),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Checks if text contains code-like constructs
#[pyfunction]
fn contains_code_characters(text: &str) -> PyResult<bool> {
    match patterns::contains_code_characters(text) {
        Ok(contains) => Ok(contains),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Calculates the ratio of bullet or ellipsis lines to total lines
#[pyfunction]
fn bullet_or_ellipsis_lines_ratio(text: &str) -> PyResult<f64> {
    match patterns::bullet_or_ellipsis_lines_ratio(text) {
        Ok(ratio) => Ok(ratio),
        Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
            e.to_string(),
        )),
    }
}

/// Checks if text contains any blacklisted terms
#[pyfunction]
fn contains_blacklist_substring(text: &str, blacklist: Vec<String>) -> PyResult<bool> {
    // Convert Vec<String> to Vec<&str>
    let blacklist_refs: Vec<&str> = blacklist.iter().map(|s| s.as_str()).collect();
    Ok(patterns::contains_blacklist_substring(
        text,
        &blacklist_refs,
    ))
}

// Zipf's law and power distribution metrics

/// Calculates the Zipf fitness score for word frequency distribution
#[pyfunction]
fn zipf_fitness_score(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> PyResult<f64> {
    // Get token frequency using our existing function
    let frequencies = unigram::token_frequency(text, include_punctuation, case_sensitive);
    Ok(zipf::calculate_zipf_fitness(&frequencies))
}

/// Estimates the power law exponent for word frequency distribution
#[pyfunction]
fn power_law_exponent(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> PyResult<f64> {
    let frequencies = unigram::token_frequency(text, include_punctuation, case_sensitive);
    Ok(zipf::estimate_power_law_exponent(&frequencies))
}

/// Calculates the token burstiness for specific words in text
#[pyfunction]
fn calculate_burstiness(text: &str, tokens: Vec<String>) -> PyResult<f64> {
    // Convert Vec<String> to Vec<&str>
    let token_refs: Vec<&str> = tokens.iter().map(|s| s.as_str()).collect();
    Ok(zipf::calculate_burstiness(text, &token_refs))
}

/// Analyzes the vocabulary growth rate in a text
#[pyfunction]
fn analyze_vocab_growth(py: Python, text: &str, chunk_size: usize) -> PyResult<PyObject> {
    let stats = zipf::analyze_vocab_growth(text, chunk_size);

    // Convert to Python dictionary
    let dict = PyDict::new(py);
    dict.set_item("chunks_analyzed", stats.chunks_analyzed)?;
    dict.set_item(
        "average_new_tokens_per_chunk",
        stats.average_new_tokens_per_chunk,
    )?;
    dict.set_item("cumulative_vocab_sizes", stats.cumulative_vocab_sizes)?;

    Ok(dict.into())
}

/// Calculates all Zipf-related metrics for a text
#[pyfunction]
fn get_zipf_metrics(
    py: Python,
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> PyResult<PyObject> {
    let frequencies = unigram::token_frequency(text, include_punctuation, case_sensitive);
    let metrics = zipf::get_zipf_metrics(&frequencies);

    // Convert to Python dictionary
    let dict = PyDict::new(py);
    for (key, value) in metrics {
        dict.set_item(key, value)?;
    }

    Ok(dict.into())
}

/// Calculates all pattern-based metrics efficiently by leveraging paragraph processing for large texts.
///
/// This function provides pattern-based statistics such as question counts, factual statement detection,
/// and content type indicators using regex pattern matching. For large texts, it can process by paragraph
/// to improve performance.
///
/// If a paragraph is longer than max_segment_size bytes (default 4096), it will be further broken down
/// into line segments for even more efficient processing.
#[pyfunction]
#[pyo3(signature = (text, use_paragraph_processing=true, max_segment_size=4096))]
fn get_all_pattern_metrics(
    py: Python,
    text: &str,
    use_paragraph_processing: bool,
    max_segment_size: usize,
) -> PyResult<PyObject> {
    // Initialize the pattern metrics dictionary
    let pattern_section = PyDict::new(py);

    // For large texts, process by paragraph when requested
    if use_paragraph_processing {
        // Split the text into paragraphs
        let paragraphs = text::segmentation::split_paragraphs(text);

        // Record that we used paragraph processing
        pattern_section.set_item("_used_paragraph_processing", true)?;
        pattern_section.set_item("_paragraph_count", paragraphs.len())?;

        // Process the paragraphs, potentially breaking them down further
        let mut processed_segments = 0;
        let mut large_paragraphs = 0;

        // For each metric we need to count, initialize a counter
        let mut question_count = 0;
        let mut interrogative_count = 0;
        let mut complex_interrogative_count = 0;
        let mut factual_statement_count = 0;
        let mut logical_reasoning_count = 0;
        let mut section_heading_count = 0;
        let mut copyright_count = 0;
        let mut rights_reserved_count = 0;
        let mut bullet_count = 0;
        let mut ellipsis_count = 0;

        // Process each paragraph, optionally breaking down large ones
        for paragraph in &paragraphs {
            processed_segments += 1;

            if paragraph.len() > max_segment_size {
                // This paragraph is too large - break it down into lines
                large_paragraphs += 1;
                let lines: Vec<String> = paragraph.lines().map(|s| s.to_string()).collect();

                // Track extremely long lines that need further chunking
                let mut extremely_long_lines = 0;

                // Process each line separately
                for line in &lines {
                    if line.len() > max_segment_size {
                        // Even this line is too long - break it into fixed-size chunks
                        extremely_long_lines += 1;

                        // Process in chunks of max_segment_size
                        let mut start = 0;

                        while start < line.len() {
                            // Calculate end position, ensuring we stay on char boundaries
                            let candidate_end = std::cmp::min(start + max_segment_size, line.len());

                            // Find the closest valid char boundary (UTF-8 safe)
                            let mut end = candidate_end;
                            while end > start && !line.is_char_boundary(end) {
                                end -= 1;
                            }

                            // Process this chunk if we have enough characters
                            // Skip chunks smaller than 10 chars as they're unlikely to match patterns
                            if end - start >= 10 {
                                let chunk = &line[start..end];

                                // Count patterns in this chunk
                                question_count += patterns::QUESTION_REGEX.find_iter(chunk).count();
                                interrogative_count +=
                                    patterns::INTERROGATIVE_REGEX.find_iter(chunk).count();
                                complex_interrogative_count +=
                                    patterns::COMPLEX_INTERROGATIVE_REGEX
                                        .find_iter(chunk)
                                        .count();
                                factual_statement_count +=
                                    patterns::FACTUAL_STATEMENT_REGEX.find_iter(chunk).count();
                                logical_reasoning_count +=
                                    patterns::LOGICAL_REASONING_REGEX.find_iter(chunk).count();
                                section_heading_count +=
                                    patterns::SECTION_HEADING_REGEX.find_iter(chunk).count();
                                copyright_count +=
                                    patterns::COPYRIGHT_REGEX.find_iter(chunk).count();
                                rights_reserved_count +=
                                    patterns::RIGHTS_RESERVED_REGEX.find_iter(chunk).count();
                                bullet_count += patterns::BULLET_REGEX.find_iter(chunk).count();
                                ellipsis_count += patterns::ELLIPSIS_REGEX.find_iter(chunk).count();
                            }

                            // Move to next chunk
                            start = end;
                        }
                    } else {
                        // Line is reasonably sized - process normally
                        question_count += patterns::QUESTION_REGEX.find_iter(line).count();
                        interrogative_count +=
                            patterns::INTERROGATIVE_REGEX.find_iter(line).count();
                        complex_interrogative_count += patterns::COMPLEX_INTERROGATIVE_REGEX
                            .find_iter(line)
                            .count();
                        factual_statement_count +=
                            patterns::FACTUAL_STATEMENT_REGEX.find_iter(line).count();
                        logical_reasoning_count +=
                            patterns::LOGICAL_REASONING_REGEX.find_iter(line).count();
                        section_heading_count +=
                            patterns::SECTION_HEADING_REGEX.find_iter(line).count();
                        copyright_count += patterns::COPYRIGHT_REGEX.find_iter(line).count();
                        rights_reserved_count +=
                            patterns::RIGHTS_RESERVED_REGEX.find_iter(line).count();
                        bullet_count += patterns::BULLET_REGEX.find_iter(line).count();
                        ellipsis_count += patterns::ELLIPSIS_REGEX.find_iter(line).count();
                    }
                }

                // Add metadata about extremely long lines
                pattern_section.set_item("_extremely_long_lines_chunked", extremely_long_lines)?;
            } else {
                // Normal-sized paragraph - process it as a single unit
                question_count += patterns::QUESTION_REGEX.find_iter(paragraph).count();
                interrogative_count += patterns::INTERROGATIVE_REGEX.find_iter(paragraph).count();
                complex_interrogative_count += patterns::COMPLEX_INTERROGATIVE_REGEX
                    .find_iter(paragraph)
                    .count();
                factual_statement_count += patterns::FACTUAL_STATEMENT_REGEX
                    .find_iter(paragraph)
                    .count();
                logical_reasoning_count += patterns::LOGICAL_REASONING_REGEX
                    .find_iter(paragraph)
                    .count();
                section_heading_count +=
                    patterns::SECTION_HEADING_REGEX.find_iter(paragraph).count();
                copyright_count += patterns::COPYRIGHT_REGEX.find_iter(paragraph).count();
                rights_reserved_count +=
                    patterns::RIGHTS_RESERVED_REGEX.find_iter(paragraph).count();
                bullet_count += patterns::BULLET_REGEX.find_iter(paragraph).count();
                ellipsis_count += patterns::ELLIPSIS_REGEX.find_iter(paragraph).count();
            }
        }

        // Add processing metadata
        pattern_section.set_item("_segments_processed", processed_segments)?;
        pattern_section.set_item("_large_paragraphs_broken_down", large_paragraphs)?;
        pattern_section.set_item("_max_segment_size", max_segment_size)?;

        // Add all the metric counts
        pattern_section.set_item("question_count", question_count)?;
        pattern_section.set_item("interrogative_question_count", interrogative_count)?;
        pattern_section.set_item("complex_interrogative_count", complex_interrogative_count)?;
        pattern_section.set_item("factual_statement_count", factual_statement_count)?;
        pattern_section.set_item("logical_reasoning_count", logical_reasoning_count)?;
        pattern_section.set_item("section_heading_count", section_heading_count)?;
        pattern_section.set_item("copyright_mention_count", copyright_count)?;
        pattern_section.set_item("rights_reserved_count", rights_reserved_count)?;
        pattern_section.set_item("bullet_count", bullet_count)?;
        pattern_section.set_item("ellipsis_count", ellipsis_count)?;

        // Some patterns need to be checked in the full text for accuracy
        let contains_code = patterns::CODE_REGEX.is_match(text);
        pattern_section.set_item("contains_code", contains_code)?;

        // Calculate bullet/ellipsis ratio
        let total_lines = text.lines().count();
        let bullet_ellipsis_ratio = if total_lines > 0 {
            (bullet_count + ellipsis_count) as f64 / total_lines as f64
        } else {
            0.0
        };
        pattern_section.set_item("bullet_ellipsis_ratio", bullet_ellipsis_ratio)?;
    } else {
        // Process the full text at once (original method)
        pattern_section.set_item("_used_paragraph_processing", false)?;

        let question_count = patterns::QUESTION_REGEX.find_iter(text).count();
        pattern_section.set_item("question_count", question_count)?;

        let interrogative_count = patterns::INTERROGATIVE_REGEX.find_iter(text).count();
        pattern_section.set_item("interrogative_question_count", interrogative_count)?;

        let complex_interrogative_count = patterns::COMPLEX_INTERROGATIVE_REGEX
            .find_iter(text)
            .count();
        pattern_section.set_item("complex_interrogative_count", complex_interrogative_count)?;

        let factual_statement_count = patterns::FACTUAL_STATEMENT_REGEX.find_iter(text).count();
        pattern_section.set_item("factual_statement_count", factual_statement_count)?;

        let logical_reasoning_count = patterns::LOGICAL_REASONING_REGEX.find_iter(text).count();
        pattern_section.set_item("logical_reasoning_count", logical_reasoning_count)?;

        let section_heading_count = patterns::SECTION_HEADING_REGEX.find_iter(text).count();
        pattern_section.set_item("section_heading_count", section_heading_count)?;

        let copyright_count = patterns::COPYRIGHT_REGEX.find_iter(text).count();
        pattern_section.set_item("copyright_mention_count", copyright_count)?;

        let rights_reserved_count = patterns::RIGHTS_RESERVED_REGEX.find_iter(text).count();
        pattern_section.set_item("rights_reserved_count", rights_reserved_count)?;

        let contains_code = patterns::CODE_REGEX.is_match(text);
        pattern_section.set_item("contains_code", contains_code)?;

        let bullet_count = patterns::BULLET_REGEX.find_iter(text).count();
        pattern_section.set_item("bullet_count", bullet_count)?;

        let ellipsis_count = patterns::ELLIPSIS_REGEX.find_iter(text).count();
        pattern_section.set_item("ellipsis_count", ellipsis_count)?;

        // Calculate bullet/ellipsis ratio manually to avoid another line counting pass
        let total_lines = text.lines().count();
        let bullet_ellipsis_ratio = if total_lines > 0 {
            (bullet_count + ellipsis_count) as f64 / total_lines as f64
        } else {
            0.0
        };
        pattern_section.set_item("bullet_ellipsis_ratio", bullet_ellipsis_ratio)?;
    }

    Ok(pattern_section.into())
}

/// Calculates all metrics including pattern-based metrics with optimized regex matching
/// to minimize processing time and reduce Rust-Python round trips.
///
/// By default, pattern-based metrics use paragraph processing for efficiency, with large paragraphs
/// (>4096 bytes) further broken down into line segments for better performance.
#[pyfunction]
#[pyo3(signature = (text, include_punctuation=true, case_sensitive=false, use_paragraph_processing=true, max_segment_size=4096))]
fn get_all_metrics(
    py: Python,
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
    use_paragraph_processing: bool,
    max_segment_size: usize,
) -> PyResult<PyObject> {
    // Create a new dictionary for results
    let result_dict = PyDict::new(py);

    // A simpler approach: use directly returned dictionaries
    // Get character metrics
    let char_metrics = get_all_char_metrics(py, text)?;
    result_dict.set_item("character", char_metrics)?;

    // Get unigram metrics
    let unigram_metrics = get_all_unigram_metrics(py, text, include_punctuation, case_sensitive)?;
    result_dict.set_item("unigram", unigram_metrics)?;

    // Add segmentation metrics
    let segmentation_section = PyDict::new(py);
    segmentation_section.set_item("line_count", text::segmentation::count_lines(text))?;
    segmentation_section.set_item(
        "average_line_length",
        text::segmentation::average_line_length(text),
    )?;
    segmentation_section.set_item(
        "paragraph_count",
        text::segmentation::count_paragraphs(text),
    )?;
    segmentation_section.set_item(
        "average_paragraph_length",
        text::segmentation::average_paragraph_length(text),
    )?;
    segmentation_section.set_item(
        "average_sentence_length",
        text::segmentation::average_sentence_length(text),
    )?;
    result_dict.set_item("segmentation", segmentation_section)?;

    // Get all pattern metrics
    let pattern_metrics =
        get_all_pattern_metrics(py, text, use_paragraph_processing, max_segment_size)?;
    result_dict.set_item("patterns", pattern_metrics)?;

    // Return the complete dictionary
    Ok(result_dict.into())
}

/// A Python module implemented in Rust.
#[pymodule]
fn cheesecloth(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Batch processor for efficient metric computation
    m.add_class::<batch::BatchProcessor>()?;

    // Hyper-optimized processor for calculating multiple metrics at once
    m.add_class::<hyper::HyperAnalyzer>()?;

    // Character metrics
    m.add_function(wrap_pyfunction!(count_chars, m)?)?;
    m.add_function(wrap_pyfunction!(count_words, m)?)?;
    m.add_function(wrap_pyfunction!(is_ascii, m)?)?;
    m.add_function(wrap_pyfunction!(is_char_ascii, m)?)?;
    m.add_function(wrap_pyfunction!(ratio_ascii, m)?)?;

    // Character classification functions
    m.add_function(wrap_pyfunction!(is_letter, m)?)?;
    m.add_function(wrap_pyfunction!(is_digit, m)?)?;
    m.add_function(wrap_pyfunction!(is_punctuation, m)?)?;
    m.add_function(wrap_pyfunction!(is_symbol, m)?)?;
    m.add_function(wrap_pyfunction!(is_whitespace, m)?)?;
    m.add_function(wrap_pyfunction!(is_uppercase, m)?)?;
    m.add_function(wrap_pyfunction!(is_lowercase, m)?)?;
    m.add_function(wrap_pyfunction!(is_alphanumeric, m)?)?;

    // Unicode character classifications
    m.add_function(wrap_pyfunction!(count_letters, m)?)?;
    m.add_function(wrap_pyfunction!(count_digits, m)?)?;
    m.add_function(wrap_pyfunction!(count_punctuation, m)?)?;
    m.add_function(wrap_pyfunction!(count_symbols, m)?)?;
    m.add_function(wrap_pyfunction!(count_whitespace, m)?)?;
    m.add_function(wrap_pyfunction!(count_non_ascii, m)?)?;
    m.add_function(wrap_pyfunction!(count_uppercase, m)?)?;
    m.add_function(wrap_pyfunction!(count_lowercase, m)?)?;
    m.add_function(wrap_pyfunction!(ratio_uppercase, m)?)?;
    m.add_function(wrap_pyfunction!(count_alphanumeric, m)?)?;
    m.add_function(wrap_pyfunction!(ratio_alphanumeric, m)?)?;
    m.add_function(wrap_pyfunction!(ratio_alpha_to_numeric, m)?)?;
    m.add_function(wrap_pyfunction!(ratio_whitespace, m)?)?;
    m.add_function(wrap_pyfunction!(ratio_digits, m)?)?;
    m.add_function(wrap_pyfunction!(ratio_punctuation, m)?)?;
    m.add_function(wrap_pyfunction!(char_entropy, m)?)?;

    // Unicode categories
    m.add_function(wrap_pyfunction!(get_unicode_categories, m)?)?;
    m.add_function(wrap_pyfunction!(get_unicode_category_groups, m)?)?;
    m.add_function(wrap_pyfunction!(count_unicode_categories, m)?)?;
    m.add_function(wrap_pyfunction!(count_unicode_category_groups, m)?)?;
    m.add_function(wrap_pyfunction!(get_unicode_category_ratios, m)?)?;
    m.add_function(wrap_pyfunction!(get_unicode_category_group_ratios, m)?)?;

    // Unicode category bigrams
    m.add_function(wrap_pyfunction!(get_unicode_category_bigrams, m)?)?;
    m.add_function(wrap_pyfunction!(get_unicode_category_bigram_ratios, m)?)?;
    m.add_function(wrap_pyfunction!(get_unicode_category_group_bigrams, m)?)?;
    m.add_function(wrap_pyfunction!(
        get_unicode_category_group_bigram_ratios,
        m
    )?)?;

    // Unicode category trigrams
    m.add_function(wrap_pyfunction!(get_unicode_category_trigrams, m)?)?;
    m.add_function(wrap_pyfunction!(get_unicode_category_trigram_ratios, m)?)?;
    m.add_function(wrap_pyfunction!(get_unicode_category_group_trigrams, m)?)?;
    m.add_function(wrap_pyfunction!(
        get_unicode_category_group_trigram_ratios,
        m
    )?)?;

    // Frequency counting functions (optimized)
    m.add_function(wrap_pyfunction!(get_char_frequency, m)?)?;
    m.add_function(wrap_pyfunction!(get_char_type_frequency, m)?)?;
    m.add_function(wrap_pyfunction!(get_unicode_category_frequency, m)?)?;
    m.add_function(wrap_pyfunction!(get_unicode_category_group_frequency, m)?)?;

    // Combined metrics
    m.add_function(wrap_pyfunction!(combined_char_metrics, m)?)?;
    m.add_function(wrap_pyfunction!(get_all_char_metrics, m)?)?;
    m.add_function(wrap_pyfunction!(get_all_pattern_metrics, m)?)?;
    m.add_function(wrap_pyfunction!(get_all_metrics, m)?)?;

    // Text segmentation functions
    m.add_function(wrap_pyfunction!(split_words, m)?)?;
    m.add_function(wrap_pyfunction!(split_lines, m)?)?;
    m.add_function(wrap_pyfunction!(segment_lines, m)?)?;
    m.add_function(wrap_pyfunction!(count_lines, m)?)?;
    m.add_function(wrap_pyfunction!(average_line_length, m)?)?;
    m.add_function(wrap_pyfunction!(split_paragraphs, m)?)?;
    m.add_function(wrap_pyfunction!(segment_paragraphs, m)?)?;
    m.add_function(wrap_pyfunction!(count_paragraphs, m)?)?;
    m.add_function(wrap_pyfunction!(average_paragraph_length, m)?)?;
    m.add_function(wrap_pyfunction!(average_word_length, m)?)?;
    m.add_function(wrap_pyfunction!(average_sentence_length, m)?)?;
    m.add_function(wrap_pyfunction!(segment_sentences, m)?)?;
    m.add_function(wrap_pyfunction!(count_section_strings, m)?)?;

    // Unigram tokenization functions
    m.add_function(wrap_pyfunction!(tokenize_unigrams, m)?)?;
    m.add_function(wrap_pyfunction!(tokenize_unigrams_with_punctuation, m)?)?;
    m.add_function(wrap_pyfunction!(count_unigram_tokens, m)?)?;
    m.add_function(wrap_pyfunction!(count_unique_unigrams, m)?)?;
    m.add_function(wrap_pyfunction!(unigram_type_token_ratio, m)?)?;
    m.add_function(wrap_pyfunction!(unigram_repetition_rate, m)?)?;
    m.add_function(wrap_pyfunction!(get_unigram_frequency, m)?)?;
    m.add_function(wrap_pyfunction!(unigram_entropy, m)?)?;
    m.add_function(wrap_pyfunction!(max_unigram_frequency_ratio, m)?)?;
    m.add_function(wrap_pyfunction!(hapax_legomena_ratio, m)?)?;
    m.add_function(wrap_pyfunction!(top_5_token_coverage, m)?)?;
    m.add_function(wrap_pyfunction!(short_token_ratio, m)?)?;
    m.add_function(wrap_pyfunction!(long_token_ratio, m)?)?;
    m.add_function(wrap_pyfunction!(get_all_unigram_metrics, m)?)?;

    // ML-based tokenization functions
    m.add_function(wrap_pyfunction!(tokenize_ml, m)?)?;
    m.add_function(wrap_pyfunction!(batch_tokenize_ml, m)?)?;
    m.add_function(wrap_pyfunction!(subword_token_count, m)?)?;
    m.add_function(wrap_pyfunction!(unique_subword_count, m)?)?;
    m.add_function(wrap_pyfunction!(subword_type_token_ratio, m)?)?;
    m.add_function(wrap_pyfunction!(subword_repetition_rate, m)?)?;
    m.add_function(wrap_pyfunction!(subword_entropy, m)?)?;
    m.add_function(wrap_pyfunction!(subword_efficiency, m)?)?;
    m.add_function(wrap_pyfunction!(get_token_metrics, m)?)?;

    // Compression metrics
    m.add_function(wrap_pyfunction!(compression_ratio, m)?)?;
    m.add_function(wrap_pyfunction!(get_compression_metrics, m)?)?;
    m.add_function(wrap_pyfunction!(unigram_compression_ratio, m)?)?;

    // Pattern matching functions
    m.add_function(wrap_pyfunction!(count_regex_matches, m)?)?;
    m.add_function(wrap_pyfunction!(contains_regex_pattern, m)?)?;
    m.add_function(wrap_pyfunction!(count_copyright_mentions, m)?)?;
    m.add_function(wrap_pyfunction!(count_rights_reserved, m)?)?;
    m.add_function(wrap_pyfunction!(count_section_strings, m)?)?;
    m.add_function(wrap_pyfunction!(count_question_strings, m)?)?;
    m.add_function(wrap_pyfunction!(count_interrogative_questions, m)?)?;
    m.add_function(wrap_pyfunction!(count_complex_interrogatives, m)?)?;
    m.add_function(wrap_pyfunction!(count_factual_statements, m)?)?;
    m.add_function(wrap_pyfunction!(count_logical_reasoning, m)?)?;
    m.add_function(wrap_pyfunction!(contains_code_characters, m)?)?;
    m.add_function(wrap_pyfunction!(bullet_or_ellipsis_lines_ratio, m)?)?;
    m.add_function(wrap_pyfunction!(contains_blacklist_substring, m)?)?;

    // Zipf's law and power distribution metrics
    m.add_function(wrap_pyfunction!(zipf_fitness_score, m)?)?;
    m.add_function(wrap_pyfunction!(power_law_exponent, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_burstiness, m)?)?;
    m.add_function(wrap_pyfunction!(analyze_vocab_growth, m)?)?;
    m.add_function(wrap_pyfunction!(get_zipf_metrics, m)?)?;

    Ok(())
}
