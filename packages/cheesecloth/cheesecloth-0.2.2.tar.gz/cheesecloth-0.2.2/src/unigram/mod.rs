//! # Unigram Tokenization and Analysis
//!
//! This module provides functionality for tokenizing text into unigrams (linguistic words)
//! based on Unicode segmentation rules, and analyzing these tokens with various metrics.
//!
//! ## Key Features
//!
//! * Unicode-aware word tokenization
//! * Options for including/excluding punctuation
//! * Token frequency analysis
//! * Lexical diversity metrics (type-token ratio, repetition rate)
//! * Information-theoretic measures (entropy)
//!
//! Unlike subword tokenization used in machine learning models, unigram tokenization
//! follows linguistic word boundaries, making it useful for stylometric analysis,
//! readability assessment, and author identification.

use std::collections::{HashMap, HashSet};
use unicode_segmentation::UnicodeSegmentation;

/// Tokenizes a text into unigram tokens (words and punctuation).
///
/// This function splits text into tokens based on Unicode word boundaries,
/// preserving words, numbers, and punctuation as separate tokens.
///
/// # Arguments
///
/// * `text` - The input text to tokenize
///
/// # Returns
///
/// A vector of string tokens
pub fn tokenize(text: &str) -> Vec<String> {
    // Use unicode_segmentation to split text into words
    let tokens: Vec<String> = UnicodeSegmentation::unicode_words(text)
        .map(|s| s.to_string())
        .collect();

    tokens
}

/// Tokenizes a text into unigram tokens, including words, punctuation, and whitespace.
///
/// Unlike the `tokenize` function, this preserves all characters including punctuation
/// and whitespace as separate tokens, providing a complete representation of the text.
///
/// # Arguments
///
/// * `text` - The input text to tokenize with preservation of all characters
///
/// # Returns
///
/// A vector of string tokens
pub fn tokenize_with_punctuation(text: &str) -> Vec<String> {
    use std::ops::Not;

    // Handle empty text
    if text.is_empty() {
        return Vec::new();
    }

    // A more customized tokenization that separates punctuation from words
    let mut tokens = Vec::new();
    let mut current_token = String::new();
    let mut current_is_punct = None;

    for ch in text.chars() {
        let is_punct = ch.is_ascii_punctuation() || ch.is_whitespace();

        match current_is_punct {
            None => {
                current_token.push(ch);
                current_is_punct = Some(is_punct);
            }
            Some(prev_is_punct) if prev_is_punct == is_punct => {
                // Continue current token if same type
                current_token.push(ch);
            }
            Some(_) => {
                // Switch token type
                if !current_token.is_empty() {
                    tokens.push(current_token);
                    current_token = String::new();
                }
                current_token.push(ch);
                current_is_punct = Some(is_punct);
            }
        }
    }

    // Add the last token if not empty
    if !current_token.is_empty() {
        tokens.push(current_token);
    }

    // If text has period in the middle, further split
    let mut final_tokens = Vec::new();
    for token in tokens {
        if token.len() > 1
            && token.chars().any(|c| c.is_ascii_punctuation())
            && token.chars().any(|c| c.is_ascii_punctuation().not())
        {
            // This is a token that contains both punctuation and non-punctuation
            let mut current = String::new();
            let mut is_punct = None;

            for ch in token.chars() {
                let ch_is_punct = ch.is_ascii_punctuation();

                match is_punct {
                    None => {
                        current.push(ch);
                        is_punct = Some(ch_is_punct);
                    }
                    Some(prev_is_punct) if prev_is_punct == ch_is_punct => {
                        current.push(ch);
                    }
                    Some(_) => {
                        if !current.is_empty() {
                            final_tokens.push(current);
                            current = String::new();
                        }
                        current.push(ch);
                        is_punct = Some(ch_is_punct);
                    }
                }
            }

            if !current.is_empty() {
                final_tokens.push(current);
            }
        } else {
            final_tokens.push(token);
        }
    }

    final_tokens
}

/// Counts the total number of unigram tokens in a text.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
///
/// # Returns
///
/// The count of tokens in the text
pub fn count_tokens(text: &str, include_punctuation: bool) -> usize {
    if include_punctuation {
        tokenize_with_punctuation(text).len()
    } else {
        tokenize(text).len()
    }
}

/// Counts the number of unique unigram tokens in a text.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// The count of unique tokens in the text
pub fn count_unique_tokens(text: &str, include_punctuation: bool, case_sensitive: bool) -> usize {
    let tokens = if include_punctuation {
        tokenize_with_punctuation(text)
    } else {
        tokenize(text)
    };

    let mut unique_tokens = HashSet::new();

    for token in tokens {
        if case_sensitive {
            unique_tokens.insert(token);
        } else {
            unique_tokens.insert(token.to_lowercase());
        }
    }

    unique_tokens.len()
}

/// Calculates the type-token ratio (unique tokens / total tokens) for a text.
///
/// This is a measure of lexical diversity. Higher values indicate more diverse vocabulary.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// The type-token ratio (between 0.0 and 1.0)
pub fn type_token_ratio(text: &str, include_punctuation: bool, case_sensitive: bool) -> f64 {
    let tokens = if include_punctuation {
        tokenize_with_punctuation(text)
    } else {
        tokenize(text)
    };

    if tokens.is_empty() {
        return 0.0;
    }

    let total_tokens = tokens.len();
    let unique_count = count_unique_tokens(text, include_punctuation, case_sensitive);

    unique_count as f64 / total_tokens as f64
}

/// Calculates the repetition rate (1 - unique tokens / total tokens) for a text.
///
/// Higher values indicate more repetition in the text.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// The repetition rate (between 0.0 and 1.0)
pub fn repetition_rate(text: &str, include_punctuation: bool, case_sensitive: bool) -> f64 {
    let tokens = if include_punctuation {
        tokenize_with_punctuation(text)
    } else {
        tokenize(text)
    };

    // Return 0.0 for empty text (no repetition)
    if tokens.is_empty() {
        return 0.0;
    }

    1.0 - type_token_ratio(text, include_punctuation, case_sensitive)
}

/// Counts the frequency of each token in the text.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// A HashMap where keys are tokens and values are occurrence counts
pub fn token_frequency(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> HashMap<String, usize> {
    let tokens = if include_punctuation {
        tokenize_with_punctuation(text)
    } else {
        tokenize(text)
    };

    let mut frequency_map = HashMap::new();

    for token in tokens {
        let key = if case_sensitive {
            token
        } else {
            token.to_lowercase()
        };

        *frequency_map.entry(key).or_insert(0) += 1;
    }

    frequency_map
}

/// Calculates the Shannon entropy of the unigram token distribution.
///
/// This measures the predictability or information content of text.
/// Higher values indicate more unpredictable text with evenly distributed tokens.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// The Shannon entropy value
pub fn token_entropy(text: &str, include_punctuation: bool, case_sensitive: bool) -> f64 {
    let frequency = token_frequency(text, include_punctuation, case_sensitive);

    if frequency.is_empty() {
        return 0.0;
    }

    let total_tokens: usize = frequency.values().sum();
    let total_tokens_f64 = total_tokens as f64;

    // Calculate entropy using Shannon's formula: -sum(p_i * log2(p_i))
    let mut entropy = 0.0;
    for &count in frequency.values() {
        let probability = count as f64 / total_tokens_f64;
        entropy -= probability * probability.log2();
    }

    entropy
}

/// Calculates the maximum token frequency ratio in a text.
///
/// This is the ratio of the most common token's frequency to the total token count.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// The maximum token frequency ratio (between 0.0 and 1.0)
pub fn max_token_frequency_ratio(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> f64 {
    let frequency = token_frequency(text, include_punctuation, case_sensitive);

    if frequency.is_empty() {
        return 0.0;
    }

    let total_tokens: usize = frequency.values().sum();
    let max_frequency = frequency.values().max().unwrap_or(&0);

    *max_frequency as f64 / total_tokens as f64
}

/// Calculates the hapax legomena ratio in a text.
///
/// Hapax legomena are words that appear exactly once in the text.
/// This ratio is the number of hapax legomena divided by the total token count.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// The hapax legomena ratio (between 0.0 and 1.0)
pub fn hapax_legomena_ratio(text: &str, include_punctuation: bool, case_sensitive: bool) -> f64 {
    let frequency = token_frequency(text, include_punctuation, case_sensitive);

    if frequency.is_empty() {
        return 0.0;
    }

    let total_tokens: usize = frequency.values().sum();
    let hapax_count = frequency.values().filter(|&&count| count == 1).count();

    hapax_count as f64 / total_tokens as f64
}

/// Calculates the top-5 token coverage in a text.
///
/// This is the percentage of the text covered by the 5 most frequent tokens.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// The top-5 token coverage (between 0.0 and 1.0)
pub fn top_5_token_coverage(text: &str, include_punctuation: bool, case_sensitive: bool) -> f64 {
    let frequency = token_frequency(text, include_punctuation, case_sensitive);

    if frequency.is_empty() {
        return 0.0;
    }

    let total_tokens: usize = frequency.values().sum();

    // Convert the values to a vector and sort in descending order
    let mut counts: Vec<usize> = frequency.values().cloned().collect();
    counts.sort_unstable_by(|a, b| b.cmp(a));

    // Take the top 5 tokens (or fewer if there aren't 5)
    let top_5_sum: usize = counts.iter().take(5).sum();

    top_5_sum as f64 / total_tokens as f64
}

/// Calculates the ratio of short tokens (3 characters or fewer by default) in a text.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
/// * `threshold` - Optional maximum length for "short" tokens, defaults to 3 if None
///
/// # Returns
///
/// The short token ratio (between 0.0 and 1.0)
///
/// # Notes
///
/// * Tokenization follows Unicode segmentation rules:
///   - With `include_punctuation=false`: Punctuation is ignored and used as boundaries
///   - With `include_punctuation=true`: Each punctuation character is a separate token
/// * Whitespace is always used as a token separator and never counted as a token
/// * Empty strings return a ratio of 0.0
pub fn short_token_ratio(
    text: &str,
    include_punctuation: bool,
    _case_sensitive: bool, // Unused but kept for API consistency
    threshold: Option<usize>, // New parameter
) -> f64 {
    let threshold = threshold.unwrap_or(3);
    
    let tokens = if include_punctuation {
        tokenize_with_punctuation(text)
    } else {
        tokenize(text)
    };

    if tokens.is_empty() {
        return 0.0;
    }

    // Clone the tokens for iterating to avoid ownership issues
    let tokens_vec = tokens.clone();
    let short_count = tokens_vec.iter().filter(|token| token.len() <= threshold).count();

    short_count as f64 / tokens.len() as f64
}

/// Calculates the ratio of short tokens (3 characters or fewer) in a text.
/// This is a convenience wrapper around short_token_ratio with the default threshold.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// The short token ratio (between 0.0 and 1.0)
pub fn short_token_ratio_default(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> f64 {
    short_token_ratio(text, include_punctuation, case_sensitive, None)
}

/// Calculates the ratio of long tokens (7 characters or more by default) in a text.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
/// * `threshold` - Optional minimum length for "long" tokens, defaults to 7 if None
///
/// # Returns
///
/// The long token ratio (between 0.0 and 1.0)
///
/// # Notes
///
/// * Tokenization follows Unicode segmentation rules:
///   - With `include_punctuation=false`: Punctuation is ignored and used as boundaries
///   - With `include_punctuation=true`: Each punctuation character is a separate token
/// * Whitespace is always used as a token separator and never counted as a token
/// * Empty strings return a ratio of 0.0
pub fn long_token_ratio(
    text: &str,
    include_punctuation: bool,
    _case_sensitive: bool, // Unused but kept for API consistency
    threshold: Option<usize>, // New parameter
) -> f64 {
    let threshold = threshold.unwrap_or(7);
    
    let tokens = if include_punctuation {
        tokenize_with_punctuation(text)
    } else {
        tokenize(text)
    };

    if tokens.is_empty() {
        return 0.0;
    }

    // Clone the tokens for iterating to avoid ownership issues
    let tokens_vec = tokens.clone();
    let long_count = tokens_vec.iter().filter(|token| token.len() >= threshold).count();

    long_count as f64 / tokens.len() as f64
}

/// Calculates the ratio of long tokens (7 characters or more) in a text.
/// This is a convenience wrapper around long_token_ratio with the default threshold.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// The long token ratio (between 0.0 and 1.0)
pub fn long_token_ratio_default(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> f64 {
    long_token_ratio(text, include_punctuation, case_sensitive, None)
}

/// A struct that holds all unigram metrics for efficient calculation.
/// This minimizes passes through the text and improves performance.
pub struct UnigramMetrics {
    pub token_count: usize,
    pub unique_token_count: usize,
    pub type_token_ratio: f64,
    pub repetition_rate: f64,
    pub token_entropy: f64,
    pub max_frequency_ratio: f64,
    pub average_token_length: f64,
    pub hapax_legomena_ratio: f64,
    pub top_5_token_coverage: f64,
    pub short_token_ratio: f64,
    pub long_token_ratio: f64,
    // No longer needed as a field since it's only used during calculation
}

/// Calculates all unigram metrics in a single pass through the text.
///
/// This is significantly more efficient than calling individual metric functions,
/// especially for longer texts, as it minimizes passes and calculations.
///
/// # Arguments
///
/// * `text` - The input text to analyze
/// * `include_punctuation` - Whether to include punctuation in the token count
/// * `case_sensitive` - Whether to treat uppercase and lowercase as different tokens
///
/// # Returns
///
/// A UnigramMetrics struct containing all calculated metrics
pub fn calculate_all_unigram_metrics(
    text: &str,
    include_punctuation: bool,
    case_sensitive: bool,
) -> UnigramMetrics {
    // Get tokens (with or without punctuation)
    let tokens = if include_punctuation {
        tokenize_with_punctuation(text)
    } else {
        tokenize(text)
    };

    // Handle empty text case
    if tokens.is_empty() {
        return UnigramMetrics {
            token_count: 0,
            unique_token_count: 0,
            type_token_ratio: 0.0,
            repetition_rate: 0.0,
            token_entropy: 0.0,
            max_frequency_ratio: 0.0,
            average_token_length: 0.0,
            hapax_legomena_ratio: 0.0,
            top_5_token_coverage: 0.0,
            short_token_ratio: 0.0,
            long_token_ratio: 0.0,
        };
    }

    // Calculate token frequency in a single pass
    let mut frequency_map = HashMap::new();
    let token_count = tokens.len();
    let mut total_token_length = 0;

    // Store a clone of tokens for later use
    let tokens_clone = tokens.clone();

    for token in &tokens {
        total_token_length += token.len();
        let key = if case_sensitive {
            token.clone()
        } else {
            token.to_lowercase()
        };

        *frequency_map.entry(key).or_insert(0) += 1;
    }

    let unique_token_count = frequency_map.len();
    let total_tokens_f64 = token_count as f64;

    // Calculate type-token ratio
    let type_token_ratio = unique_token_count as f64 / total_tokens_f64;

    // Calculate repetition rate
    let repetition_rate = 1.0 - type_token_ratio;

    // Calculate entropy
    let mut entropy = 0.0;
    let mut max_frequency = 0;

    for &count in frequency_map.values() {
        if count > max_frequency {
            max_frequency = count;
        }

        let probability = count as f64 / total_tokens_f64;
        entropy -= probability * probability.log2();
    }

    // Calculate max frequency ratio
    let max_frequency_ratio = max_frequency as f64 / total_tokens_f64;

    // Calculate average token length
    let average_token_length = if token_count > 0 {
        total_token_length as f64 / token_count as f64
    } else {
        0.0
    };

    // Calculate hapax legomena ratio
    let hapax_count = frequency_map.values().filter(|&&count| count == 1).count();
    let hapax_legomena_ratio = hapax_count as f64 / token_count as f64;

    // Calculate top-5 token coverage
    let mut counts: Vec<usize> = frequency_map.values().cloned().collect();
    counts.sort_unstable_by(|a, b| b.cmp(a));
    let top_5_sum: usize = counts.iter().take(5).sum();
    let top_5_token_coverage = top_5_sum as f64 / token_count as f64;

    // Calculate short token ratio and long token ratio
    // Use default thresholds (3 for short, 7 for long)
    let short_count = tokens_clone.iter().filter(|token| token.len() <= 3).count();
    let long_count = tokens_clone.iter().filter(|token| token.len() >= 7).count();
    let short_token_ratio = short_count as f64 / token_count as f64;
    let long_token_ratio = long_count as f64 / token_count as f64;

    UnigramMetrics {
        token_count,
        unique_token_count,
        type_token_ratio,
        repetition_rate,
        token_entropy: entropy,
        max_frequency_ratio,
        average_token_length,
        hapax_legomena_ratio,
        top_5_token_coverage,
        short_token_ratio,
        long_token_ratio,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tokenize() {
        let text = "Hello, world! This is a test.";
        let tokens = tokenize(text);
        assert_eq!(tokens, vec!["Hello", "world", "This", "is", "a", "test"]);
    }

    #[test]
    fn test_tokenize_with_punctuation() {
        let text = "Hello, world!";
        let tokens = tokenize_with_punctuation(text);
        assert_eq!(tokens, vec!["Hello", ",", " ", "world", "!"]);
    }

    #[test]
    fn test_count_tokens() {
        let text = "Hello, world! This is a test.";
        assert_eq!(count_tokens(text, false), 6);
        assert_eq!(count_tokens(text, true), 14); // Including punctuation and spaces as separate tokens
    }

    #[test]
    fn test_count_unique_tokens() {
        let text = "The cat and the dog. The cat ran.";
        // Without punctuation, case insensitive
        assert_eq!(count_unique_tokens(text, false, false), 5); // the, cat, and, dog, ran
                                                                // With punctuation, case insensitive
        assert_eq!(count_unique_tokens(text, true, false), 7); // includes ".", " " and punctuation
                                                               // Without punctuation, case sensitive
        assert_eq!(count_unique_tokens(text, false, true), 6); // "The" and "the" are different
    }

    #[test]
    fn test_type_token_ratio() {
        let text = "The cat and the dog. The cat ran.";
        // 5 unique tokens / 8 total tokens = 0.625
        let ratio = type_token_ratio(text, false, false);
        assert!((ratio - 0.625).abs() < 1e-10);
    }

    #[test]
    fn test_repetition_rate() {
        let text = "The cat and the dog. The cat ran.";
        // 1 - (5 unique tokens / 8 total tokens) = 0.375
        let rate = repetition_rate(text, false, false);
        assert!((rate - 0.375).abs() < 1e-10);
    }

    #[test]
    fn test_token_frequency() {
        let text = "The cat and the dog. The cat ran.";
        let frequency = token_frequency(text, false, false);

        assert_eq!(frequency.get("the").unwrap(), &3);
        assert_eq!(frequency.get("cat").unwrap(), &2);
        assert_eq!(frequency.get("dog").unwrap(), &1);
    }

    #[test]
    fn test_token_entropy() {
        // For a text with uniform distribution (all tokens different), entropy is log2(n)
        let text = "one two three four five";
        let entropy = token_entropy(text, false, true);
        assert!((entropy - 2.32192809489).abs() < 1e-8); // log2(5) = 2.32192809489

        // For a text with all the same token, entropy is 0
        let uniform_text = "one one one one one";
        let uniform_entropy = token_entropy(uniform_text, false, true);
        assert!(uniform_entropy.abs() < 1e-10);
    }

    #[test]
    fn test_max_token_frequency_ratio() {
        let text = "The cat and the dog. The cat ran.";
        // "the" appears 3 times out of 8 tokens
        let ratio = max_token_frequency_ratio(text, false, false);
        assert!((ratio - 0.375).abs() < 1e-10);
    }

    #[test]
    fn test_hapax_legomena_ratio() {
        let text = "The cat and the dog. The cat ran.";
        // 3 hapax words (and, dog, ran) out of 8 tokens
        let ratio = hapax_legomena_ratio(text, false, false);
        assert!((ratio - 0.375).abs() < 1e-10);

        // Test case with no hapax
        let text2 = "one one one two two";
        let ratio2 = hapax_legomena_ratio(text2, false, true);
        assert!((ratio2 - 0.0).abs() < 1e-10);
    }

    #[test]
    fn test_top_5_token_coverage() {
        let text = "The cat and the dog. The cat ran quickly past the fence.";
        // Tokens: the (4), cat (2), and, dog, ran, quickly, past, fence (1 each)
        // Top 5: the (4), cat (2), and (1), dog (1), ran (1) = 9 out of 12 tokens
        let ratio = top_5_token_coverage(text, false, false);
        assert!((ratio - 0.75).abs() < 1e-10);

        // Test with fewer than 5 unique tokens
        let text2 = "one two three";
        // 3 unique tokens, all should be covered (100%)
        let ratio2 = top_5_token_coverage(text2, false, true);
        assert!((ratio2 - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_short_token_ratio() {
        let text = "The cat and the dog ran. I am glad.";
        // Expected tokens with include_punctuation=false: 
        // ["The", "cat", "and", "the", "dog", "ran", "I", "am", "glad"]
        // Short tokens (≤3): "cat", "and", "the", "dog", "ran", "I", "am", "The" = 8 out of 9
        
        // First verify tokens match our expectation
        let tokens = tokenize(text);
        assert_eq!(tokens.len(), 9, "Expected 9 tokens, got {}: {:?}", tokens.len(), tokens);
        
        let short_count = tokens.iter().filter(|token| token.len() <= 3).count();
        assert_eq!(short_count, 8, "Expected 8 tokens of length ≤3, got {}", short_count);
        
        // Calculate ratio
        let expected_ratio = 8.0 / 9.0;
        let ratio = short_token_ratio(text, false, false, None);
        assert!((ratio - expected_ratio).abs() < 1e-10, 
                "Expected ratio {}, got {}", expected_ratio, ratio);
    }

    #[test]
    fn test_long_token_ratio() {
        let text = "Extraordinary vocabulary demonstrates sophisticated communication abilities.";
        // Expected tokens with include_punctuation=false: 
        // ["Extraordinary", "vocabulary", "demonstrates", "sophisticated", "communication", "abilities"]
        // Long tokens (≥7): All 6 out of 6
        
        // First verify tokens match our expectation
        let tokens = tokenize(text);
        assert_eq!(tokens.len(), 6, "Expected 6 tokens, got {}: {:?}", tokens.len(), tokens);
        
        let long_count = tokens.iter().filter(|token| token.len() >= 7).count();
        assert_eq!(long_count, 6, "Expected 6 tokens of length ≥7, got {}", long_count);
        
        // Calculate ratio
        let expected_ratio = 6.0 / 6.0;
        let ratio = long_token_ratio(text, false, false, None);
        assert!((ratio - expected_ratio).abs() < 1e-10, 
                "Expected ratio {}, got {}", expected_ratio, ratio);
    }

    #[test]
    fn test_calculate_all_unigram_metrics() {
        let text = "The cat and the dog. The cat ran quickly.";
        
        // First verify tokens to ensure we understand what's being calculated
        let tokens = tokenize(text);
        println!("Tokens: {:?}", tokens);
        
        // Expected tokens with include_punctuation=false: 
        // ["The", "cat", "and", "the", "dog", "The", "cat", "ran", "quickly"]
        
        let unique_tokens: HashSet<String> = tokens.iter()
            .map(|t| t.to_lowercase())
            .collect();
        println!("Unique tokens (case-insensitive): {:?}", unique_tokens);
        // Expected unique tokens (case insensitive): 
        // ["the", "cat", "and", "dog", "ran", "quickly"]
        
        let metrics = calculate_all_unigram_metrics(text, false, false);

        // Verify basic metrics
        assert_eq!(metrics.token_count, 9, "Expected 9 tokens, got {}", metrics.token_count);
        assert_eq!(metrics.unique_token_count, 6, 
            "Expected 6 unique tokens (case-insensitive), got {}", metrics.unique_token_count);

        // Verify our new metrics
        let expected_hapax_ratio = 4.0 / 9.0; // and, dog, ran, quickly are hapax legomena
        assert!((metrics.hapax_legomena_ratio - expected_hapax_ratio).abs() < 1e-10,
            "Expected hapax ratio {}, got {}", expected_hapax_ratio, metrics.hapax_legomena_ratio);

        let expected_top5_coverage = 8.0 / 9.0; // the (3), cat (2), and, dog, ran = 8 out of 9
        assert!((metrics.top_5_token_coverage - expected_top5_coverage).abs() < 1e-10,
            "Expected top5 coverage {}, got {}", expected_top5_coverage, metrics.top_5_token_coverage);

        // Count short tokens (≤3): the, cat, and, dog, ran = 6 out of 9
        let short_count = tokens.iter()
            .filter(|t| t.len() <= 3)
            .count();
        println!("Short tokens (≤3): {:?}", tokens.iter().filter(|t| t.len() <= 3).collect::<Vec<_>>());
        let expected_short_ratio = short_count as f64 / tokens.len() as f64;
        
        assert!((metrics.short_token_ratio - expected_short_ratio).abs() < 1e-10,
            "Expected short token ratio {}, got {}", expected_short_ratio, metrics.short_token_ratio);

        // Count long tokens (≥7): quickly = 1 out of 9
        let long_count = tokens.iter()
            .filter(|t| t.len() >= 7)
            .count();
        println!("Long tokens (≥7): {:?}", tokens.iter().filter(|t| t.len() >= 7).collect::<Vec<_>>());
        let expected_long_ratio = long_count as f64 / tokens.len() as f64;
        
        assert!((metrics.long_token_ratio - expected_long_ratio).abs() < 1e-10,
            "Expected long token ratio {}, got {}", expected_long_ratio, metrics.long_token_ratio);
    }
}
