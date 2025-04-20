//! # Text Segmentation
//!
//! This module provides functionality for segmenting text into structural units
//! such as words, lines, paragraphs, and sentences, and calculating related metrics.
//!
//! ## Key Features
//!
//! * Unicode-aware word segmentation
//! * Line and paragraph detection
//! * Sentence boundary recognition
//! * Structural metrics (average lengths, counts)
//!
//! Text segmentation is fundamental for analyzing document structure and readability,
//! providing insights into how text is organized and presented. These functions form
//! the foundation for higher-level readability metrics.

use unicode_segmentation::UnicodeSegmentation;

/// Splits text into words according to Unicode segmentation rules
pub fn split_words(text: &str) -> Vec<&str> {
    text.unicode_words().collect()
}

/// Counts the number of words using Unicode segmentation rules
pub fn count_words(text: &str) -> usize {
    text.unicode_words().count()
}

/// Splits text into lines by newline characters (CR, LF, CRLF)
pub fn split_lines(text: &str) -> Vec<&str> {
    text.lines().collect()
}

/// Counts the number of lines in text
pub fn count_lines(text: &str) -> usize {
    text.lines().count()
}

/// Calculates the average line length in characters
pub fn average_line_length(text: &str) -> f64 {
    let lines = split_lines(text);
    if lines.is_empty() {
        return 0.0;
    }

    let total_chars: usize = lines.iter().map(|line| line.chars().count()).sum();

    total_chars as f64 / lines.len() as f64
}

/// Splits text into paragraphs (sequences of text separated by blank lines)
pub fn split_paragraphs(text: &str) -> Vec<String> {
    let mut paragraphs = Vec::new();
    let mut current_paragraph = String::new();

    for line in text.lines() {
        let trimmed = line.trim();
        if trimmed.is_empty() {
            // End of paragraph
            if !current_paragraph.is_empty() {
                paragraphs.push(current_paragraph.trim().to_string());
                current_paragraph = String::new();
            }
        } else {
            // Add to current paragraph
            if !current_paragraph.is_empty() {
                current_paragraph.push(' ');
            }
            current_paragraph.push_str(trimmed);
        }
    }

    // Add the last paragraph if it's not empty
    if !current_paragraph.is_empty() {
        paragraphs.push(current_paragraph.trim().to_string());
    }

    paragraphs
}

/// Counts the number of paragraphs in text
pub fn count_paragraphs(text: &str) -> usize {
    split_paragraphs(text).len()
}

/// Calculates the average paragraph length in characters
pub fn average_paragraph_length(text: &str) -> f64 {
    let paragraphs = split_paragraphs(text);
    if paragraphs.is_empty() {
        return 0.0;
    }

    let total_chars: usize = paragraphs.iter().map(|p| p.chars().count()).sum();

    total_chars as f64 / paragraphs.len() as f64
}

/// Calculates the average word length in characters
pub fn average_word_length(text: &str) -> f64 {
    let words = split_words(text);
    if words.is_empty() {
        return 0.0;
    }

    let total_chars: usize = words.iter().map(|word| word.chars().count()).sum();

    total_chars as f64 / words.len() as f64
}

/// Segments text into sentences based on common sentence terminators
/// Returns a vector of strings representing individual sentences
pub fn segment_sentences(text: &str) -> Vec<String> {
    // Simple sentence terminators
    let sentence_terminators = ['.', '!', '?'];
    let mut sentences = Vec::new();
    let mut current_sentence = String::new();

    for c in text.chars() {
        current_sentence.push(c);

        // Check if the character is a sentence terminator and the sentence is not empty
        if sentence_terminators.contains(&c) && !current_sentence.trim().is_empty() {
            sentences.push(current_sentence.trim().to_string());
            current_sentence = String::new();
        }
    }

    // Add the last sentence if it's not empty
    if !current_sentence.trim().is_empty() {
        sentences.push(current_sentence.trim().to_string());
    }

    sentences
}

/// Segments text into lines identical to split_lines but returns owned Strings
/// Returns a vector of strings representing individual lines
pub fn segment_lines(text: &str) -> Vec<String> {
    text.lines().map(|line| line.to_string()).collect()
}

/// Segments text into paragraphs identical to split_paragraphs but with a different name
/// for API consistency. Returns a vector of strings representing individual paragraphs
pub fn segment_paragraphs(text: &str) -> Vec<String> {
    split_paragraphs(text)
}

/// Estimates the average sentence length in words
/// Note: This is a simple estimation based on common sentence terminators
pub fn average_sentence_length(text: &str) -> f64 {
    let sentences = segment_sentences(text);

    if sentences.is_empty() {
        return 0.0;
    }

    let total_words: usize = sentences.iter().map(|s| s.unicode_words().count()).sum();

    total_words as f64 / sentences.len() as f64
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_split_words() {
        let text = "The quick (\"brown\") fox can't jump 32.3 feet, right?";
        let words = split_words(text);
        assert_eq!(
            words,
            vec!["The", "quick", "brown", "fox", "can't", "jump", "32.3", "feet", "right"]
        );
    }

    #[test]
    fn test_count_words() {
        let text = "The quick brown fox";
        assert_eq!(count_words(text), 4);

        let empty = "";
        assert_eq!(count_words(empty), 0);

        let mixed = "The quick (\"brown\") fox can't jump 32.3 feet, right?";
        assert_eq!(count_words(mixed), 9);
    }

    #[test]
    fn test_split_lines() {
        let text = "Line 1\nLine 2\r\nLine 3";
        let lines = split_lines(text);
        assert_eq!(lines, vec!["Line 1", "Line 2", "Line 3"]);
    }

    #[test]
    fn test_count_lines() {
        let text = "Line 1\nLine 2\r\nLine 3";
        assert_eq!(count_lines(text), 3);

        let empty = "";
        assert_eq!(count_lines(empty), 0);

        let one_line = "Just one line";
        assert_eq!(count_lines(one_line), 1);
    }

    #[test]
    fn test_average_line_length() {
        let text = "123\n12345\n1";
        assert_eq!(average_line_length(text), 3.0);

        let empty = "";
        assert_eq!(average_line_length(empty), 0.0);
    }

    #[test]
    fn test_split_paragraphs() {
        let text = "Paragraph 1.\n\nParagraph 2.\n\r\nParagraph 3.";
        let paragraphs = split_paragraphs(text);
        assert_eq!(
            paragraphs,
            vec!["Paragraph 1.", "Paragraph 2.", "Paragraph 3."]
        );

        let text_with_indentation = "   Paragraph 1.   \n\n   Paragraph 2.   ";
        let paragraphs = split_paragraphs(text_with_indentation);
        assert_eq!(paragraphs, vec!["Paragraph 1.", "Paragraph 2."]);
    }

    #[test]
    fn test_count_paragraphs() {
        let text = "Paragraph 1.\n\nParagraph 2.\n\r\nParagraph 3.";
        assert_eq!(count_paragraphs(text), 3);

        let empty = "";
        assert_eq!(count_paragraphs(empty), 0);

        let one_paragraph = "Just one paragraph.";
        assert_eq!(count_paragraphs(one_paragraph), 1);
    }

    #[test]
    fn test_average_paragraph_length() {
        let text = "123.\n\n12345.\n\n1.";
        assert_eq!(average_paragraph_length(text), 4.0); // "123." (4), "12345." (6), "1." (2) -> avg = 4.0

        let empty = "";
        assert_eq!(average_paragraph_length(empty), 0.0);
    }

    #[test]
    fn test_average_word_length() {
        let text = "The quick brown fox";
        assert_eq!(average_word_length(text), 4.0); // (3 + 5 + 5 + 3) / 4 = 4.0

        let empty = "";
        assert_eq!(average_word_length(empty), 0.0);

        let mixed = "a bb ccc dddd";
        assert_eq!(average_word_length(mixed), 2.5); // (1 + 2 + 3 + 4) / 4 = 2.5

        // Test with Unicode characters (each counts as 1 char)
        let unicode = "αβ γδε";
        assert_eq!(average_word_length(unicode), 2.5); // (2 + 3) / 2 = 2.5
    }

    #[test]
    fn test_average_sentence_length() {
        let text = "This is sentence one. This is the second sentence! Is this the third?";
        let avg = average_sentence_length(text);
        assert!(avg > 3.0 && avg < 5.0);

        let empty = "";
        assert_eq!(average_sentence_length(empty), 0.0);
    }
}
