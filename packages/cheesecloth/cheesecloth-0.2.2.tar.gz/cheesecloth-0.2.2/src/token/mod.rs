//! # Machine Learning Tokenization
//!
//! This module provides functionality for machine learning-based tokenization
//! (e.g., BPE, WordPiece) and analysis of the resulting subword tokens.
//!
//! ## Key Features
//!
//! * Integration with Hugging Face tokenizers
//! * Efficient tokenizer caching
//! * Token-based metrics (counts, diversity, entropy)
//! * Support for pretrained tokenizers from major language models
//!
//! Unlike unigram tokenization that follows linguistic word boundaries,
//! ML tokenization breaks text into subword units optimized for machine learning models.
//! This module enables analysis of how text is processed by language models,
//! providing insights into tokenization efficiency and model behavior.

use lazy_static::lazy_static;
use std::collections::{HashMap, HashSet};
use std::sync::Mutex;
use tokenizers::tokenizer::{Result, Tokenizer};

// Cache for storing tokenizers
lazy_static! {
    static ref TOKENIZER_CACHE: Mutex<HashMap<String, Tokenizer>> = Mutex::new(HashMap::new());
}

/// Gets a tokenizer from the cache, or loads it from Hugging Face if not present
fn get_tokenizer(name: &str) -> Result<Tokenizer> {
    let mut cache = TOKENIZER_CACHE.lock().unwrap();

    // Check if we have it cached
    if let Some(tokenizer) = cache.get(name) {
        return Ok(tokenizer.clone());
    }

    // Load from HuggingFace
    let tokenizer = Tokenizer::from_pretrained(name, None)?;

    // Cache it
    cache.insert(name.to_string(), tokenizer.clone());

    Ok(tokenizer)
}

/// Encodes a string into token IDs using the specified tokenizer
pub fn encode_str(tokenizer_name: &str, text: &str) -> Result<Vec<u32>> {
    let tokenizer = get_tokenizer(tokenizer_name)?;
    let encoding = tokenizer.encode(text, false)?;

    Ok(encoding.get_ids().to_vec())
}

/// Decodes token IDs back into a string using the specified tokenizer
pub fn decode_str(tokenizer_name: &str, ids: &[u32]) -> Result<String> {
    let tokenizer = get_tokenizer(tokenizer_name)?;

    tokenizer.decode(ids, false)
}

/// Encodes multiple strings into token IDs (batch processing)
pub fn encode_str_list(tokenizer_name: &str, texts: &[&str]) -> Result<Vec<Vec<u32>>> {
    let tokenizer = get_tokenizer(tokenizer_name)?;

    let encodings = tokenizer.encode_batch(texts.to_vec(), false)?;
    let ids_list = encodings
        .iter()
        .map(|encoding| encoding.get_ids().to_vec())
        .collect();

    Ok(ids_list)
}

/// Decodes multiple lists of token IDs back into strings
pub fn decode_str_list(tokenizer_name: &str, ids_list: &[Vec<u32>]) -> Result<Vec<String>> {
    let tokenizer = get_tokenizer(tokenizer_name)?;

    let mut results = Vec::with_capacity(ids_list.len());

    for ids in ids_list {
        results.push(tokenizer.decode(ids, false)?);
    }

    Ok(results)
}

/// Tokenizes text into token IDs using a specified tokenizer (defaults to "gpt2")
pub fn tokenize(text: &str, tokenizer_name: Option<&str>) -> Result<Vec<u32>> {
    encode_str(tokenizer_name.unwrap_or("gpt2"), text)
}

/// Batch tokenizes multiple texts into token IDs (defaults to "gpt2")
pub fn batch_tokenize(texts: &[&str], tokenizer_name: Option<&str>) -> Result<Vec<Vec<u32>>> {
    encode_str_list(tokenizer_name.unwrap_or("gpt2"), texts)
}

// --- Metrics functions ---

/// Returns the total count of tokens for a text using the specified tokenizer
pub fn subword_token_count(text: &str, tokenizer_name: Option<&str>) -> Result<usize> {
    let tokens = tokenize(text, tokenizer_name)?;
    Ok(tokens.len())
}

/// Returns the count of unique tokens for a text using the specified tokenizer
pub fn unique_subword_count(text: &str, tokenizer_name: Option<&str>) -> Result<usize> {
    let tokens = tokenize(text, tokenizer_name)?;
    let unique_tokens: HashSet<u32> = tokens.into_iter().collect();
    Ok(unique_tokens.len())
}

/// Returns the type-token ratio (unique tokens / total tokens) for a text
pub fn subword_type_token_ratio(text: &str, tokenizer_name: Option<&str>) -> Result<f64> {
    let tokens = tokenize(text, tokenizer_name)?;

    if tokens.is_empty() {
        return Ok(0.0);
    }

    let unique_tokens: HashSet<u32> = tokens.iter().cloned().collect();

    Ok(unique_tokens.len() as f64 / tokens.len() as f64)
}

/// Returns the repetition rate (1 - unique/total) for a text
///
/// For empty text, returns 0.0 to indicate "no repetition" since there are no tokens to repeat.
pub fn subword_repetition_rate(text: &str, tokenizer_name: Option<&str>) -> Result<f64> {
    // If text is empty, special case to match behavior across metrics
    if text.is_empty() {
        return Ok(0.0);
    }

    let ratio = subword_type_token_ratio(text, tokenizer_name)?;
    Ok(1.0 - ratio)
}

/// Calculates the Shannon entropy of tokens in a text
pub fn subword_entropy(text: &str, tokenizer_name: Option<&str>) -> Result<f64> {
    let tokens = tokenize(text, tokenizer_name)?;

    if tokens.is_empty() {
        return Ok(0.0);
    }

    // Count frequency of each token
    let mut frequency: HashMap<u32, usize> = HashMap::new();
    for token in &tokens {
        *frequency.entry(*token).or_insert(0) += 1;
    }

    let total = tokens.len() as f64;

    // Calculate entropy using Shannon's formula: -sum(p_i * log2(p_i))
    let mut entropy = 0.0;
    for &count in frequency.values() {
        let probability = count as f64 / total;
        entropy -= probability * probability.log2();
    }

    Ok(entropy)
}

/// Calculates the tokenization efficiency (entropy / avg token length)
/// This is useful for comparing how much information is packed per token
pub fn subword_efficiency(text: &str, tokenizer_name: Option<&str>) -> Result<f64> {
    let tokens = tokenize(text, tokenizer_name)?;

    if tokens.is_empty() {
        return Ok(0.0);
    }

    let token_name = tokenizer_name.unwrap_or("gpt2");
    let tokenizer = get_tokenizer(token_name)?;

    // First, get the entropy
    let entropy = subword_entropy(text, Some(token_name))?;

    // Now, get the average decoded token length
    let mut total_length = 0;
    for token_id in &tokens {
        let token_text = tokenizer.decode(&[*token_id], false)?;
        total_length += token_text.chars().count();
    }

    // Safe division with zero check
    let total_tokens = tokens.len();
    let avg_length = if total_tokens > 0 {
        total_length as f64 / total_tokens as f64
    } else {
        0.0
    };

    // Prevent division by zero
    if avg_length <= 0.0 {
        return Ok(0.0);
    }

    Ok(entropy / avg_length)
}

/// Gets comprehensive token metrics for a text in a single function call
pub fn get_token_metrics(text: &str, tokenizer_name: Option<&str>) -> Result<HashMap<String, f64>> {
    let token_name = tokenizer_name.unwrap_or("gpt2");

    // Get the tokens once to avoid repeated tokenization
    let tokens = tokenize(text, Some(token_name))?;

    if tokens.is_empty() {
        let mut metrics = HashMap::new();
        metrics.insert("subword_token_count".to_string(), 0.0);
        metrics.insert("unique_subword_count".to_string(), 0.0);
        metrics.insert("subword_type_token_ratio".to_string(), 0.0);
        metrics.insert("subword_repetition_rate".to_string(), 0.0);
        metrics.insert("subword_entropy".to_string(), 0.0);
        metrics.insert("subword_efficiency".to_string(), 0.0);
        return Ok(metrics);
    }

    // Count frequency of each token
    let mut frequency: HashMap<u32, usize> = HashMap::new();
    for token in &tokens {
        *frequency.entry(*token).or_insert(0) += 1;
    }

    let total = tokens.len();
    let unique = frequency.len();
    let type_token_ratio = unique as f64 / total as f64;
    let repetition_rate = 1.0 - type_token_ratio;

    // Calculate entropy using Shannon's formula: -sum(p_i * log2(p_i))
    let total_f64 = total as f64;
    let mut entropy = 0.0;
    for &count in frequency.values() {
        let probability = count as f64 / total_f64;
        entropy -= probability * probability.log2();
    }

    // Calculate efficiency (using all tokens for consistency)
    let tokenizer = get_tokenizer(token_name)?;
    let mut total_length = 0;

    // Process all tokens to ensure accuracy
    for token_id in &tokens {
        let token_text = tokenizer.decode(&[*token_id], false)?;
        total_length += token_text.chars().count();
    }

    // Safe division with zero check
    let avg_length = if total > 0 {
        total_length as f64 / total as f64
    } else {
        0.0
    };
    let efficiency = if avg_length > 0.0 {
        entropy / avg_length
    } else {
        0.0
    };

    // Build metrics hashmap
    let mut metrics = HashMap::new();
    metrics.insert("subword_token_count".to_string(), total as f64);
    metrics.insert("unique_subword_count".to_string(), unique as f64);
    metrics.insert("subword_type_token_ratio".to_string(), type_token_ratio);
    metrics.insert("subword_repetition_rate".to_string(), repetition_rate);
    metrics.insert("subword_entropy".to_string(), entropy);
    metrics.insert("subword_efficiency".to_string(), efficiency);

    Ok(metrics)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gpt2_tokenize() {
        let text = "Hello, world!";
        let tokenizer_name = "gpt2";

        match encode_str(tokenizer_name, text) {
            Ok(tokens) => {
                println!("Tokens: {:?}", tokens);
                assert!(!tokens.is_empty());
            }
            Err(e) => {
                println!(
                    "Error in tokenization (this is acceptable if not connected to internet): {:?}",
                    e
                );
            }
        }
    }

    #[test]
    fn test_gpt2_encode_decode() {
        let text = "Hello, world!";
        let tokenizer_name = "gpt2";

        match encode_str(tokenizer_name, text) {
            Ok(tokens) => {
                println!("Tokens: {:?}", tokens);

                match decode_str(tokenizer_name, &tokens) {
                    Ok(decoded) => {
                        println!("Decoded: {}", decoded);
                        assert!(decoded.to_lowercase().contains("hello"));
                    }
                    Err(e) => {
                        println!("Error in decoding (this is acceptable if not connected to internet): {:?}", e);
                    }
                }
            }
            Err(e) => {
                println!(
                    "Error in tokenization (this is acceptable if not connected to internet): {:?}",
                    e
                );
            }
        }
    }

    #[test]
    fn test_gpt2_batch_encode() {
        let texts = ["Hello, world!", "How are you?"];
        let tokenizer_name = "gpt2";

        match encode_str_list(tokenizer_name, &texts) {
            Ok(token_batches) => {
                println!("Token batches: {:?}", token_batches);
                assert_eq!(token_batches.len(), texts.len());
            }
            Err(e) => {
                println!("Error in batch tokenization (this is acceptable if not connected to internet): {:?}", e);
            }
        }
    }

    #[test]
    fn test_token_metrics() {
        let text = "Hello, world! This is a test of the tokenization metrics. \
                   We want to see how the entropy and efficiency calculations work \
                   with different text inputs. Repeated tokens should affect the entropy.";

        match get_token_metrics(text, None) {
            Ok(metrics) => {
                println!("Token metrics: {:#?}", metrics);
                assert!(metrics.contains_key("subword_token_count"));
                assert!(metrics.contains_key("subword_entropy"));
                assert!(metrics.contains_key("subword_efficiency"));
            }
            Err(e) => {
                println!("Error calculating token metrics (this is acceptable if not connected to internet): {:?}", e);
            }
        }
    }
}
