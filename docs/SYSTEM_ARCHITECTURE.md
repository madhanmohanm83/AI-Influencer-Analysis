# System Architecture

## Architecture Overview

The application follows a modular Python architecture.

## Main Components

### 1. User Interface
Streamlit provides the dashboard and accepts creator search and brand keywords.

### 2. API Layer
The YouTube Data API v3 client handles API authentication and requests. The channel search module retrieves creator information and video metrics.

### 3. Analytics Layer
The engagement module analyzes public video views, likes, comments, and engagement rates.

### 4. NLP Layer
The sentiment module retrieves available public comments and classifies their sentiment.

### 5. Machine Learning and Text Similarity Layer
The recommendation module uses TF-IDF and cosine similarity for textual brand relevance and combines normalized indicators into a weighted score.

### 6. Database Layer
SQLite stores creator information, search history, and recommendation records.

### 7. Reporting Layer
Streamlit and Plotly present results, while CSV exports support further analysis.

## Data Flow

User Input -> Streamlit -> YouTube API -> Data Processing -> Analytics and NLP -> Recommendation Engine -> Dashboard and SQLite.

## Architecture Note

This describes the current logical architecture. It does not imply that every possible feature or data source is implemented.
