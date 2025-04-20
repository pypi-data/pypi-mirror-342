//! # Unicode Character Analysis
//!
//! This module provides fundamental character-level analysis functions for text,
//! focusing on efficient classification, counting, and statistical measures.
//!
//! ## Key Features
//!
//! * Character classification: letters, digits, punctuation, symbols, whitespace
//! * Character counts and ratios: total, letters, digits, ASCII, etc.
//! * Statistical measures: entropy, frequency distributions
//! * Optimized for performance with minimal allocations
//!
//! These functions form the foundation for higher-level text analysis by providing
//! accurate and efficient character-level metrics.

use std::collections::HashSet;
use unicode_categories::UnicodeCategories;

/// Checks if a character is a letter (alphabetic)
pub fn is_letter(ch: char) -> bool {
    ch.is_alphabetic()
}

/// Checks if a character is a digit
pub fn is_digit(ch: char) -> bool {
    ch.is_numeric()
}

/// Checks if a character is a punctuation
pub fn is_punctuation(ch: char) -> bool {
    // Exclude specific characters that we want to classify as symbols
    if is_symbol(ch) {
        return false;
    }
    ch.is_ascii_punctuation() || (!ch.is_ascii() && ch.is_punctuation())
}

/// Checks if a character is a symbol
pub fn is_symbol(ch: char) -> bool {
    match ch {
        '+' | '<' | '=' | '>' | '^' | '|' | '~' | '$' | '%' | '¢' | '£' | '¤' | '¥' | '©' | '®'
        | '™' => true,
        _ if !ch.is_ascii() => {
            // For non-ASCII, check if it's a symbol according to Unicode
            ch.is_symbol()
        }
        _ => false,
    }
}

/// Checks if a character is whitespace
pub fn is_whitespace(ch: char) -> bool {
    ch.is_whitespace()
}

/// Checks if a character is uppercase
pub fn is_uppercase(ch: char) -> bool {
    ch.is_uppercase()
}

/// Checks if a character is lowercase
pub fn is_lowercase(ch: char) -> bool {
    ch.is_lowercase()
}

/// Checks if a character is alphanumeric (letter or digit)
pub fn is_alphanumeric(ch: char) -> bool {
    ch.is_alphanumeric()
}

/// Counts the number of letters (alphabetic characters) in a string
pub fn count_letters(text: &str) -> usize {
    text.chars().filter(|&c| is_letter(c)).count()
}

/// Counts the number of digits in a string
pub fn count_digits(text: &str) -> usize {
    text.chars().filter(|&c| is_digit(c)).count()
}

/// Counts the number of punctuation characters in a string
pub fn count_punctuation(text: &str) -> usize {
    text.chars().filter(|&c| is_punctuation(c)).count()
}

/// Counts the number of symbol characters in a string
pub fn count_symbols(text: &str) -> usize {
    text.chars().filter(|&c| is_symbol(c)).count()
}

/// Counts the number of whitespace characters in a string
pub fn count_whitespace(text: &str) -> usize {
    text.chars().filter(|&c| is_whitespace(c)).count()
}

/// Counts the number of uppercase characters in a string
pub fn count_uppercase(text: &str) -> usize {
    text.chars().filter(|&c| is_uppercase(c)).count()
}

/// Counts the number of lowercase characters in a string
pub fn count_lowercase(text: &str) -> usize {
    text.chars().filter(|&c| is_lowercase(c)).count()
}

/// Counts the number of alphanumeric characters in a string
pub fn count_alphanumeric(text: &str) -> usize {
    text.chars().filter(|&c| is_alphanumeric(c)).count()
}

/// Calculates the ratio of alphanumeric characters to all characters in a string
pub fn ratio_alphanumeric(text: &str) -> f64 {
    if text.is_empty() {
        return 0.0;
    }

    let total_chars = text.chars().count();
    let alphanumeric_count = count_alphanumeric(text);
    alphanumeric_count as f64 / total_chars as f64
}

/// Calculates the ratio of whitespace characters to all characters in a string
pub fn ratio_whitespace(text: &str) -> f64 {
    if text.is_empty() {
        return 0.0;
    }

    let total_chars = text.chars().count();
    let whitespace_count = count_whitespace(text);
    whitespace_count as f64 / total_chars as f64
}

/// Calculates the ratio of digit characters to all characters in a string
pub fn ratio_digits(text: &str) -> f64 {
    if text.is_empty() {
        return 0.0;
    }

    let total_chars = text.chars().count();
    let digit_count = count_digits(text);
    digit_count as f64 / total_chars as f64
}

/// Calculates the ratio of punctuation characters to all characters in a string
pub fn ratio_punctuation(text: &str) -> f64 {
    if text.is_empty() {
        return 0.0;
    }

    let total_chars = text.chars().count();
    let punctuation_count = count_punctuation(text);
    punctuation_count as f64 / total_chars as f64
}

/// Calculates the ratio of alphabetic to numeric characters in a string
pub fn ratio_alpha_to_numeric(text: &str) -> f64 {
    if text.is_empty() {
        return 0.0;
    }

    let digit_count = count_digits(text);
    let letter_count = count_letters(text);

    if digit_count == 0 {
        // Return 0.0 for consistent handling when denominator is zero
        return if letter_count == 0 {
            0.0
        } else {
            // Use a large but finite number instead of infinity
            1e6 * letter_count as f64
        };
    }

    letter_count as f64 / digit_count as f64
}

/// 1. Character Case Ratio - Ratio of uppercase to lowercase letters (not just to all letters)
///
///    Returns the ratio of uppercase letters to lowercase letters in the text
pub fn case_ratio(text: &str) -> f64 {
    let uppercase_count = count_uppercase(text);
    let lowercase_count = count_lowercase(text);

    if lowercase_count == 0 {
        if uppercase_count == 0 {
            return 0.0; // No letters
        } else {
            return 1e6 * uppercase_count as f64; // Large number instead of infinity
        }
    }

    uppercase_count as f64 / lowercase_count as f64
}

/// 2. Character Type Transitions - Count transitions between different character types
///
///    Returns a count of how many times the character type changes in the text
pub fn count_char_type_transitions(text: &str) -> usize {
    if text.is_empty() {
        return 0;
    }

    let chars: Vec<char> = text.chars().collect();
    if chars.len() < 2 {
        return 0;
    }

    let mut transitions = 0;
    let mut current_type = get_char_type(&chars[0]);

    for c in chars.iter().skip(1) {
        let next_type = get_char_type(c);
        if next_type != current_type {
            transitions += 1;
            current_type = next_type;
        }
    }

    transitions
}

/// Helper function to get the type of a character for transitions
fn get_char_type(c: &char) -> u8 {
    if is_letter(*c) {
        if is_uppercase(*c) {
            1 // uppercase letter
        } else {
            2 // lowercase letter
        }
    } else if is_digit(*c) {
        3 // digit
    } else if is_punctuation(*c) {
        4 // punctuation
    } else if is_symbol(*c) {
        5 // symbol
    } else if is_whitespace(*c) {
        6 // whitespace
    } else {
        7 // other
    }
}

/// 3. Character Runs - Count runs of consecutive same character types
///
///    Returns the count of sequences where the character type doesn't change
pub fn count_consecutive_runs(text: &str) -> usize {
    if text.is_empty() {
        return 0;
    }

    let chars: Vec<char> = text.chars().collect();
    if chars.len() == 1 {
        return 1;
    }

    let mut runs = 1; // Start with one run
    let mut current_type = get_char_type(&chars[0]);

    for c in chars.iter().skip(1) {
        let next_type = get_char_type(c);
        if next_type != current_type {
            runs += 1;
            current_type = next_type;
        }
    }

    runs
}

/// 5. Punctuation Diversity - Count unique punctuation marks
///
///    Returns the count of distinct punctuation characters in the text
pub fn punctuation_diversity(text: &str) -> usize {
    let mut unique_punctuation = HashSet::new();

    for c in text.chars() {
        if is_punctuation(c) {
            unique_punctuation.insert(c);
        }
    }

    unique_punctuation.len()
}

/// 8. Category/Group Entropy - Shannon entropy of Unicode categories
///
///    Calculates the entropy of the distribution of character categories
pub fn category_entropy(text: &str) -> f64 {
    use crate::char::categories::char_to_category;

    if text.is_empty() {
        return 0.0;
    }

    let mut category_counts = std::collections::HashMap::new();
    let total_chars = text.chars().count();

    // Count occurrences of each category
    for c in text.chars() {
        let category = char_to_category(c);
        *category_counts.entry(category).or_insert(0) += 1;
    }

    // Calculate entropy
    let mut entropy = 0.0;
    for (_, count) in category_counts {
        let probability = count as f64 / total_chars as f64;
        entropy -= probability * probability.log2();
    }

    entropy
}

/// Computes the ratio of uppercase characters to all letters in a string
pub fn ratio_uppercase(text: &str) -> f64 {
    if text.is_empty() {
        return 0.0;
    }

    let letter_count = count_letters(text);
    if letter_count == 0 {
        return 0.0;
    }

    let uppercase_count = count_uppercase(text);
    uppercase_count as f64 / letter_count as f64
}

/// Checks if a string is all ASCII
pub fn is_ascii(text: &str) -> bool {
    text.is_ascii()
}

/// Counts the number of non-ASCII characters in a string
pub fn count_non_ascii(text: &str) -> usize {
    text.chars().filter(|&c| !c.is_ascii()).count()
}

/// Computes the ratio of ASCII characters in a string
pub fn ratio_ascii(text: &str) -> f64 {
    if text.is_empty() {
        return 0.0; // Consistent with other ratio functions for empty input
    }

    let total_chars = text.chars().count();
    let ascii_count = text.chars().filter(|&c| c.is_ascii()).count();
    ascii_count as f64 / total_chars as f64
}

/// Counts the total number of characters in a string
pub fn count_chars(text: &str) -> usize {
    text.chars().count()
}

/// Counts the total number of words in a string using Unicode segmentation rules
pub fn count_words(text: &str) -> usize {
    use unicode_segmentation::UnicodeSegmentation;
    text.unicode_words().count()
}

/// Counts the frequency of each character in a string
pub fn char_frequency(text: &str) -> std::collections::HashMap<char, usize> {
    let mut counts = std::collections::HashMap::new();

    // Use a single pass through the text to count characters
    for c in text.chars() {
        *counts.entry(c).or_insert(0) += 1;
    }

    counts
}

/// Calculates the Shannon entropy of a string at the character level
/// Shannon entropy is a measure of information content or randomness
pub fn char_entropy(text: &str) -> f64 {
    if text.is_empty() {
        return 0.0;
    }

    let frequency = char_frequency(text);
    let total_chars = text.chars().count() as f64;

    // Calculate entropy using Shannon's formula: -sum(p_i * log2(p_i))
    let mut entropy = 0.0;
    for (_, count) in frequency {
        let probability = count as f64 / total_chars;
        entropy -= probability * probability.log2();
    }

    entropy
}

/// Counts the frequency of each character type (letter, digit, punctuation, etc.) in a string
pub fn char_type_frequency(text: &str) -> std::collections::HashMap<&'static str, usize> {
    let mut counts = std::collections::HashMap::new();

    // Initialize with zero counts for all types
    counts.insert("letter", 0);
    counts.insert("digit", 0);
    counts.insert("punctuation", 0);
    counts.insert("symbol", 0);
    counts.insert("whitespace", 0);
    counts.insert("other", 0);

    // Use a single pass through the text to count character types
    for c in text.chars() {
        if is_letter(c) {
            *counts.get_mut("letter").unwrap() += 1;
        } else if is_digit(c) {
            *counts.get_mut("digit").unwrap() += 1;
        } else if is_punctuation(c) {
            *counts.get_mut("punctuation").unwrap() += 1;
        } else if is_symbol(c) {
            *counts.get_mut("symbol").unwrap() += 1;
        } else if is_whitespace(c) {
            *counts.get_mut("whitespace").unwrap() += 1;
        } else {
            *counts.get_mut("other").unwrap() += 1;
        }
    }

    counts
}

/// Contains both count metrics and ratio metrics for character analysis
pub struct CharMetrics {
    // Count metrics
    pub total_chars: usize,
    pub letters: usize,
    pub digits: usize,
    pub punctuation: usize,
    pub symbols: usize,
    pub whitespace: usize,
    pub non_ascii: usize,
    pub uppercase: usize,
    pub lowercase: usize,
    pub alphanumeric: usize,

    // New count metrics
    pub char_type_transitions: usize,
    pub consecutive_runs: usize,
    pub punctuation_diversity: usize,

    // Ratio metrics
    pub ratio_letters: f64,
    pub ratio_digits: f64,
    pub ratio_punctuation: f64,
    pub ratio_symbols: f64,
    pub ratio_whitespace: f64,
    pub ratio_non_ascii: f64,
    pub ratio_uppercase: f64,
    pub ratio_lowercase: f64,
    pub ratio_alphanumeric: f64,
    pub ratio_alpha_to_numeric: f64,
    pub char_entropy: f64,

    // New ratio metrics
    pub case_ratio: f64,
    pub category_entropy: f64,
}

/// Calculates all character metrics in a single pass (optimized Rust implementation)
/// Returns both count metrics and ratio metrics in a single struct
pub fn calculate_char_metrics(text: &str) -> CharMetrics {
    // Initial counts
    let mut total_chars = 0;
    let mut letters = 0;
    let mut digits = 0;
    let mut punctuation = 0;
    let mut symbols = 0;
    let mut whitespace = 0;
    let mut non_ascii = 0;
    let mut uppercase = 0;
    let mut lowercase = 0;
    let mut alphanumeric = 0;

    // For entropy calculation
    let mut char_counts = std::collections::HashMap::new();

    // For punctuation diversity
    let mut unique_punctuation = std::collections::HashSet::new();

    // For category entropy
    use crate::char::categories::char_to_category;
    let mut category_counts = std::collections::HashMap::new();

    // Use a single pass through the text to count all metrics at once
    for c in text.chars() {
        total_chars += 1;

        // Update character frequency for entropy calculation
        *char_counts.entry(c).or_insert(0) += 1;

        // Update category for category entropy
        let category = char_to_category(c);
        *category_counts.entry(category).or_insert(0) += 1;

        if is_letter(c) {
            letters += 1;
            alphanumeric += 1;

            if is_uppercase(c) {
                uppercase += 1;
            } else if is_lowercase(c) {
                lowercase += 1;
            }
        } else if is_digit(c) {
            digits += 1;
            alphanumeric += 1;
        } else if is_punctuation(c) {
            punctuation += 1;
            unique_punctuation.insert(c);
        } else if is_symbol(c) {
            symbols += 1;
        } else if is_whitespace(c) {
            whitespace += 1;
        }

        if !c.is_ascii() {
            non_ascii += 1;
        }
    }

    // Calculate metrics that need a separate pass
    let char_type_transitions = count_char_type_transitions(text);
    let consecutive_runs = count_consecutive_runs(text);
    let punctuation_diversity = unique_punctuation.len();

    // Calculate ratios, handling empty text cases
    let ratio_letters = if total_chars > 0 {
        letters as f64 / total_chars as f64
    } else {
        0.0
    };
    let ratio_digits = if total_chars > 0 {
        digits as f64 / total_chars as f64
    } else {
        0.0
    };
    let ratio_punctuation = if total_chars > 0 {
        punctuation as f64 / total_chars as f64
    } else {
        0.0
    };
    let ratio_symbols = if total_chars > 0 {
        symbols as f64 / total_chars as f64
    } else {
        0.0
    };
    let ratio_whitespace = if total_chars > 0 {
        whitespace as f64 / total_chars as f64
    } else {
        0.0
    };
    let ratio_non_ascii = if total_chars > 0 {
        non_ascii as f64 / total_chars as f64
    } else {
        0.0
    };
    let ratio_uppercase = if letters > 0 {
        uppercase as f64 / letters as f64
    } else {
        0.0
    };
    let ratio_lowercase = if letters > 0 {
        lowercase as f64 / letters as f64
    } else {
        0.0
    };
    let ratio_alphanumeric = if total_chars > 0 {
        alphanumeric as f64 / total_chars as f64
    } else {
        0.0
    };
    let ratio_alpha_to_numeric = if digits > 0 {
        letters as f64 / digits as f64
    } else if letters > 0 {
        // Use large but finite number instead of infinity for consistency
        1e6 * letters as f64
    } else {
        0.0
    };

    // New ratio metrics
    let case_ratio = if lowercase > 0 {
        uppercase as f64 / lowercase as f64
    } else if uppercase > 0 {
        1e6 * uppercase as f64
    } else {
        0.0
    };

    // Calculate character entropy
    let mut char_entropy = 0.0;
    if total_chars > 0 {
        let total_chars_f64 = total_chars as f64;
        for (_, count) in char_counts {
            let probability = count as f64 / total_chars_f64;
            char_entropy -= probability * probability.log2();
        }
    }

    // Calculate category entropy
    let mut category_entropy = 0.0;
    if total_chars > 0 {
        let total_chars_f64 = total_chars as f64;
        for (_, count) in category_counts {
            let probability = count as f64 / total_chars_f64;
            category_entropy -= probability * probability.log2();
        }
    }

    CharMetrics {
        total_chars,
        letters,
        digits,
        punctuation,
        symbols,
        whitespace,
        non_ascii,
        uppercase,
        lowercase,
        alphanumeric,

        // New count metrics
        char_type_transitions,
        consecutive_runs,
        punctuation_diversity,

        ratio_letters,
        ratio_digits,
        ratio_punctuation,
        ratio_symbols,
        ratio_whitespace,
        ratio_non_ascii,
        ratio_uppercase,
        ratio_lowercase,
        ratio_alphanumeric,
        ratio_alpha_to_numeric,
        char_entropy,

        // New ratio metrics
        case_ratio,
        category_entropy,
    }
}

/// Performs combined character metrics in a single pass (optimized Rust implementation)
pub fn combined_char_metrics(text: &str) -> std::collections::HashMap<&'static str, usize> {
    let mut counts = std::collections::HashMap::new();

    // Initialize with zero counts for all metrics
    counts.insert("letters", 0);
    counts.insert("digits", 0);
    counts.insert("punctuation", 0);
    counts.insert("symbols", 0);
    counts.insert("whitespace", 0);
    counts.insert("non_ascii", 0);
    counts.insert("uppercase", 0);
    counts.insert("lowercase", 0);
    counts.insert("alphanumeric", 0);

    // Use a single pass through the text to count all metrics at once
    for c in text.chars() {
        if is_letter(c) {
            *counts.get_mut("letters").unwrap() += 1;
            *counts.get_mut("alphanumeric").unwrap() += 1;

            if is_uppercase(c) {
                *counts.get_mut("uppercase").unwrap() += 1;
            } else if is_lowercase(c) {
                *counts.get_mut("lowercase").unwrap() += 1;
            }
        } else if is_digit(c) {
            *counts.get_mut("digits").unwrap() += 1;
            *counts.get_mut("alphanumeric").unwrap() += 1;
        } else if is_punctuation(c) {
            *counts.get_mut("punctuation").unwrap() += 1;
        } else if is_symbol(c) {
            *counts.get_mut("symbols").unwrap() += 1;
        } else if is_whitespace(c) {
            *counts.get_mut("whitespace").unwrap() += 1;
        }

        if !c.is_ascii() {
            *counts.get_mut("non_ascii").unwrap() += 1;
        }
    }

    counts
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_is_letter() {
        assert!(is_letter('a'));
        assert!(is_letter('Z'));
        assert!(is_letter('é'));
        assert!(!is_letter('1'));
        assert!(!is_letter(' '));
        assert!(!is_letter('.'));
    }

    #[test]
    fn test_case_ratio() {
        assert_eq!(case_ratio(""), 0.0);
        assert_eq!(case_ratio("abc"), 0.0);
        assert_eq!(case_ratio("ABC"), 1e6 * 3.0); // Large number instead of infinity
        assert_eq!(case_ratio("AbCd"), 2.0 / 2.0);
        assert_eq!(case_ratio("ABCdef"), 3.0 / 3.0);
        assert_eq!(case_ratio("ABCdefghi"), 3.0 / 6.0);
    }

    #[test]
    fn test_count_char_type_transitions() {
        assert_eq!(count_char_type_transitions(""), 0);
        assert_eq!(count_char_type_transitions("a"), 0);
        assert_eq!(count_char_type_transitions("abc"), 0); // All same type (lowercase)
        assert_eq!(count_char_type_transitions("aBc"), 2); // lowercase -> uppercase -> lowercase
        assert_eq!(count_char_type_transitions("a1A"), 2); // lowercase -> digit -> uppercase
        assert_eq!(count_char_type_transitions("a1A,"), 3); // lowercase -> digit -> uppercase -> punctuation
        assert_eq!(count_char_type_transitions("a1A, "), 4); // lowercase -> digit -> uppercase -> punctuation -> whitespace
    }

    #[test]
    fn test_count_consecutive_runs() {
        assert_eq!(count_consecutive_runs(""), 0);
        assert_eq!(count_consecutive_runs("a"), 1);
        assert_eq!(count_consecutive_runs("abc"), 1); // One run of lowercase
        assert_eq!(count_consecutive_runs("aBc"), 3); // lowercase -> uppercase -> lowercase
        assert_eq!(count_consecutive_runs("AAAbbb123"), 3); // uppercase -> lowercase -> digits
        assert_eq!(count_consecutive_runs("A1a,"), 4); // uppercase -> digit -> lowercase -> punctuation
    }

    #[test]
    fn test_punctuation_diversity() {
        assert_eq!(punctuation_diversity(""), 0);
        assert_eq!(punctuation_diversity("abc"), 0);
        assert_eq!(punctuation_diversity("abc!"), 1);
        assert_eq!(punctuation_diversity("Hello, world!"), 2); // Comma and exclamation
        assert_eq!(punctuation_diversity("He,ll.o; w!or?ld:"), 6); // , . ; ! ? :
    }

    #[test]
    fn test_category_entropy() {
        // Single category should have entropy 0
        assert_eq!(category_entropy("aaaaa"), 0.0);

        // Different categories should have non-zero entropy
        assert!(category_entropy("aB1,") > 0.0);

        // Empty string
        assert_eq!(category_entropy(""), 0.0);

        // Test increase in entropy with more diverse categories
        let less_diverse = "aaabbb";
        let more_diverse = "aB1!@,";
        assert!(category_entropy(more_diverse) > category_entropy(less_diverse));
    }

    #[test]
    fn test_is_digit() {
        assert!(is_digit('0'));
        assert!(is_digit('9'));
        assert!(!is_digit('a'));
        assert!(!is_digit(' '));
    }

    #[test]
    fn test_is_punctuation() {
        assert!(is_punctuation('.'));
        assert!(is_punctuation(','));
        assert!(is_punctuation('!'));
        assert!(is_punctuation('?'));
        assert!(!is_punctuation('a'));
        assert!(!is_punctuation('1'));
        assert!(!is_punctuation(' '));
    }

    #[test]
    fn test_is_symbol() {
        assert!(is_symbol('+'));
        assert!(is_symbol('='));
        assert!(is_symbol('$'));
        assert!(!is_symbol('a'));
        assert!(!is_symbol('1'));
        assert!(!is_symbol(' '));
    }

    #[test]
    fn test_is_whitespace() {
        assert!(is_whitespace(' '));
        assert!(is_whitespace('\t'));
        assert!(is_whitespace('\n'));
        assert!(!is_whitespace('a'));
        assert!(!is_whitespace('1'));
    }

    #[test]
    fn test_is_uppercase() {
        assert!(is_uppercase('A'));
        assert!(is_uppercase('Z'));
        assert!(is_uppercase('É'));
        assert!(!is_uppercase('a'));
        assert!(!is_uppercase('1'));
        assert!(!is_uppercase(' '));
    }

    #[test]
    fn test_is_lowercase() {
        assert!(is_lowercase('a'));
        assert!(is_lowercase('z'));
        assert!(is_lowercase('é'));
        assert!(!is_lowercase('A'));
        assert!(!is_lowercase('1'));
        assert!(!is_lowercase(' '));
    }

    #[test]
    fn test_count_functions() {
        let text = "Hello, world! 123 $%^";

        assert_eq!(count_letters(text), 10);
        assert_eq!(count_digits(text), 3);
        assert_eq!(count_punctuation(text), 2); // Comma and exclamation
        assert_eq!(count_symbols(text), 3); // $, %, and ^ are symbols
        assert_eq!(count_whitespace(text), 3); // 3 whitespace characters
        assert_eq!(count_chars(text), 21); // Total character count
        assert_eq!(count_words(text), 3);
        assert_eq!(count_uppercase(text), 1); // "H" is uppercase
        assert_eq!(count_lowercase(text), 9); // "ello, world" are lowercase
    }

    #[test]
    fn test_ratio_uppercase() {
        assert_eq!(ratio_uppercase(""), 0.0);
        assert_eq!(ratio_uppercase("123"), 0.0);
        assert_eq!(ratio_uppercase("abc"), 0.0);
        assert_eq!(ratio_uppercase("ABC"), 1.0);
        assert_eq!(ratio_uppercase("AbC"), 2.0 / 3.0);
        assert_eq!(ratio_uppercase("Hello"), 0.2);
    }

    #[test]
    fn test_ascii_functions() {
        let ascii_text = "Hello, world!";
        let mixed_text = "Hello, 世界!";

        assert!(is_ascii(ascii_text));
        assert!(!is_ascii(mixed_text));
        assert_eq!(count_non_ascii(ascii_text), 0);
        assert_eq!(count_non_ascii(mixed_text), 2);
        assert_eq!(ratio_ascii(ascii_text), 1.0);
        assert!(ratio_ascii(mixed_text) < 1.0);
    }

    #[test]
    fn test_combined_char_metrics() {
        let text = "Hello, world! 123 $%^";
        let metrics = combined_char_metrics(text);

        assert_eq!(*metrics.get("letters").unwrap(), 10);
        assert_eq!(*metrics.get("digits").unwrap(), 3);
        assert_eq!(*metrics.get("punctuation").unwrap(), 2); // Comma and exclamation
        assert_eq!(*metrics.get("symbols").unwrap(), 3); // $, %, and ^ are symbols
        assert_eq!(*metrics.get("whitespace").unwrap(), 3); // 3 whitespace characters
        assert_eq!(*metrics.get("non_ascii").unwrap(), 0);
        assert_eq!(*metrics.get("uppercase").unwrap(), 1);
        assert_eq!(*metrics.get("lowercase").unwrap(), 9);
        assert_eq!(*metrics.get("alphanumeric").unwrap(), 13);
        // Note: We don't assert the total count here as combined_char_metrics doesn't return it
    }

    #[test]
    fn test_is_alphanumeric() {
        assert!(is_alphanumeric('a'));
        assert!(is_alphanumeric('Z'));
        assert!(is_alphanumeric('0'));
        assert!(is_alphanumeric('9'));
        assert!(!is_alphanumeric('!'));
        assert!(!is_alphanumeric(' '));
        assert!(!is_alphanumeric('.'));
    }

    #[test]
    fn test_count_alphanumeric() {
        assert_eq!(count_alphanumeric("abc123"), 6);
        assert_eq!(count_alphanumeric("abc 123"), 6);
        assert_eq!(count_alphanumeric("!@#"), 0);
        assert_eq!(count_alphanumeric(""), 0);
    }

    #[test]
    fn test_ratio_alphanumeric() {
        assert_eq!(ratio_alphanumeric("abc123"), 1.0);
        assert_eq!(ratio_alphanumeric("abc 123"), 6.0 / 7.0);
        assert_eq!(ratio_alphanumeric("!@#"), 0.0);
        assert_eq!(ratio_alphanumeric(""), 0.0);
    }

    #[test]
    fn test_ratio_alpha_to_numeric() {
        assert_eq!(ratio_alpha_to_numeric("abc123"), 3.0 / 3.0);
        assert_eq!(ratio_alpha_to_numeric("abcde12"), 5.0 / 2.0);
        assert_eq!(ratio_alpha_to_numeric("12345"), 0.0);
        // Should be using large number instead of infinity
        assert_eq!(ratio_alpha_to_numeric("abcde"), 1e6 * 5.0);
        assert_eq!(ratio_alpha_to_numeric(""), 0.0);
    }

    #[test]
    fn test_ratio_whitespace() {
        assert_eq!(ratio_whitespace("abc"), 0.0);
        assert_eq!(ratio_whitespace("a b c"), 2.0 / 5.0);
        assert_eq!(ratio_whitespace("   "), 1.0);
        assert_eq!(ratio_whitespace(""), 0.0);
    }

    #[test]
    fn test_ratio_digits() {
        assert_eq!(ratio_digits("abc"), 0.0);
        assert_eq!(ratio_digits("a1b2c3"), 3.0 / 6.0);
        assert_eq!(ratio_digits("123"), 1.0);
        assert_eq!(ratio_digits(""), 0.0);
    }

    #[test]
    fn test_ratio_punctuation() {
        assert_eq!(ratio_punctuation("abc"), 0.0);
        assert_eq!(ratio_punctuation("a,b.c!"), 3.0 / 6.0);
        assert_eq!(ratio_punctuation(",.;:"), 1.0);
        assert_eq!(ratio_punctuation(""), 0.0);
    }

    #[test]
    fn test_char_entropy() {
        // For a string with all the same character, entropy = 0
        assert_eq!(char_entropy("aaaaa"), 0.0);

        // For a string with perfect distribution (all characters equally likely),
        // entropy = log2(n) where n is the number of unique characters
        let text = "abcd";
        let expected = 2.0; // log2(4) = 2
        assert!((char_entropy(text) - expected).abs() < 1e-10);

        // Empty string
        assert_eq!(char_entropy(""), 0.0);

        // String with varied distribution
        let entropy = char_entropy("Hello, World!");
        assert!(entropy > 0.0);
    }

    #[test]
    fn test_calculate_char_metrics() {
        // Test with a mixed content string
        let text = "Hello, World! 123 $%^";
        let metrics = calculate_char_metrics(text);

        // Test count metrics
        assert_eq!(metrics.total_chars, 21); // Total character count
        assert_eq!(metrics.letters, 10);
        assert_eq!(metrics.digits, 3);
        assert_eq!(metrics.punctuation, 2); // Comma and exclamation
        assert_eq!(metrics.symbols, 3); // $, %, and ^ are symbols
        assert_eq!(metrics.whitespace, 3); // 3 whitespace characters
        assert_eq!(metrics.non_ascii, 0);
        assert_eq!(metrics.uppercase, 2); // 'H' and 'W'
        assert_eq!(metrics.lowercase, 8); // 'ello', 'orld'
        assert_eq!(metrics.alphanumeric, 13); // letters + digits

        // Test new count metrics
        assert_eq!(metrics.punctuation_diversity, 2); // Comma and exclamation mark
        assert!(metrics.char_type_transitions > 0);
        assert!(metrics.consecutive_runs > 0);

        // Test ratio metrics
        assert_eq!(metrics.ratio_letters, 10.0 / 21.0);
        assert_eq!(metrics.ratio_digits, 3.0 / 21.0);
        assert_eq!(metrics.ratio_punctuation, 2.0 / 21.0); // Updated for punctuation
        assert_eq!(metrics.ratio_symbols, 3.0 / 21.0); // Updated for symbols
        assert_eq!(metrics.ratio_whitespace, 3.0 / 21.0);
        assert_eq!(metrics.ratio_non_ascii, 0.0);
        assert_eq!(metrics.ratio_uppercase, 2.0 / 10.0); // This is unchanged as it's relative to letters
        assert_eq!(metrics.ratio_lowercase, 8.0 / 10.0); // This is unchanged as it's relative to letters
        assert_eq!(metrics.ratio_alphanumeric, 13.0 / 21.0);
        assert_eq!(metrics.ratio_alpha_to_numeric, 10.0 / 3.0);
        assert!(metrics.char_entropy > 0.0);

        // Test new ratio metrics
        assert_eq!(metrics.case_ratio, 2.0 / 8.0); // 2 uppercase to 8 lowercase
        assert!(metrics.category_entropy > 0.0);

        // Test with empty string
        let empty_metrics = calculate_char_metrics("");
        assert_eq!(empty_metrics.total_chars, 0);
        assert_eq!(empty_metrics.ratio_letters, 0.0);
        assert_eq!(empty_metrics.ratio_uppercase, 0.0);
        assert_eq!(empty_metrics.char_entropy, 0.0);
        assert_eq!(empty_metrics.case_ratio, 0.0);
        assert_eq!(empty_metrics.category_entropy, 0.0);
        assert_eq!(empty_metrics.char_type_transitions, 0);
        assert_eq!(empty_metrics.consecutive_runs, 0);
        assert_eq!(empty_metrics.punctuation_diversity, 0);

        // Test with all letters
        let letters_metrics = calculate_char_metrics("abcABC");
        assert_eq!(letters_metrics.ratio_letters, 1.0);
        assert_eq!(letters_metrics.ratio_uppercase, 0.5);
        assert_eq!(letters_metrics.ratio_lowercase, 0.5);
        assert_eq!(letters_metrics.ratio_alpha_to_numeric, 1e6 * 6.0); // Large number instead of infinity
        assert_eq!(letters_metrics.case_ratio, 3.0 / 3.0); // Equal uppercase and lowercase
        assert!(letters_metrics.category_entropy > 0.0);
        assert_eq!(letters_metrics.punctuation_diversity, 0);
    }
}
