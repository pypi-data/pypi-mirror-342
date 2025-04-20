//! # Character Analysis Module
//!
//! This module provides comprehensive analysis of text at the character level,
//! offering a wide range of metrics and categorizations for detailed text analysis.
//!
//! ## Core Components
//!
//! * `unicode`: Basic character metrics, counts, and ratios
//! * `categories`: Unicode category classification and frequency analysis
//!
//! The character module forms the foundation of text analysis in Cheesecloth,
//! providing the building blocks for higher-level metrics while optimizing for
//! performance with non-allocating algorithms and efficient data structures.

pub mod categories;
pub mod unicode;
