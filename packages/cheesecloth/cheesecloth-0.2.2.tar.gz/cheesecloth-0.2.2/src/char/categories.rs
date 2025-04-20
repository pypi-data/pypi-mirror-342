//! # Unicode Character Categories
//!
//! This module provides comprehensive Unicode character categorization functionality,
//! allowing for detailed analysis of text based on the standard Unicode character
//! categories and category groups.
//!
//! ## Key Features
//!
//! * Full Unicode character categorization (Ll, Lu, Nd, etc.)
//! * Unicode category grouping (L, N, P, S, Z, etc.)
//! * Efficient category counting and frequency analysis
//! * Parallelized processing for large texts
//! * Optimized caching for common ASCII characters
//!
//! The module implements the full Unicode General Category system with extensions
//! for efficient text analysis, providing insights into script composition and
//! character distribution patterns.

use icu_properties::{maps, GeneralCategory};
use lru::LruCache;
use rayon::prelude::*;
use std::cell::RefCell;
use std::collections::HashMap;
use std::num::NonZeroUsize;

/// Unicode character category enum
#[derive(Hash, Eq, PartialEq, Clone, Copy, Debug)]
pub enum UnicodeCategory {
    Ll, // Lowercase Letter
    Lu, // Uppercase Letter
    Lt, // Titlecase Letter
    Lm, // Modifier Letter
    Lo, // Other Letter
    Mn, // Non-spacing Mark
    Mc, // Spacing Mark
    Me, // Enclosing Mark
    Nd, // Decimal Number
    Nl, // Letter Number
    No, // Other Number
    Pc, // Connector Punctuation
    Pd, // Dash Punctuation
    Ps, // Open Punctuation
    Pe, // Close Punctuation
    Pi, // Initial Punctuation
    Pf, // Final Punctuation
    Po, // Other Punctuation
    Sm, // Math Symbol
    Sc, // Currency Symbol
    Sk, // Modifier Symbol
    So, // Other Symbol
    Zs, // Space Separator
    Zl, // Line Separator
    Zp, // Paragraph Separator
    Cc, // Control
    Cf, // Format
    Cs, // Surrogate
    Co, // Private Use
    Cn, // Unassigned
}

/// Unicode character category group enum
#[derive(Hash, Eq, PartialEq, Clone, Copy, Debug)]
pub enum UnicodeCategoryGroup {
    L, // Letter
    M, // Mark
    N, // Number
    P, // Punctuation
    S, // Symbol
    Z, // Separator
    C, // Other
}

// Initialize the thread-local LRU caches with capacity of 4096 entries
// This size provides an optimal balance between memory usage and cache hit rate
thread_local! {
    // Cache for char to UnicodeCategory lookups
    // Using a cache of 4096 entries to balance memory usage with hit rate
    static CATEGORY_CACHE: RefCell<LruCache<char, UnicodeCategory>> =
        RefCell::new(LruCache::new(NonZeroUsize::new(4096).unwrap()));

    // Cache for char to UnicodeCategoryGroup lookups
    // Using a cache of 4096 entries to balance memory usage with hit rate
    static CATEGORY_GROUP_CACHE: RefCell<LruCache<char, UnicodeCategoryGroup>> =
        RefCell::new(LruCache::new(NonZeroUsize::new(4096).unwrap()));
}

/// Convert a character to its Unicode category with efficient caching for common characters
pub fn char_to_category(ch: char) -> UnicodeCategory {
    // Fast path for ASCII range (most common in typical text)
    // This avoids the expensive ICU lookup for common characters
    if ch as u32 <= 127 {
        match ch {
            'a'..='z' => return UnicodeCategory::Ll,
            'A'..='Z' => return UnicodeCategory::Lu,
            '0'..='9' => return UnicodeCategory::Nd,
            ' ' | '\t' | '\n' | '\r' | '\x0C' => return UnicodeCategory::Zs,
            '.' | ',' | ';' | ':' | '!' | '?' => return UnicodeCategory::Po,
            '(' | '[' | '{' => return UnicodeCategory::Ps,
            ')' | ']' | '}' => return UnicodeCategory::Pe,
            '+' | '-' | '*' | '/' | '%' | '=' | '<' | '>' => return UnicodeCategory::Sm,
            '$' => return UnicodeCategory::Sc,
            '_' => return UnicodeCategory::Pc,
            '#' | '@' | '&' | '^' => return UnicodeCategory::Po,
            '\"' | '\'' => return UnicodeCategory::Po,
            // Fall through to cache/ICU lookup for other ASCII
            _ => {}
        }
    }

    // For non-ASCII characters, first check the thread-local cache
    // This avoids the expensive ICU lookup for repeated characters
    let mut category = None;

    // Try to get from cache first
    CATEGORY_CACHE.with(|cache| {
        let mut cache_ref = cache.borrow_mut();
        if let Some(&cached_category) = cache_ref.get(&ch) {
            category = Some(cached_category);
        }
    });

    // Return early if found in cache
    if let Some(cat) = category {
        return cat;
    }

    // For cache miss, use the ICU lookup
    let result = match maps::general_category().get(ch) {
        GeneralCategory::LowercaseLetter => UnicodeCategory::Ll,
        GeneralCategory::UppercaseLetter => UnicodeCategory::Lu,
        GeneralCategory::TitlecaseLetter => UnicodeCategory::Lt,
        GeneralCategory::ModifierLetter => UnicodeCategory::Lm,
        GeneralCategory::OtherLetter => UnicodeCategory::Lo,
        GeneralCategory::NonspacingMark => UnicodeCategory::Mn,
        GeneralCategory::SpacingMark => UnicodeCategory::Mc,
        GeneralCategory::EnclosingMark => UnicodeCategory::Me,
        GeneralCategory::DecimalNumber => UnicodeCategory::Nd,
        GeneralCategory::LetterNumber => UnicodeCategory::Nl,
        GeneralCategory::OtherNumber => UnicodeCategory::No,
        GeneralCategory::ConnectorPunctuation => UnicodeCategory::Pc,
        GeneralCategory::DashPunctuation => UnicodeCategory::Pd,
        GeneralCategory::OpenPunctuation => UnicodeCategory::Ps,
        GeneralCategory::ClosePunctuation => UnicodeCategory::Pe,
        GeneralCategory::InitialPunctuation => UnicodeCategory::Pi,
        GeneralCategory::FinalPunctuation => UnicodeCategory::Pf,
        GeneralCategory::OtherPunctuation => UnicodeCategory::Po,
        GeneralCategory::MathSymbol => UnicodeCategory::Sm,
        GeneralCategory::CurrencySymbol => UnicodeCategory::Sc,
        GeneralCategory::ModifierSymbol => UnicodeCategory::Sk,
        GeneralCategory::OtherSymbol => UnicodeCategory::So,
        GeneralCategory::SpaceSeparator => UnicodeCategory::Zs,
        GeneralCategory::LineSeparator => UnicodeCategory::Zl,
        GeneralCategory::ParagraphSeparator => UnicodeCategory::Zp,
        GeneralCategory::Control => UnicodeCategory::Cc,
        GeneralCategory::Format => UnicodeCategory::Cf,
        GeneralCategory::Surrogate => UnicodeCategory::Cs,
        GeneralCategory::PrivateUse => UnicodeCategory::Co,
        GeneralCategory::Unassigned => UnicodeCategory::Cn,
    };

    // Add to cache
    CATEGORY_CACHE.with(|cache| {
        let mut cache_ref = cache.borrow_mut();
        cache_ref.put(ch, result);
    });

    result
}

/// Convert a Unicode category to its group - optimized with a direct lookup table
pub fn category_to_group(category: UnicodeCategory) -> UnicodeCategoryGroup {
    // Using a lookup table for better performance than a match statement
    static GROUPS: [UnicodeCategoryGroup; 30] = [
        // Ll, Lu, Lt, Lm, Lo
        UnicodeCategoryGroup::L,
        UnicodeCategoryGroup::L,
        UnicodeCategoryGroup::L,
        UnicodeCategoryGroup::L,
        UnicodeCategoryGroup::L,
        // Mn, Mc, Me
        UnicodeCategoryGroup::M,
        UnicodeCategoryGroup::M,
        UnicodeCategoryGroup::M,
        // Nd, Nl, No
        UnicodeCategoryGroup::N,
        UnicodeCategoryGroup::N,
        UnicodeCategoryGroup::N,
        // Pc, Pd, Ps, Pe, Pi, Pf, Po
        UnicodeCategoryGroup::P,
        UnicodeCategoryGroup::P,
        UnicodeCategoryGroup::P,
        UnicodeCategoryGroup::P,
        UnicodeCategoryGroup::P,
        UnicodeCategoryGroup::P,
        UnicodeCategoryGroup::P,
        // Sm, Sc, Sk, So
        UnicodeCategoryGroup::S,
        UnicodeCategoryGroup::S,
        UnicodeCategoryGroup::S,
        UnicodeCategoryGroup::S,
        // Zs, Zl, Zp
        UnicodeCategoryGroup::Z,
        UnicodeCategoryGroup::Z,
        UnicodeCategoryGroup::Z,
        // Cc, Cf, Cs, Co, Cn
        UnicodeCategoryGroup::C,
        UnicodeCategoryGroup::C,
        UnicodeCategoryGroup::C,
        UnicodeCategoryGroup::C,
        UnicodeCategoryGroup::C,
    ];

    // Use the enum discriminant as an index into the lookup table
    GROUPS[category as usize]
}

/// Convert a character directly to its Unicode category group with optimized inline caching
pub fn char_to_category_group(ch: char) -> UnicodeCategoryGroup {
    // Fast path for ASCII with inline category mapping to avoid double lookups
    if ch as u32 <= 127 {
        match ch {
            'a'..='z' | 'A'..='Z' => return UnicodeCategoryGroup::L, // Letters
            '0'..='9' => return UnicodeCategoryGroup::N,             // Numbers
            ' ' | '\t' | '\n' | '\r' | '\x0C' => return UnicodeCategoryGroup::Z, // Whitespace
            '.' | ',' | ';' | ':' | '!' | '?' | '(' | '[' | '{' | ')' | ']' | '}' | '#' | '@'
            | '&' | '^' | '\"' | '\'' => return UnicodeCategoryGroup::P, // Punctuation
            '+' | '-' | '*' | '/' | '%' | '=' | '<' | '>' | '$' => return UnicodeCategoryGroup::S, // Symbols
            '_' => return UnicodeCategoryGroup::P, // Underscore is punctuation
            _ => {}                                // Fall through for other ASCII
        }
    }

    // For non-ASCII characters, first check the thread-local cache
    // This avoids the expensive category lookup and group mapping for repeated characters
    let mut group = None;

    // Try to get from cache first
    CATEGORY_GROUP_CACHE.with(|cache| {
        let mut cache_ref = cache.borrow_mut();
        if let Some(&cached_group) = cache_ref.get(&ch) {
            group = Some(cached_group);
        }
    });

    // Return early if found in cache
    if let Some(g) = group {
        return g;
    }

    // For cache miss, get category first then map to group
    let result = category_to_group(char_to_category(ch));

    // Add to cache
    CATEGORY_GROUP_CACHE.with(|cache| {
        let mut cache_ref = cache.borrow_mut();
        cache_ref.put(ch, result);
    });

    result
}

/// Get the string representation of a Unicode category
pub fn category_to_string(category: UnicodeCategory) -> &'static str {
    match category {
        UnicodeCategory::Ll => "Ll",
        UnicodeCategory::Lu => "Lu",
        UnicodeCategory::Lt => "Lt",
        UnicodeCategory::Lm => "Lm",
        UnicodeCategory::Lo => "Lo",
        UnicodeCategory::Mn => "Mn",
        UnicodeCategory::Mc => "Mc",
        UnicodeCategory::Me => "Me",
        UnicodeCategory::Nd => "Nd",
        UnicodeCategory::Nl => "Nl",
        UnicodeCategory::No => "No",
        UnicodeCategory::Pc => "Pc",
        UnicodeCategory::Pd => "Pd",
        UnicodeCategory::Ps => "Ps",
        UnicodeCategory::Pe => "Pe",
        UnicodeCategory::Pi => "Pi",
        UnicodeCategory::Pf => "Pf",
        UnicodeCategory::Po => "Po",
        UnicodeCategory::Sm => "Sm",
        UnicodeCategory::Sc => "Sc",
        UnicodeCategory::Sk => "Sk",
        UnicodeCategory::So => "So",
        UnicodeCategory::Zs => "Zs",
        UnicodeCategory::Zl => "Zl",
        UnicodeCategory::Zp => "Zp",
        UnicodeCategory::Cc => "Cc",
        UnicodeCategory::Cf => "Cf",
        UnicodeCategory::Cs => "Cs",
        UnicodeCategory::Co => "Co",
        UnicodeCategory::Cn => "Cn",
    }
}

/// Get the string representation of a Unicode category group
pub fn category_group_to_string(group: UnicodeCategoryGroup) -> &'static str {
    match group {
        UnicodeCategoryGroup::L => "L",
        UnicodeCategoryGroup::M => "M",
        UnicodeCategoryGroup::N => "N",
        UnicodeCategoryGroup::P => "P",
        UnicodeCategoryGroup::S => "S",
        UnicodeCategoryGroup::Z => "Z",
        UnicodeCategoryGroup::C => "C",
    }
}

/// Convert a string to a vector of Unicode categories
pub fn to_category_vector(text: &str) -> Vec<UnicodeCategory> {
    text.chars()
        .collect::<Vec<char>>()
        .par_iter()
        .map(|&c| char_to_category(c))
        .collect()
}

/// Convert a string to a vector of Unicode category groups
pub fn to_category_group_vector(text: &str) -> Vec<UnicodeCategoryGroup> {
    text.chars()
        .collect::<Vec<char>>()
        .par_iter()
        .map(|&c| char_to_category_group(c))
        .collect()
}

/// Count the occurrences of each Unicode category in a string - efficient implementation
pub fn count_categories(text: &str) -> HashMap<UnicodeCategory, usize> {
    let mut counts = HashMap::new();

    // Process text in parallel for larger texts, sequential for smaller ones
    if text.len() > 10000 {
        // For larger texts, use parallel processing
        let char_vec: Vec<char> = text.chars().collect();
        let category_counts = char_vec
            .par_iter()
            .map(|&c| char_to_category(c))
            .fold(
                HashMap::new,
                |mut acc, category| {
                    *acc.entry(category).or_insert(0) += 1;
                    acc
                },
            )
            .reduce(
                HashMap::new,
                |mut acc, partial| {
                    for (k, v) in partial {
                        *acc.entry(k).or_insert(0) += v;
                    }
                    acc
                },
            );

        counts = category_counts;
    } else {
        // For smaller texts, use direct sequential processing
        for c in text.chars() {
            *counts.entry(char_to_category(c)).or_insert(0) += 1;
        }
    }

    counts
}

/// Count the occurrences of each Unicode category group in a string - efficient implementation
pub fn count_category_groups(text: &str) -> HashMap<UnicodeCategoryGroup, usize> {
    let mut counts = HashMap::new();

    // Pre-initialize with all possible groups for more efficient insertions
    counts.insert(UnicodeCategoryGroup::L, 0);
    counts.insert(UnicodeCategoryGroup::M, 0);
    counts.insert(UnicodeCategoryGroup::N, 0);
    counts.insert(UnicodeCategoryGroup::P, 0);
    counts.insert(UnicodeCategoryGroup::S, 0);
    counts.insert(UnicodeCategoryGroup::Z, 0);
    counts.insert(UnicodeCategoryGroup::C, 0);

    // Process text in parallel for larger texts, sequential for smaller ones
    if text.len() > 10000 {
        // For larger texts, use parallel processing with Rayon
        let char_vec: Vec<char> = text.chars().collect();
        let group_counts = char_vec
            .par_iter()
            .fold(
                || {
                    let mut map = HashMap::new();
                    map.insert(UnicodeCategoryGroup::L, 0);
                    map.insert(UnicodeCategoryGroup::M, 0);
                    map.insert(UnicodeCategoryGroup::N, 0);
                    map.insert(UnicodeCategoryGroup::P, 0);
                    map.insert(UnicodeCategoryGroup::S, 0);
                    map.insert(UnicodeCategoryGroup::Z, 0);
                    map.insert(UnicodeCategoryGroup::C, 0);
                    map
                },
                |mut acc, &c| {
                    let group = char_to_category_group(c);
                    *acc.get_mut(&group).unwrap() += 1;
                    acc
                },
            )
            .reduce(
                || {
                    let mut map = HashMap::new();
                    map.insert(UnicodeCategoryGroup::L, 0);
                    map.insert(UnicodeCategoryGroup::M, 0);
                    map.insert(UnicodeCategoryGroup::N, 0);
                    map.insert(UnicodeCategoryGroup::P, 0);
                    map.insert(UnicodeCategoryGroup::S, 0);
                    map.insert(UnicodeCategoryGroup::Z, 0);
                    map.insert(UnicodeCategoryGroup::C, 0);
                    map
                },
                |mut acc, partial| {
                    for (k, v) in partial {
                        *acc.get_mut(&k).unwrap() += v;
                    }
                    acc
                },
            );

        counts = group_counts;
    } else {
        // For smaller texts, use direct sequential processing with pre-initialized counts
        for c in text.chars() {
            let group = char_to_category_group(c);
            *counts.get_mut(&group).unwrap() += 1;
        }
    }

    // Remove any groups with zero counts
    counts.retain(|_, &mut count| count > 0);

    counts
}

/// Get efficient string-based frequency counts of Unicode categories
pub fn category_string_frequency(text: &str) -> HashMap<String, usize> {
    // First get the category counts using the efficient implementation
    let category_counts = count_categories(text);

    // Then convert category keys to strings for Python compatibility
    category_counts
        .into_iter()
        .map(|(category, count)| (category_to_string(category).to_string(), count))
        .collect()
}

/// Get efficient string-based frequency counts of Unicode category groups
pub fn category_group_string_frequency(text: &str) -> HashMap<String, usize> {
    // First get the category group counts using the efficient implementation
    let group_counts = count_category_groups(text);

    // Then convert group keys to strings for Python compatibility
    group_counts
        .into_iter()
        .map(|(group, count)| (category_group_to_string(group).to_string(), count))
        .collect()
}

/// Count the ratio of each Unicode category in a string
pub fn category_ratios(text: &str) -> HashMap<UnicodeCategory, f64> {
    let counts = count_categories(text);
    let total = text.chars().count() as f64;

    if total == 0.0 {
        return HashMap::new();
    }

    counts
        .into_iter()
        .map(|(k, v)| (k, v as f64 / total))
        .collect()
}

/// Count the ratio of each Unicode category group in a string
pub fn category_group_ratios(text: &str) -> HashMap<UnicodeCategoryGroup, f64> {
    let counts = count_category_groups(text);
    let total = text.chars().count() as f64;

    if total == 0.0 {
        return HashMap::new();
    }

    counts
        .into_iter()
        .map(|(k, v)| (k, v as f64 / total))
        .collect()
}

/// Calculate bigrams of Unicode categories in a text
/// Each bigram is a tuple of (optional preceding category, optional following category)
/// For the first character, the preceding category is None
/// For the last character, the following category is None
pub fn calculate_category_bigrams(
    text: &str,
) -> Vec<(Option<UnicodeCategory>, Option<UnicodeCategory>)> {
    let chars: Vec<char> = text.chars().collect();

    if chars.is_empty() {
        return Vec::new();
    }

    // Special case for single character
    if chars.len() == 1 {
        let cat = char_to_category(chars[0]);
        return vec![(None, Some(cat)), (Some(cat), None)];
    }

    let categories: Vec<UnicodeCategory> = chars.iter().map(|&c| char_to_category(c)).collect();
    let mut bigrams = Vec::with_capacity(chars.len() + 1);

    // First character: (None, Char1)
    bigrams.push((None, Some(categories[0])));

    // All adjacent character pairs: (Char_i, Char_i+1)
    for window in categories.windows(2) {
        if window.len() == 2 {
            bigrams.push((Some(window[0]), Some(window[1])));
        }
    }

    // Last character: (CharN, None)
    bigrams.push((Some(categories[categories.len() - 1]), None));

    bigrams
}

/// Count the frequencies of Unicode category bigrams in a text
pub fn count_category_bigrams(text: &str) -> HashMap<(Option<String>, Option<String>), usize> {
    let bigrams = calculate_category_bigrams(text);
    let mut counts = HashMap::new();

    for (prev_cat, next_cat) in bigrams {
        // Convert categories to strings, using None where appropriate
        let prev_cat_str = prev_cat.map(|c| category_to_string(c).to_string());
        let next_cat_str = next_cat.map(|c| category_to_string(c).to_string());

        // Increment the count for this bigram
        *counts.entry((prev_cat_str, next_cat_str)).or_insert(0) += 1;
    }

    counts
}

/// Calculate the ratios of Unicode category bigrams in a text
pub fn category_bigram_ratios(text: &str) -> HashMap<(Option<String>, Option<String>), f64> {
    let counts = count_category_bigrams(text);

    // For bigrams, the total count should be the sum of all bigram counts
    let total: usize = counts.values().sum();

    if total == 0 {
        return HashMap::new();
    }

    counts
        .into_iter()
        .map(|(k, v)| (k, v as f64 / total as f64))
        .collect()
}

/// Calculate bigrams of Unicode category groups in a text
pub fn calculate_category_group_bigrams(
    text: &str,
) -> Vec<(Option<UnicodeCategoryGroup>, Option<UnicodeCategoryGroup>)> {
    let chars: Vec<char> = text.chars().collect();

    if chars.is_empty() {
        return Vec::new();
    }

    // Special case for single character
    if chars.len() == 1 {
        let group = char_to_category_group(chars[0]);
        return vec![(None, Some(group)), (Some(group), None)];
    }

    let groups: Vec<UnicodeCategoryGroup> =
        chars.iter().map(|&c| char_to_category_group(c)).collect();
    let mut bigrams = Vec::with_capacity(chars.len() + 1);

    // First character: (None, Group1)
    bigrams.push((None, Some(groups[0])));

    // All adjacent character pairs: (Group_i, Group_i+1)
    for window in groups.windows(2) {
        if window.len() == 2 {
            bigrams.push((Some(window[0]), Some(window[1])));
        }
    }

    // Last character: (GroupN, None)
    bigrams.push((Some(groups[groups.len() - 1]), None));

    bigrams
}

/// Count the frequencies of Unicode category group bigrams in a text
pub fn count_category_group_bigrams(
    text: &str,
) -> HashMap<(Option<String>, Option<String>), usize> {
    let bigrams = calculate_category_group_bigrams(text);
    let mut counts = HashMap::new();

    for (prev_group, next_group) in bigrams {
        // Convert category groups to strings, using None where appropriate
        let prev_group_str = prev_group.map(|g| category_group_to_string(g).to_string());
        let next_group_str = next_group.map(|g| category_group_to_string(g).to_string());

        // Increment the count for this bigram
        *counts.entry((prev_group_str, next_group_str)).or_insert(0) += 1;
    }

    counts
}

/// Calculate the ratios of Unicode category group bigrams in a text
pub fn category_group_bigram_ratios(text: &str) -> HashMap<(Option<String>, Option<String>), f64> {
    let counts = count_category_group_bigrams(text);

    // For bigrams, the total count should be the sum of all bigram counts
    let total: usize = counts.values().sum();

    if total == 0 {
        return HashMap::new();
    }

    counts
        .into_iter()
        .map(|(k, v)| (k, v as f64 / total as f64))
        .collect()
}

/// Calculate trigrams of Unicode categories in a text
/// Each trigram is a tuple of (prev category, current category, next category)
/// For the first character, prev is None; for the last character, next is None
pub fn calculate_category_trigrams(
    text: &str,
) -> Vec<(
    Option<UnicodeCategory>,
    UnicodeCategory,
    Option<UnicodeCategory>,
)> {
    let chars: Vec<char> = text.chars().collect();

    if chars.is_empty() {
        return Vec::new();
    }

    // Special case for single character
    if chars.len() == 1 {
        let cat = char_to_category(chars[0]);
        return vec![(None, cat, None)];
    }

    // Special case for two characters
    if chars.len() == 2 {
        let cat1 = char_to_category(chars[0]);
        let cat2 = char_to_category(chars[1]);
        return vec![(None, cat1, Some(cat2)), (Some(cat1), cat2, None)];
    }

    let categories: Vec<UnicodeCategory> = chars.iter().map(|&c| char_to_category(c)).collect();
    let mut trigrams = Vec::with_capacity(chars.len());

    // First character: (None, Char1, Char2)
    trigrams.push((None, categories[0], Some(categories[1])));

    // Middle characters: (Char_i-1, Char_i, Char_i+1)
    for i in 1..categories.len() - 1 {
        trigrams.push((
            Some(categories[i - 1]),
            categories[i],
            Some(categories[i + 1]),
        ));
    }

    // Last character: (CharN-1, CharN, None)
    let last_idx = categories.len() - 1;
    trigrams.push((Some(categories[last_idx - 1]), categories[last_idx], None));

    trigrams
}

/// Count the frequencies of Unicode category trigrams in a text
pub fn count_category_trigrams(
    text: &str,
) -> HashMap<(Option<String>, String, Option<String>), usize> {
    let trigrams = calculate_category_trigrams(text);
    let mut counts = HashMap::new();

    for (prev_cat, current_cat, next_cat) in trigrams {
        // Convert categories to strings, using None where appropriate
        let prev_cat_str = prev_cat.map(|c| category_to_string(c).to_string());
        let current_cat_str = category_to_string(current_cat).to_string();
        let next_cat_str = next_cat.map(|c| category_to_string(c).to_string());

        // Increment the count for this trigram
        *counts
            .entry((prev_cat_str, current_cat_str, next_cat_str))
            .or_insert(0) += 1;
    }

    counts
}

/// Calculate the ratios of Unicode category trigrams in a text
pub fn category_trigram_ratios(
    text: &str,
) -> HashMap<(Option<String>, String, Option<String>), f64> {
    let counts = count_category_trigrams(text);

    // For trigrams, the total count should be the sum of all trigram counts
    let total: usize = counts.values().sum();

    if total == 0 {
        return HashMap::new();
    }

    counts
        .into_iter()
        .map(|(k, v)| (k, v as f64 / total as f64))
        .collect()
}

/// Calculate trigrams of Unicode category groups in a text
pub fn calculate_category_group_trigrams(
    text: &str,
) -> Vec<(
    Option<UnicodeCategoryGroup>,
    UnicodeCategoryGroup,
    Option<UnicodeCategoryGroup>,
)> {
    let chars: Vec<char> = text.chars().collect();

    if chars.is_empty() {
        return Vec::new();
    }

    // Special case for single character
    if chars.len() == 1 {
        let group = char_to_category_group(chars[0]);
        return vec![(None, group, None)];
    }

    // Special case for two characters
    if chars.len() == 2 {
        let group1 = char_to_category_group(chars[0]);
        let group2 = char_to_category_group(chars[1]);
        return vec![(None, group1, Some(group2)), (Some(group1), group2, None)];
    }

    let groups: Vec<UnicodeCategoryGroup> =
        chars.iter().map(|&c| char_to_category_group(c)).collect();
    let mut trigrams = Vec::with_capacity(chars.len());

    // First character: (None, Group1, Group2)
    trigrams.push((None, groups[0], Some(groups[1])));

    // Middle characters: (Group_i-1, Group_i, Group_i+1)
    for i in 1..groups.len() - 1 {
        trigrams.push((Some(groups[i - 1]), groups[i], Some(groups[i + 1])));
    }

    // Last character: (GroupN-1, GroupN, None)
    let last_idx = groups.len() - 1;
    trigrams.push((Some(groups[last_idx - 1]), groups[last_idx], None));

    trigrams
}

/// Count the frequencies of Unicode category group trigrams in a text
pub fn count_category_group_trigrams(
    text: &str,
) -> HashMap<(Option<String>, String, Option<String>), usize> {
    let trigrams = calculate_category_group_trigrams(text);
    let mut counts = HashMap::new();

    for (prev_group, current_group, next_group) in trigrams {
        // Convert category groups to strings, using None where appropriate
        let prev_group_str = prev_group.map(|g| category_group_to_string(g).to_string());
        let current_group_str = category_group_to_string(current_group).to_string();
        let next_group_str = next_group.map(|g| category_group_to_string(g).to_string());

        // Increment the count for this trigram
        *counts
            .entry((prev_group_str, current_group_str, next_group_str))
            .or_insert(0) += 1;
    }

    counts
}

/// Calculate the ratios of Unicode category group trigrams in a text
pub fn category_group_trigram_ratios(
    text: &str,
) -> HashMap<(Option<String>, String, Option<String>), f64> {
    let counts = count_category_group_trigrams(text);

    // For trigrams, the total count should be the sum of all trigram counts
    let total: usize = counts.values().sum();

    if total == 0 {
        return HashMap::new();
    }

    counts
        .into_iter()
        .map(|(k, v)| (k, v as f64 / total as f64))
        .collect()
}

mod tests {
    // Importing everything since most of the module's functions are tested
    #[allow(unused_imports)]
    use super::*;

    #[test]
    fn test_char_to_category() {
        assert_eq!(char_to_category('a'), UnicodeCategory::Ll);
        assert_eq!(char_to_category('A'), UnicodeCategory::Lu);
        assert_eq!(char_to_category('1'), UnicodeCategory::Nd);
        assert_eq!(char_to_category('!'), UnicodeCategory::Po);
        assert_eq!(char_to_category(' '), UnicodeCategory::Zs);
    }

    #[test]
    fn test_category_to_group() {
        assert_eq!(
            category_to_group(UnicodeCategory::Ll),
            UnicodeCategoryGroup::L
        );
        assert_eq!(
            category_to_group(UnicodeCategory::Mn),
            UnicodeCategoryGroup::M
        );
        assert_eq!(
            category_to_group(UnicodeCategory::Nd),
            UnicodeCategoryGroup::N
        );
        assert_eq!(
            category_to_group(UnicodeCategory::Po),
            UnicodeCategoryGroup::P
        );
        assert_eq!(
            category_to_group(UnicodeCategory::Sm),
            UnicodeCategoryGroup::S
        );
        assert_eq!(
            category_to_group(UnicodeCategory::Zs),
            UnicodeCategoryGroup::Z
        );
        assert_eq!(
            category_to_group(UnicodeCategory::Cc),
            UnicodeCategoryGroup::C
        );
    }

    #[test]
    fn test_char_to_category_group() {
        assert_eq!(char_to_category_group('a'), UnicodeCategoryGroup::L);
        assert_eq!(char_to_category_group('A'), UnicodeCategoryGroup::L);
        assert_eq!(char_to_category_group('1'), UnicodeCategoryGroup::N);
        assert_eq!(char_to_category_group('!'), UnicodeCategoryGroup::P);
        assert_eq!(char_to_category_group(' '), UnicodeCategoryGroup::Z);
    }

    #[test]
    fn test_to_category_vector() {
        let text = "Hello, world!";
        let categories = to_category_vector(text);
        assert_eq!(categories.len(), text.len());
        assert_eq!(categories[0], UnicodeCategory::Lu);
        assert_eq!(categories[1], UnicodeCategory::Ll);
        assert_eq!(categories[5], UnicodeCategory::Po);
        assert_eq!(categories[12], UnicodeCategory::Po);
    }

    #[test]
    fn test_to_category_group_vector() {
        let text = "Hello, world!";
        let categories = to_category_group_vector(text);
        assert_eq!(categories.len(), text.len());
        assert_eq!(categories[0], UnicodeCategoryGroup::L);
        assert_eq!(categories[1], UnicodeCategoryGroup::L);
        assert_eq!(categories[5], UnicodeCategoryGroup::P);
        assert_eq!(categories[12], UnicodeCategoryGroup::P);
    }

    #[test]
    fn test_count_categories() {
        let text = "Hello, world!";
        let counts = count_categories(text);
        assert_eq!(counts[&UnicodeCategory::Lu], 1);
        assert_eq!(counts[&UnicodeCategory::Ll], 9);
        assert_eq!(counts[&UnicodeCategory::Po], 2);
        assert_eq!(counts[&UnicodeCategory::Zs], 1);
    }

    #[test]
    fn test_count_category_groups() {
        let text = "Hello, world!";
        let counts = count_category_groups(text);
        assert_eq!(counts[&UnicodeCategoryGroup::L], 10);
        assert_eq!(counts[&UnicodeCategoryGroup::P], 2);
        assert_eq!(counts[&UnicodeCategoryGroup::Z], 1);
    }

    #[test]
    fn test_category_ratios() {
        let text = "Hello, world!";
        let ratios = category_ratios(text);

        assert!((ratios[&UnicodeCategory::Lu] - 1.0 / 13.0).abs() < 1e-10);
        assert!((ratios[&UnicodeCategory::Ll] - 9.0 / 13.0).abs() < 1e-10);
        assert!((ratios[&UnicodeCategory::Po] - 2.0 / 13.0).abs() < 1e-10);
        assert!((ratios[&UnicodeCategory::Zs] - 1.0 / 13.0).abs() < 1e-10);
    }

    #[test]
    fn test_category_group_ratios() {
        let text = "Hello, world!";
        let ratios = category_group_ratios(text);

        assert!((ratios[&UnicodeCategoryGroup::L] - 10.0 / 13.0).abs() < 1e-10);
        assert!((ratios[&UnicodeCategoryGroup::P] - 2.0 / 13.0).abs() < 1e-10);
        assert!((ratios[&UnicodeCategoryGroup::Z] - 1.0 / 13.0).abs() < 1e-10);
    }

    #[test]
    fn test_calculate_category_bigrams() {
        let text = "Hi";
        let bigrams = calculate_category_bigrams(text);

        assert_eq!(bigrams.len(), 3);
        assert_eq!(bigrams[0], (None, Some(UnicodeCategory::Lu))); // H: (None, H)
        assert_eq!(
            bigrams[1],
            (Some(UnicodeCategory::Lu), Some(UnicodeCategory::Ll))
        ); // H→i
        assert_eq!(bigrams[2], (Some(UnicodeCategory::Ll), None)); // i: (i, None)

        let text = "A1";
        let bigrams = calculate_category_bigrams(text);

        assert_eq!(bigrams.len(), 3);
        assert_eq!(bigrams[0], (None, Some(UnicodeCategory::Lu))); // A: (None, A)
        assert_eq!(
            bigrams[1],
            (Some(UnicodeCategory::Lu), Some(UnicodeCategory::Nd))
        ); // A→1
        assert_eq!(bigrams[2], (Some(UnicodeCategory::Nd), None)); // 1: (1, None)
    }

    #[test]
    fn test_count_category_bigrams() {
        let text = "Hi";
        let counts = count_category_bigrams(text);

        assert_eq!(counts.len(), 3);
        assert_eq!(counts[&(None, Some("Lu".to_string()))], 1); // Start→H
        assert_eq!(counts[&(Some("Lu".to_string()), Some("Ll".to_string()))], 1); // H→i
        assert_eq!(counts[&(Some("Ll".to_string()), None)], 1); // i→End

        let text = "HiHi"; // Test counts with duplicated bigrams
        let counts = count_category_bigrams(text);

        assert_eq!(counts.len(), 4);
        assert_eq!(counts[&(None, Some("Lu".to_string()))], 1); // Start→H
        assert_eq!(counts[&(Some("Lu".to_string()), Some("Ll".to_string()))], 2); // H→i (twice)
        assert_eq!(counts[&(Some("Ll".to_string()), Some("Lu".to_string()))], 1); // i→H
        assert_eq!(counts[&(Some("Ll".to_string()), None)], 1); // i→End
    }

    #[test]
    fn test_category_bigram_ratios() {
        let text = "Hi";
        let ratios = category_bigram_ratios(text);

        assert_eq!(ratios.len(), 3);
        assert!((ratios[&(None, Some("Lu".to_string()))] - 1.0 / 3.0).abs() < 1e-10); // Start→H
        assert!(
            (ratios[&(Some("Lu".to_string()), Some("Ll".to_string()))] - 1.0 / 3.0).abs() < 1e-10
        ); // H→i
        assert!((ratios[&(Some("Ll".to_string()), None)] - 1.0 / 3.0).abs() < 1e-10);
        // i→End
    }

    #[test]
    fn test_calculate_category_group_bigrams() {
        let text = "Hi";
        let bigrams = calculate_category_group_bigrams(text);

        assert_eq!(bigrams.len(), 3);
        assert_eq!(bigrams[0], (None, Some(UnicodeCategoryGroup::L))); // Start→H
        assert_eq!(
            bigrams[1],
            (Some(UnicodeCategoryGroup::L), Some(UnicodeCategoryGroup::L))
        ); // H→i
        assert_eq!(bigrams[2], (Some(UnicodeCategoryGroup::L), None)); // i→End

        let text = "A1";
        let bigrams = calculate_category_group_bigrams(text);

        assert_eq!(bigrams.len(), 3);
        assert_eq!(bigrams[0], (None, Some(UnicodeCategoryGroup::L))); // Start→A
        assert_eq!(
            bigrams[1],
            (Some(UnicodeCategoryGroup::L), Some(UnicodeCategoryGroup::N))
        ); // A→1
        assert_eq!(bigrams[2], (Some(UnicodeCategoryGroup::N), None)); // 1→End
    }

    #[test]
    fn test_count_category_group_bigrams() {
        let text = "Hi";
        let counts = count_category_group_bigrams(text);

        assert_eq!(counts.len(), 3);
        assert_eq!(counts[&(None, Some("L".to_string()))], 1); // Start→L
        assert_eq!(counts[&(Some("L".to_string()), Some("L".to_string()))], 1); // L→L
        assert_eq!(counts[&(Some("L".to_string()), None)], 1); // L→End

        let text = "A1";
        let counts = count_category_group_bigrams(text);

        assert_eq!(counts.len(), 3);
        assert_eq!(counts[&(None, Some("L".to_string()))], 1); // Start→L
        assert_eq!(counts[&(Some("L".to_string()), Some("N".to_string()))], 1); // L→N
        assert_eq!(counts[&(Some("N".to_string()), None)], 1); // N→End
    }

    #[test]
    fn test_category_group_bigram_ratios() {
        let text = "Hi";
        let ratios = category_group_bigram_ratios(text);

        assert_eq!(ratios.len(), 3);
        assert!((ratios[&(None, Some("L".to_string()))] - 1.0 / 3.0).abs() < 1e-10); // Start→L
        assert!(
            (ratios[&(Some("L".to_string()), Some("L".to_string()))] - 1.0 / 3.0).abs() < 1e-10
        ); // L→L
        assert!((ratios[&(Some("L".to_string()), None)] - 1.0 / 3.0).abs() < 1e-10); // L→End

        let text = "A1";
        let ratios = category_group_bigram_ratios(text);

        assert_eq!(ratios.len(), 3);
        assert!((ratios[&(None, Some("L".to_string()))] - 1.0 / 3.0).abs() < 1e-10); // Start→L
        assert!(
            (ratios[&(Some("L".to_string()), Some("N".to_string()))] - 1.0 / 3.0).abs() < 1e-10
        ); // L→N
        assert!((ratios[&(Some("N".to_string()), None)] - 1.0 / 3.0).abs() < 1e-10);
        // N→End
    }

    #[test]
    fn test_calculate_category_trigrams() {
        let text = "Hi!";
        let trigrams = calculate_category_trigrams(text);

        assert_eq!(trigrams.len(), 3);
        assert_eq!(
            trigrams[0],
            (None, UnicodeCategory::Lu, Some(UnicodeCategory::Ll))
        ); // Start→H→i
        assert_eq!(
            trigrams[1],
            (
                Some(UnicodeCategory::Lu),
                UnicodeCategory::Ll,
                Some(UnicodeCategory::Po)
            )
        ); // H→i→!
        assert_eq!(
            trigrams[2],
            (Some(UnicodeCategory::Ll), UnicodeCategory::Po, None)
        ); // i→!→End
    }

    #[test]
    fn test_count_category_trigrams() {
        let text = "Hi!";
        let counts = count_category_trigrams(text);

        assert_eq!(counts.len(), 3);
        assert_eq!(counts[&(None, "Lu".to_string(), Some("Ll".to_string()))], 1); // Start→H→i
        assert_eq!(
            counts[&(
                Some("Lu".to_string()),
                "Ll".to_string(),
                Some("Po".to_string())
            )],
            1
        ); // H→i→!
        assert_eq!(counts[&(Some("Ll".to_string()), "Po".to_string(), None)], 1);
        // i→!→End
    }

    #[test]
    fn test_category_trigram_ratios() {
        let text = "Hi!";
        let ratios = category_trigram_ratios(text);

        assert_eq!(ratios.len(), 3);
        assert!(
            (ratios[&(None, "Lu".to_string(), Some("Ll".to_string()))] - 1.0 / 3.0).abs() < 1e-10
        ); // Start→H→i
        assert!(
            (ratios[&(
                Some("Lu".to_string()),
                "Ll".to_string(),
                Some("Po".to_string())
            )] - 1.0 / 3.0)
                .abs()
                < 1e-10
        ); // H→i→!
        assert!(
            (ratios[&(Some("Ll".to_string()), "Po".to_string(), None)] - 1.0 / 3.0).abs() < 1e-10
        ); // i→!→End
    }

    #[test]
    fn test_calculate_category_group_trigrams() {
        let text = "Hi!";
        let trigrams = calculate_category_group_trigrams(text);

        assert_eq!(trigrams.len(), 3);
        assert_eq!(
            trigrams[0],
            (None, UnicodeCategoryGroup::L, Some(UnicodeCategoryGroup::L))
        ); // Start→H→i
        assert_eq!(
            trigrams[1],
            (
                Some(UnicodeCategoryGroup::L),
                UnicodeCategoryGroup::L,
                Some(UnicodeCategoryGroup::P)
            )
        ); // H→i→!
        assert_eq!(
            trigrams[2],
            (Some(UnicodeCategoryGroup::L), UnicodeCategoryGroup::P, None)
        ); // i→!→End
    }

    #[test]
    fn test_count_category_group_trigrams() {
        let text = "Hi!";
        let counts = count_category_group_trigrams(text);

        assert_eq!(counts.len(), 3);
        assert_eq!(counts[&(None, "L".to_string(), Some("L".to_string()))], 1); // Start→H→i
        assert_eq!(
            counts[&(
                Some("L".to_string()),
                "L".to_string(),
                Some("P".to_string())
            )],
            1
        ); // H→i→!
        assert_eq!(counts[&(Some("L".to_string()), "P".to_string(), None)], 1); // i→!→End
    }

    #[test]
    fn test_category_group_trigram_ratios() {
        let text = "Hi!";
        let ratios = category_group_trigram_ratios(text);

        assert_eq!(ratios.len(), 3);
        assert!(
            (ratios[&(None, "L".to_string(), Some("L".to_string()))] - 1.0 / 3.0).abs() < 1e-10
        ); // Start→H→i
        assert!(
            (ratios[&(
                Some("L".to_string()),
                "L".to_string(),
                Some("P".to_string())
            )] - 1.0 / 3.0)
                .abs()
                < 1e-10
        ); // H→i→!
        assert!(
            (ratios[&(Some("L".to_string()), "P".to_string(), None)] - 1.0 / 3.0).abs() < 1e-10
        ); // i→!→End
    }

    #[test]
    fn test_trigram_empty_string() {
        let text = "";
        assert_eq!(calculate_category_trigrams(text).len(), 0);
        assert_eq!(calculate_category_group_trigrams(text).len(), 0);
        assert_eq!(count_category_trigrams(text).len(), 0);
        assert_eq!(count_category_group_trigrams(text).len(), 0);
        assert_eq!(category_trigram_ratios(text).len(), 0);
        assert_eq!(category_group_trigram_ratios(text).len(), 0);
    }

    #[test]
    fn test_trigram_single_character() {
        let text = "A";
        let cat_trigrams = calculate_category_trigrams(text);
        assert_eq!(cat_trigrams.len(), 1);
        assert_eq!(cat_trigrams[0], (None, UnicodeCategory::Lu, None));

        let group_trigrams = calculate_category_group_trigrams(text);
        assert_eq!(group_trigrams.len(), 1);
        assert_eq!(group_trigrams[0], (None, UnicodeCategoryGroup::L, None));
    }

    #[test]
    fn test_trigram_two_characters() {
        let text = "A1";
        let cat_trigrams = calculate_category_trigrams(text);
        assert_eq!(cat_trigrams.len(), 2);
        assert_eq!(
            cat_trigrams[0],
            (None, UnicodeCategory::Lu, Some(UnicodeCategory::Nd))
        );
        assert_eq!(
            cat_trigrams[1],
            (Some(UnicodeCategory::Lu), UnicodeCategory::Nd, None)
        );

        let group_trigrams = calculate_category_group_trigrams(text);
        assert_eq!(group_trigrams.len(), 2);
        assert_eq!(
            group_trigrams[0],
            (None, UnicodeCategoryGroup::L, Some(UnicodeCategoryGroup::N))
        );
        assert_eq!(
            group_trigrams[1],
            (Some(UnicodeCategoryGroup::L), UnicodeCategoryGroup::N, None)
        );
    }

    #[test]
    fn test_trigram_ratio_sums() {
        let text = "Hello!";
        let cat_ratios = category_trigram_ratios(text);
        let total = cat_ratios.values().sum::<f64>();
        assert!((total - 1.0).abs() < 1e-10);

        let group_ratios = category_group_trigram_ratios(text);
        let total = group_ratios.values().sum::<f64>();
        assert!((total - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_cache_hit() {
        // Test the cache by calling the function twice with the same character
        let non_ascii_char = 'ñ';

        // First call should cache the result
        let first_result = char_to_category(non_ascii_char);

        // Second call should hit the cache
        let second_result = char_to_category(non_ascii_char);

        // Results should be the same
        assert_eq!(first_result, second_result);

        // Same for category group
        let first_group = char_to_category_group(non_ascii_char);
        let second_group = char_to_category_group(non_ascii_char);
        assert_eq!(first_group, second_group);
    }
}
