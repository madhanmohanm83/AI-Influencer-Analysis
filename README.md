# Creator Intelligence Pro
🚀 **Live Dashboard:** https://ai-influencer-analysis-gxwwyyjw6ubty2ebsrdw7l.streamlit.app/

💻 **GitHub Repository:** https://github.com/madhanmohanm83/AI-Influencer-Analysis
### AI-Assisted YouTube Creator Discovery, Analytics & Recommendation Platform

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)](https://streamlit.io/)
[![API](https://img.shields.io/badge/API-YouTube%20Data%20API%20v3-red)](https://developers.google.com/youtube/v3)
[![Database](https://img.shields.io/badge/Database-SQLite-lightgrey)](https://www.sqlite.org/)

## 1. Project Overview

Creator Intelligence Pro is a Python-based analytics platform designed to help brands and marketing teams discover, analyze, compare, and shortlist suitable YouTube creators.

The platform collects publicly available YouTube channel and video information through YouTube Data API v3. It applies engagement analytics, natural language processing, text similarity, and a weighted recommendation approach to support creator selection.

The application provides an interactive Streamlit dashboard for creator discovery, performance analysis, sentiment insights, comparisons, and recommendations.

## 2. Problem Statement

Brands and marketing teams often face challenges when selecting suitable YouTube influencers for promotional campaigns.

Selecting creators only by subscriber count may not provide a complete picture of their suitability. Engagement, content relevance, audience response, and creator activity are also important considerations.

Manually collecting and comparing these metrics across multiple channels is time-consuming.

This project addresses these challenges by bringing publicly available creator information and analytical indicators into a single platform.

## 3. Proposed Solution

Creator Intelligence Pro provides a centralized workflow to:

- Discover creators using keywords and niches.
- Retrieve public channel statistics.
- Analyze recent video engagement.
- Compare multiple creators.
- Analyze available public comment sentiment.
- Calculate brand-content relevance.
- Rank creators using a weighted suitability score.
- Store creator records and search history.
- Export analytical results as CSV reports.

## 4. Main Features

### Creator Discovery
Search YouTube channels using keywords and retrieve channel names, descriptions, subscriber counts, total views, and video counts.

### Engagement Analytics
Analyze sampled public videos using views, likes, comments, and engagement-rate indicators.

### Creator Comparison
Compare multiple creators using available channel and video performance metrics.

### Sentiment Analysis
Analyze available public comments and classify sentiment as positive, negative, or neutral using TextBlob-based polarity analysis.

### Brand Relevance
Use TF-IDF vectorization and cosine similarity to estimate the textual relevance between a brand/product keyword and creator channel descriptions.

### AI-Assisted Recommendations
Rank creators using reach, engagement, brand relevance, and activity indicators.

### Dashboard and Reports
Display analytical results through Streamlit and Plotly, with CSV export support.

### Database
Use SQLite to store creator records and search history.

## 5. System Workflow

1. User enters a creator niche, keyword, or brand/product keyword.
2. The application searches YouTube channels through YouTube Data API v3.
3. Channel statistics and descriptions are retrieved.
4. Recent public video metrics are collected for engagement analysis.
5. Available public comments are analyzed for sentiment.
6. TF-IDF and cosine similarity calculate textual brand relevance.
7. The recommendation engine calculates weighted suitability scores.
8. Creators are ranked and presented in the dashboard.
9. Creator records and search history are stored in SQLite.
10. Results can be exported for further analysis.

## 6. Recommendation Methodology

The current recommendation engine uses the following provisional weighted scoring model:

| Component | Weight |
|---|---:|
| Reach Score | 25% |
| Engagement Score | 30% |
| Brand Relevance Score | 35% |
| Activity Score | 10% |
| **Total** | **100%** |

Brand relevance is calculated using TF-IDF and cosine similarity.

The component scores are normalized relative to the current creator search results.

This is a heuristic recommendation model, not a supervised model trained on historical campaign outcomes. Scores should be interpreted as decision-support indicators rather than guaranteed campaign-performance predictions.

## 7. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web dashboard |
| YouTube Data API v3 | Public YouTube data retrieval |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Scikit-learn | TF-IDF and cosine similarity |
| TextBlob | Sentiment analysis |
| NLTK | NLP support |
| Plotly | Interactive charts |
| SQLite | Persistent local storage |
| SQLAlchemy | Database toolkit dependency |

## 8. Project Structure

```text
Creator-Intelligence-Pro/
|
|-- app.py
|-- config.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|
|-- src/
|   |-- api/
|   |   |-- youtube_client.py
|   |   |-- channel_search.py
|   |
|   |-- analytics/
|   |   |-- engagement.py
|   |
|   |-- ml/
|   |   |-- recommendation.py
|   |
|   |-- nlp/
|   |   |-- sentiment.py
|   |
|   |-- database/
|       |-- database.py
|
|-- data/
|-- models/
|-- notebooks/
|-- dashboard/
|-- tests/
|-- utils/
```

## 9. Installation and Setup

### Prerequisites

- Python 3.13
- Git
- YouTube Data API v3 key

### Step 1: Clone the repository

```powershell
git clone YOUR_GITHUB_REPOSITORY_URL
cd Creator-Intelligence-Pro
```

### Step 2: Create a virtual environment

```powershell
py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure API credentials

Create a `.env` file in the project root:

```env
YOUTUBE_API_KEY=your_youtube_api_key
```

Do not share or commit this file.

### Step 5: Run the dashboard

```powershell
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

## 10. Data Sources

The application uses publicly accessible YouTube information through YouTube Data API v3.

The API provides channel metadata, public statistics, video metadata, and available public comment information, subject to API permissions and quota limits.

No private creator account information is collected through this public-data workflow.

## 11. Limitations and Responsible Use

- Public YouTube API data does not provide private audience age and gender demographics.
- Engagement analysis uses a sample of public videos, not necessarily every video.
- Comments may be disabled, unavailable, or limited by API access.
- TextBlob sentiment analysis may be less reliable for multilingual comments.
- Brand relevance measures textual similarity, not actual audience-brand affinity.
- Public metrics cannot definitively prove fake followers or creator authenticity.
- Suitability scores are indicators and do not guarantee campaign success or ROI.
- API quota restrictions may limit the number of searches and requests.

## 12. Future Enhancements

- Persistent creator shortlists.
- Historical creator performance tracking.
- More advanced multilingual sentiment analysis.
- Creator niche classification.
- Improved anomaly indicators.
- Authorized creator analytics integration where account owners provide permission.
- Campaign performance feedback and recommendation-model validation.
- Automated PDF and Excel reports.

## 13. Security

API credentials are stored locally in `.env`.

The `.env` file, virtual environment, and local database files should not be uploaded to GitHub.

## 14. Project Status

This project is under active development. Features and recommendation methodology may evolve as testing and validation continue.

## 15. License

No open-source license has been specified.
