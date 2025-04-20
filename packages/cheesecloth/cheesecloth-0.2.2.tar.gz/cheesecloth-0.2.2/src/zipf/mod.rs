//! # Zipf's Law and Statistical Patterns
//!
//! This module provides analysis of statistical patterns in text, focusing on
//! Zipf's law and related power-law distributions in natural language.
//!
//! ## Key Features
//!
//! * Zipf fitness score calculation
//! * Power law exponent estimation
//! * Burstiness analysis (clustering of token occurrences)
//! * Vocabulary growth rate analysis
//! * Kullback-Leibler divergence for distribution comparison
//!
//! These statistical measures provide deep insights into text naturalness,
//! authorial style, and the fundamental structure of language. They can be
//! used to detect machine-generated text, assess writing quality, and
//! quantify differences between text corpora.

// removed unused imports
use std::collections::HashMap;

/// Calculates the Zipf fitness score for a frequency distribution
///
/// Zipf's law states that in natural language, the frequency of a word is inversely proportional
/// to its rank in the frequency table. This function calculates how well a given frequency
/// distribution fits this power law pattern.
///
/// # Arguments
///
/// * `frequencies` - A HashMap containing token to frequency count mapping
///
/// # Returns
///
/// A score between 0.0 and 1.0, where 1.0 indicates perfect Zipf distribution
pub fn calculate_zipf_fitness<T: std::hash::Hash + Eq>(frequencies: &HashMap<T, usize>) -> f64 {
    if frequencies.is_empty() {
        return 0.0;
    }

    // Sort by frequency (descending)
    let mut sorted_freqs: Vec<(usize, &T)> = frequencies
        .iter()
        .map(|(token, &count)| (count, token))
        .collect();

    sorted_freqs.sort_by(|a, b| b.0.cmp(&a.0)); // Sort by count (descending)

    // For a perfect Zipf distribution, frequency ∝ 1/rank
    // So f_i = C/i where C is a constant and i is the rank

    // Calculate the theoretical Zipf distribution for comparison
    let total_tokens: usize = frequencies.values().sum();
    let highest_freq = sorted_freqs[0].0;

    // Calculate the Zipf constant (C) based on the highest frequency
    let zipf_constant = highest_freq as f64; // C = f_1 * 1

    // Calculate the theoretical frequencies according to Zipf's law
    let mut theoretical_freqs = Vec::with_capacity(sorted_freqs.len());
    let mut theoretical_sum = 0.0;

    for i in 1..=sorted_freqs.len() {
        let expected_freq = zipf_constant / (i as f64);
        theoretical_freqs.push(expected_freq);
        theoretical_sum += expected_freq;
    }

    // Normalize theoretical frequencies to match the total token count
    let scaling_factor = total_tokens as f64 / theoretical_sum;

    for freq in &mut theoretical_freqs {
        *freq *= scaling_factor;
    }

    // Calculate the deviation from the theoretical Zipf distribution
    let mut sum_squared_diff = 0.0;
    let mut max_possible_diff = 0.0;

    for (i, &(actual_freq, _)) in sorted_freqs.iter().enumerate() {
        let theor_freq = theoretical_freqs[i];
        sum_squared_diff += (actual_freq as f64 - theor_freq).powi(2);
        max_possible_diff += theor_freq.powi(2); // Maximum possible deviation if all frequencies were 0
    }

    // Calculate the fitness score (1 - normalized deviation)
    // A score of 1.0 means perfect fit to Zipf's law
    let fitness = 1.0 - (sum_squared_diff / max_possible_diff).sqrt();

    // Handle edge cases and bound to [0, 1]
    fitness.clamp(0.0, 1.0)
}

/// Calculates the power law exponent (alpha) for a frequency distribution
///
/// For a power law distribution, the probability of occurrence is proportional
/// to frequency^(-alpha). In Zipf's law, alpha is typically close to 1.
///
/// # Arguments
///
/// * `frequencies` - A HashMap containing token to frequency count mapping
///
/// # Returns
///
/// The estimated power law exponent (alpha)
pub fn estimate_power_law_exponent<T: std::hash::Hash + Eq>(
    frequencies: &HashMap<T, usize>,
) -> f64 {
    if frequencies.is_empty() {
        return 0.0;
    }

    // Sort by frequency (descending)
    let mut sorted_freqs: Vec<usize> = frequencies.values().cloned().collect();
    sorted_freqs.sort_by(|a, b| b.cmp(a));

    // We will use logarithmic regression to estimate alpha
    // In a log-log plot, a power law appears as a straight line with slope -alpha

    let mut sum_ln_rank = 0.0;
    let mut sum_ln_freq = 0.0;
    let mut sum_ln_rank_ln_freq = 0.0;
    let mut sum_ln_rank_squared = 0.0;
    let n = sorted_freqs.len() as f64;

    for (i, &freq) in sorted_freqs.iter().enumerate() {
        if freq == 0 {
            continue; // Skip zero frequencies
        }

        let rank = (i + 1) as f64;
        let ln_rank = rank.ln();
        let ln_freq = (freq as f64).ln();

        sum_ln_rank += ln_rank;
        sum_ln_freq += ln_freq;
        sum_ln_rank_ln_freq += ln_rank * ln_freq;
        sum_ln_rank_squared += ln_rank.powi(2);
    }

    // Linear regression formula: slope = (n*sum(xy) - sum(x)*sum(y)) / (n*sum(x^2) - sum(x)^2)
    // For power law: alpha = -slope

    let denominator = n * sum_ln_rank_squared - sum_ln_rank.powi(2);

    if denominator.abs() < 1e-10 {
        return 0.0; // Avoid division by (near) zero
    }

    let slope = (n * sum_ln_rank_ln_freq - sum_ln_rank * sum_ln_freq) / denominator;

    // The power law exponent is the negative of the slope
    -slope
}

/// Calculate the token distribution burstiness
///
/// Burstiness measures how tokens tend to cluster together rather than
/// being evenly distributed throughout the text.
///
/// # Arguments
///
/// * `text` - The text to analyze
/// * `tokens` - The tokens to track for burstiness
///
/// # Returns
///
/// A burstiness score where higher values indicate more clustered/bursty distribution
pub fn calculate_burstiness(text: &str, tokens: &[&str]) -> f64 {
    if text.is_empty() || tokens.is_empty() {
        return 0.0;
    }

    // For each token, collect the positions where it appears
    let mut positions: HashMap<&str, Vec<usize>> = HashMap::new();

    // For simplicity, we'll use character positions
    for token in tokens {
        if token.is_empty() {
            continue;
        }

        // Find all occurrences of the token
        let mut start = 0;
        while let Some(pos) = text[start..].find(token) {
            let absolute_pos = start + pos;
            positions.entry(token).or_default().push(absolute_pos);
            start = absolute_pos + 1; // Move past this occurrence
        }
    }

    // Calculate the burstiness for each token and average them
    let mut total_burstiness = 0.0;
    let mut count = 0;

    for (_, pos_vec) in positions {
        if pos_vec.len() < 2 {
            continue; // Need at least 2 occurrences to calculate burstiness
        }

        // Calculate the gaps between occurrences
        let mut gaps = Vec::with_capacity(pos_vec.len() - 1);
        for i in 1..pos_vec.len() {
            gaps.push(pos_vec[i] - pos_vec[i - 1]);
        }

        // Calculate gap statistics
        let mean_gap = gaps.iter().sum::<usize>() as f64 / gaps.len() as f64;
        let variance = gaps
            .iter()
            .map(|&gap| (gap as f64 - mean_gap).powi(2))
            .sum::<f64>()
            / gaps.len() as f64;
        let std_dev = variance.sqrt();

        // Burstiness B = (σ - μ) / (σ + μ)
        // Where σ is the standard deviation and μ is the mean of the gaps
        if mean_gap > 0.0 {
            let burstiness = (std_dev - mean_gap) / (std_dev + mean_gap);

            // Normalize to range [0, 1] for easier interpretation
            // Burstiness in theory can range from -1 to 1, where:
            // -1 is for perfectly periodic (evenly spaced)
            // 0 is for random (Poisson distribution)
            // 1 is for extremely bursty distribution
            let normalized_burstiness = (burstiness + 1.0) / 2.0;

            total_burstiness += normalized_burstiness;
            count += 1;
        }
    }

    if count == 0 {
        return 0.0;
    }

    total_burstiness / count as f64
}

/// Calculates the Kullback-Leibler divergence between two frequency distributions
///
/// KL divergence measures how one probability distribution differs from another.
/// It's useful for comparing token distributions between texts.
///
/// # Arguments
///
/// * `distribution_p` - First token frequency HashMap
/// * `distribution_q` - Second token frequency HashMap (reference distribution)
///
/// # Returns
///
/// The KL divergence value (higher means more difference)
pub fn kl_divergence<T: std::hash::Hash + Eq + Clone>(
    distribution_p: &HashMap<T, usize>,
    distribution_q: &HashMap<T, usize>,
) -> f64 {
    if distribution_p.is_empty() || distribution_q.is_empty() {
        return 0.0;
    }

    // Calculate total counts for normalization
    let total_p: usize = distribution_p.values().sum();
    let total_q: usize = distribution_q.values().sum();

    if total_p == 0 || total_q == 0 {
        return 0.0;
    }

    // Create a merged set of all tokens
    let mut all_tokens = distribution_p.keys().cloned().collect::<Vec<_>>();
    for key in distribution_q.keys() {
        if !distribution_p.contains_key(key) {
            all_tokens.push(key.clone());
        }
    }

    // Calculate KL divergence: Σ P(x) * log(P(x) / Q(x))
    let mut kl_div = 0.0;

    for token in all_tokens {
        // Get counts, defaulting to 1 to avoid zeros (add-one smoothing)
        let count_p = distribution_p.get(&token).cloned().unwrap_or(1);
        let count_q = distribution_q.get(&token).cloned().unwrap_or(1);

        // Calculate probabilities
        let prob_p = count_p as f64 / (total_p + distribution_p.len()) as f64;
        let prob_q = count_q as f64 / (total_q + distribution_q.len()) as f64;

        // Add to divergence sum
        kl_div += prob_p * (prob_p / prob_q).ln();
    }

    kl_div
}

/// Analyze the rate of vocabulary introduction in a text
///
/// This function breaks the text into chunks and measures how quickly
/// new vocabulary is introduced throughout the text.
///
/// # Arguments
///
/// * `text` - The text to analyze
/// * `chunk_size` - The size of each chunk to analyze
///
/// # Returns
///
/// A structure containing vocabulary growth statistics
pub fn analyze_vocab_growth(text: &str, chunk_size: usize) -> VocabGrowthStats {
    // Default results
    let mut stats = VocabGrowthStats {
        chunks_analyzed: 0,
        average_new_tokens_per_chunk: 0.0,
        cumulative_vocab_sizes: Vec::new(),
    };

    if text.is_empty() || chunk_size == 0 {
        return stats;
    }

    // Split the text into chunks
    let chunks: Vec<&str> = text
        .as_bytes()
        .chunks(chunk_size)
        .map(|chunk| std::str::from_utf8(chunk).unwrap_or(""))
        .collect();

    if chunks.is_empty() {
        return stats;
    }

    // Track vocabulary (unique tokens) across chunks
    let mut cumulative_vocabulary = HashMap::new();
    let mut cumulative_vocab_sizes = Vec::with_capacity(chunks.len());
    let mut new_tokens_per_chunk = Vec::with_capacity(chunks.len());

    for chunk in &chunks {
        // We'll use whitespace tokenization for simplicity
        let tokens: Vec<&str> = chunk.split_whitespace().collect();

        // Count new tokens in this chunk
        let mut new_token_count = 0;

        for token in tokens {
            if !cumulative_vocabulary.contains_key(token) {
                cumulative_vocabulary.insert(token.to_string(), true);
                new_token_count += 1;
            }
        }

        new_tokens_per_chunk.push(new_token_count);
        cumulative_vocab_sizes.push(cumulative_vocabulary.len());
    }

    // Calculate statistics
    let average_new_tokens = if !chunks.is_empty() {
        new_tokens_per_chunk.iter().sum::<usize>() as f64 / chunks.len() as f64
    } else {
        0.0
    };

    stats.chunks_analyzed = chunks.len();
    stats.average_new_tokens_per_chunk = average_new_tokens;
    stats.cumulative_vocab_sizes = cumulative_vocab_sizes;

    stats
}

/// Structure to hold vocabulary growth statistics
#[derive(Debug, Clone)]
pub struct VocabGrowthStats {
    /// Number of chunks analyzed
    pub chunks_analyzed: usize,
    /// Average number of new tokens per chunk
    pub average_new_tokens_per_chunk: f64,
    /// Cumulative vocabulary size after each chunk
    pub cumulative_vocab_sizes: Vec<usize>,
}

/// Get all Zipf-related metrics for a token frequency distribution
///
/// # Arguments
///
/// * `frequencies` - A HashMap containing token to frequency count mapping
///
/// # Returns
///
/// A HashMap containing all calculated Zipf metrics
pub fn get_zipf_metrics<T: std::hash::Hash + Eq>(
    frequencies: &HashMap<T, usize>,
) -> HashMap<String, f64> {
    let mut metrics = HashMap::new();

    metrics.insert(
        "zipf_fitness_score".to_string(),
        calculate_zipf_fitness(frequencies),
    );
    metrics.insert(
        "power_law_exponent".to_string(),
        estimate_power_law_exponent(frequencies),
    );

    metrics
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_zipf_fitness_perfect() {
        // Create a perfect Zipf distribution: f_i = C/i
        let mut frequencies = HashMap::new();
        let zipf_constant = 100.0;

        for i in 1..=20 {
            let freq = (zipf_constant / i as f64).round() as usize;
            frequencies.insert(format!("token{}", i), freq);
        }

        let fitness = calculate_zipf_fitness(&frequencies);
        println!("Perfect Zipf fitness: {}", fitness);
        assert!(fitness > 0.9); // Should be very close to 1.0
    }

    #[test]
    fn test_zipf_fitness_uniform() {
        // Create a uniform distribution (not Zipf-like at all)
        let mut frequencies = HashMap::new();

        for i in 1..=20 {
            frequencies.insert(format!("token{}", i), 10); // All tokens have same frequency
        }

        let fitness = calculate_zipf_fitness(&frequencies);
        println!("Uniform distribution fitness: {}", fitness);
        assert!(fitness < 0.5); // Should be much lower than the perfect Zipf
    }

    #[test]
    fn test_power_law_exponent() {
        // Create a Zipf distribution with exponent close to 1
        let mut frequencies = HashMap::new();
        let zipf_constant = 100.0;

        for i in 1..=50 {
            let freq = (zipf_constant / i as f64).round() as usize;
            frequencies.insert(format!("token{}", i), freq);
        }

        let alpha = estimate_power_law_exponent(&frequencies);
        println!("Estimated power law exponent: {}", alpha);
        assert!((alpha - 1.0).abs() < 0.3); // Should be close to 1.0 for a Zipf distribution
    }

    #[test]
    fn test_burstiness() {
        // Text with bursty distribution of "token"
        let bursty_text = "token token token. Some other words here. token token more words. token token token token.";

        // Text with more evenly distributed occurrences of "token"
        let even_text = "token. Some words here. token. More words here. token. Yet more words. token. Final words.";

        let bursty_score = calculate_burstiness(bursty_text, &["token"]);
        let even_score = calculate_burstiness(even_text, &["token"]);

        println!("Bursty score: {}, Even score: {}", bursty_score, even_score);
        assert!(bursty_score > even_score); // Bursty text should have higher score
    }

    #[test]
    fn test_kl_divergence() {
        // Create two distributions with some differences
        let mut dist_p = HashMap::new();
        let mut dist_q = HashMap::new();

        dist_p.insert("a", 10);
        dist_p.insert("b", 5);
        dist_p.insert("c", 2);

        dist_q.insert("a", 5);
        dist_q.insert("b", 10);
        dist_q.insert("c", 2);

        let divergence = kl_divergence(&dist_p, &dist_q);
        println!("KL divergence: {}", divergence);
        assert!(divergence > 0.0); // Should be positive for different distributions

        // Divergence to self should be zero
        let self_divergence = kl_divergence(&dist_p, &dist_p);
        assert!(self_divergence < 1e-10); // Should be very close to 0
    }

    #[test]
    fn test_vocab_growth() {
        let text = "This is a test. This is only a test. If this were a real emergency, \
                    you would be instructed. New words appear as the text continues.";

        let stats = analyze_vocab_growth(text, 20); // 20-character chunks

        println!("Vocab growth stats: {:?}", stats);
        assert!(stats.chunks_analyzed > 0);
        assert!(stats.average_new_tokens_per_chunk > 0.0);

        // The vocabulary size should grow and then plateau
        assert!(stats.cumulative_vocab_sizes.last() > stats.cumulative_vocab_sizes.first());
    }
}
