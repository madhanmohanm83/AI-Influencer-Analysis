# Creator Intelligence Pro – Project Report

## 1. Introduction

Creator Intelligence Pro is an AI-assisted YouTube creator discovery and analytics platform developed using Python and Streamlit.

It helps users discover, analyze, compare, and rank YouTube creators using publicly available channel and video information.

## 2. Problem Statement

Brands and marketing teams face difficulties identifying suitable YouTube creators for promotional campaigns.

Subscriber count alone is not sufficient to evaluate a creator. Engagement, content relevance, audience response, and creator activity are also important.

Manual collection and comparison of these metrics can be time-consuming.

## 3. Project Objectives

- Discover YouTube creators by keyword.
- Collect public channel statistics.
- Analyze video engagement.
- Compare multiple creators.
- Analyze available public comment sentiment.
- Calculate brand relevance.
- Rank creators using a weighted recommendation score.
- Store creator and search records.
- Provide downloadable analytical reports.

## 4. Proposed System

The proposed platform integrates YouTube API data collection, data analysis, NLP-based sentiment analysis, text similarity, creator recommendation, and dashboard visualization.

## 5. Implementation Modules

1. YouTube API integration
2. Creator discovery
3. Engagement analytics
4. Comment sentiment analysis
5. Brand relevance analysis
6. Creator recommendation engine
7. SQLite database management
8. Streamlit dashboard and reporting

## 6. Recommendation Weights

| Metric | Weight |
|---|---:|
| Reach | 25% |
| Engagement | 30% |
| Brand relevance | 35% |
| Activity | 10% |

These weights are provisional and represent a heuristic ranking approach.

## 7. Technology Stack

Python, Streamlit, YouTube Data API v3, Pandas, NumPy, Scikit-learn, TextBlob, NLTK, Plotly, and SQLite.

## 8. Limitations

- Public API data does not provide private audience demographics.
- Sentiment analysis may be less accurate for multilingual comments.
- Engagement analysis uses sampled public videos.
- Recommendation scores are not trained campaign ROI predictions.
- Public metrics cannot definitively establish creator authenticity.

## 9. Conclusion

Creator Intelligence Pro brings creator discovery and multiple analytical indicators into one dashboard. It provides a structured way to compare YouTube creators and support influencer selection decisions.
