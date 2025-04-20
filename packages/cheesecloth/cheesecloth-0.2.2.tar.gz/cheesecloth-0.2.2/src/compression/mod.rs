//! # Compression-based Text Analysis
//!
//! This module provides text analysis functionality based on data compression,
//! which serves as a proxy for measuring information density and redundancy.
//!
//! ## Key Features
//!
//! * Compression ratio calculation (original size / compressed size)
//! * Token-based compression metrics
//! * Normalized and efficiency-based compression measures
//!
//! Compression-based metrics provide insights into text complexity and redundancy
//! that complement traditional statistical measures. They can detect subtle patterns
//! and repetitive structures that might not be apparent from frequency-based analysis
//! alone, making them useful for authorship analysis and content quality assessment.

use crate::unigram;
use flate2::write::DeflateEncoder;
use flate2::Compression;
use std::collections::HashMap;
use std::io::{self, Write};

/// Calculates the compression ratio of a string using deflate
///
/// The compression ratio is defined as: original_size / compressed_size
/// A higher ratio indicates more compressible (redundant) text
///
/// # Arguments
///
/// * `text` - The text to analyze
///
/// # Returns
///
/// The compression ratio
pub fn calculate_compression_ratio(text: &str) -> io::Result<f64> {
    // Handle empty text
    if text.is_empty() {
        return Ok(1.0);
    }

    let original_size = text.as_bytes().len();

    // Create a DeflateEncoder with maximum compression
    let mut encoder = DeflateEncoder::new(Vec::new(), Compression::best());

    // Write the text to be compressed
    encoder.write_all(text.as_bytes())?;

    // Finish the compression and get the compressed bytes
    let compressed = encoder.finish()?;
    let compressed_size = compressed.len();

    // Avoid division by zero
    if compressed_size == 0 {
        return Ok(f64::INFINITY);
    }

    Ok(original_size as f64 / compressed_size as f64)
}

/// Calculates the compression ratio of a string's tokens
///
/// This is similar to the regular compression ratio, but operates on word tokens
/// to better measure lexical redundancy rather than character-level redundancy.
///
/// # Arguments
///
/// * `text` - The text to analyze
/// * `include_punctuation` - Whether to include punctuation in tokenization
///
/// # Returns
///
/// The unigram compression ratio
pub fn unigram_compression_ratio(text: &str, include_punctuation: bool) -> io::Result<f64> {
    if text.is_empty() {
        return Ok(1.0);
    }

    // Get the tokens
    let tokens = if include_punctuation {
        unigram::tokenize_with_punctuation(text)
    } else {
        unigram::tokenize(text)
    };

    // Join tokens with spaces to standardize presentation
    let token_text = tokens.join(" ");

    // Then calculate compression ratio on this normalized text
    calculate_compression_ratio(&token_text)
}

/// Calculates additional compression metrics beyond basic ratio
///
/// This provides a more comprehensive view of text compressibility
/// by including both the regular and normalized compression ratios.
///
/// # Arguments
///
/// * `text` - The text to analyze
///
/// # Returns
///
/// A HashMap of compression metrics
pub fn get_compression_metrics(text: &str) -> io::Result<HashMap<String, f64>> {
    let mut metrics = HashMap::new();

    // Basic compression ratio
    let ratio = calculate_compression_ratio(text)?;
    metrics.insert("compression_ratio".to_string(), ratio);

    // Unigram compression ratios (with and without punctuation)
    let unigram_ratio = unigram_compression_ratio(text, false)?;
    metrics.insert("unigram_compression_ratio".to_string(), unigram_ratio);

    let unigram_punct_ratio = unigram_compression_ratio(text, true)?;
    metrics.insert(
        "unigram_compression_ratio_with_punct".to_string(),
        unigram_punct_ratio,
    );

    // Calculate normalized ratio (compression relative to random text of similar characteristics)
    // This is a simple approximation - in a complete implementation, you would compare to
    // randomly generated text with similar character distributions
    let normalized_ratio = if ratio > 1.0 {
        (ratio - 1.0) / 9.0
    } else {
        0.0
    };
    metrics.insert("normalized_compression_ratio".to_string(), normalized_ratio);

    // Compression efficiency - how much is actually saved by compression
    let efficiency = if ratio > 1.0 {
        1.0 - (1.0 / ratio)
    } else {
        0.0
    };
    metrics.insert("compression_efficiency".to_string(), efficiency);

    Ok(metrics)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_compression_ratio() {
        // Highly compressible text (repeated pattern)
        let repetitive_text = "aaaaaaaaaaaaaaaaaaaaaaaaaaaa";
        let ratio1 = calculate_compression_ratio(repetitive_text).unwrap();
        assert!(
            ratio1 > 5.0,
            "Highly repetitive text should have high compression ratio"
        );

        // Random text (less compressible)
        let random_text = "The quick brown fox jumps over the lazy dog";
        let ratio2 = calculate_compression_ratio(random_text).unwrap();
        assert!(
            ratio2 < ratio1,
            "Random text should be less compressible than repetitive text"
        );

        // Empty text edge case
        let empty_text = "";
        let ratio3 = calculate_compression_ratio(empty_text).unwrap();
        assert_eq!(
            ratio3, 1.0,
            "Empty text should have compression ratio of 1.0"
        );
    }

    #[test]
    fn test_unigram_compression_ratio() {
        // Test with text containing repeated words
        let text_with_repeated_words = "the the the the cat cat cat sat sat on on the the mat";
        let ratio = unigram_compression_ratio(text_with_repeated_words, false).unwrap();
        assert!(
            ratio > 1.5,
            "Text with repeated words should have high unigram compression ratio"
        );

        // Compare with and without punctuation
        let text_with_punct = "Hello, world! How are you? I am fine, thanks!";
        let ratio_no_punct = unigram_compression_ratio(text_with_punct, false).unwrap();
        let ratio_with_punct = unigram_compression_ratio(text_with_punct, true).unwrap();

        // Results should be different
        assert!(
            ratio_no_punct != ratio_with_punct,
            "Including punctuation should change the compression ratio"
        );
    }

    #[test]
    fn test_get_compression_metrics() {
        let text =
            "This is a test of the compression metrics. This text has some repetition in it.";
        let metrics = get_compression_metrics(text).unwrap();

        // Check that all expected metrics are present
        assert!(metrics.contains_key("compression_ratio"));
        assert!(metrics.contains_key("unigram_compression_ratio"));
        assert!(metrics.contains_key("unigram_compression_ratio_with_punct"));
        assert!(metrics.contains_key("normalized_compression_ratio"));
        assert!(metrics.contains_key("compression_efficiency"));

        // Sanity check on values
        assert!(
            metrics["compression_ratio"] > 1.0,
            "Compression ratio should be > 1 for normal text"
        );
        assert!(
            metrics["compression_efficiency"] > 0.0,
            "Compression efficiency should be positive"
        );
        assert!(
            metrics["compression_efficiency"] < 1.0,
            "Compression efficiency should be < 1"
        );
    }
}
