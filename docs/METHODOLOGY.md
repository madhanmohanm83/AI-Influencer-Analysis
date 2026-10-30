# Methodology

## 1. Creator Discovery

The application searches YouTube channels using a user-provided keyword through YouTube Data API v3.

## 2. Channel Metrics

Public channel statistics include subscriber count, total views, and video count, subject to API availability.

## 3. Engagement Analysis

The application retrieves a sample of recent public videos and collects available views, likes, and comments.

Engagement rate is calculated by the engagement analytics module. It should be interpreted in the context of the sampled videos and available metrics.

## 4. Sentiment Analysis

Available public comments are analyzed using TextBlob polarity.

Comments are categorized as positive, negative, or neutral based on their polarity.

TextBlob is English-oriented, so multilingual sentiment results may be less reliable.

## 5. Brand Relevance

TF-IDF converts creator channel names and descriptions and the user-provided brand keyword into numerical text representations.

Cosine similarity estimates textual relevance between the brand keyword and each creator.

## 6. Recommendation Scoring

The current provisional weights are:

- Reach: 25%
- Engagement: 30%
- Brand relevance: 35%
- Activity: 10%

The scores are normalized relative to the current search result set.

The recommendation engine is a heuristic weighted scoring system, not a supervised model trained on historical campaign outcomes.

## 7. Data Storage

SQLite stores creator records, search history, and recommendation records.

## 8. Interpretation

The results are decision-support indicators. They do not guarantee creator authenticity, audience-brand affinity, or campaign ROI.
