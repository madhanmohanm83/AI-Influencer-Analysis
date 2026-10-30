import streamlit as st
import pandas as pd
import plotly.express as px
from src.database.database import (
    save_creators,
    save_search_history,
    get_search_history
)
from config import PROJECT_NAME

from src.api.channel_search import (
    search_creators,
    get_channel_video_metrics
)

from src.analytics.engagement import (
    get_recent_video_engagement,
    get_engagement_summary
)

from src.nlp.sentiment import (
    get_video_comments,
    analyze_comment_sentiment,
    get_sentiment_summary
)

from src.ml.recommendation import recommend_creators

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title=PROJECT_NAME,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. CUSTOM DASHBOARD THEME
# =====================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0B1020;
        color: #F8FAFC;
    }

    [data-testid="stSidebar"] {
        background-color: #10172B;
        border-right: 1px solid #26334D;
    }

    .brand {
        color: #22D3EE;
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 3px;
    }

    .hero {
        background: linear-gradient(
            115deg,
            #14213B,
            #202044,
            #2A1C4B
        );
        border: 1px solid #334155;
        border-radius: 22px;
        padding: 35px;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 42px;
        font-weight: 800;
    }

    .hero p {
        color: #CBD5E1;
        font-size: 15px;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            #151F35,
            #192541
        );
        border: 1px solid #334155;
        padding: 18px;
        border-radius: 15px;
    }

    div[data-testid="stMetricLabel"] {
        color: #94A3B8;
    }

    div[data-testid="stMetricValue"] {
        color: #F8FAFC;
    }

    .stButton > button {
        background: linear-gradient(
            100deg,
            #1B3150,
            #26345A
        );
        color: white;
        border: 1px solid #22D3EE;
        border-radius: 10px;
        min-height: 42px;
    }

    .stButton > button:hover {
        color: #22D3EE;
        border-color: #22D3EE;
    }

    .stDownloadButton > button {
        background-color: #1B3150;
        color: white;
        border: 1px solid #22D3EE;
        border-radius: 10px;
    }

    hr {
        border-color: #334155;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# 3. SESSION STATE
# =====================================================

if "creators" not in st.session_state:
    st.session_state.creators = []

if "comparison" not in st.session_state:
    st.session_state.comparison = None

if "saved_creators" not in st.session_state:
    st.session_state.saved_creators = []

if "engagement_data" not in st.session_state:
    st.session_state.engagement_data = {}

if "sentiment_data" not in st.session_state:
    st.session_state.sentiment_data = {}


# =====================================================
# 4. HELPER FUNCTIONS
# =====================================================

def creator_label(creator):
    return (
        f"{creator['channel_name']} "
        f"({creator['channel_id'][-6:]})"
    )


def get_creator_map():
    return {
        creator_label(creator): creator
        for creator in st.session_state.creators
    }


def show_hero(title, description):
    st.markdown(
        f"""
        <div class="hero">
            <div class="brand">
                CREATOR INTELLIGENCE PRO
            </div>

            <h1>{title}</h1>

            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_creator_table(creators):

    if not creators:
        st.info("No creators available. Search first.")
        return

    df = pd.DataFrame(creators)

    columns = [
        "channel_name",
        "country",
        "subscribers",
        "total_views",
        "total_videos"
    ]

    st.dataframe(
        df[columns],
        use_container_width=True,
        hide_index=True
    )


def analyze_videos(channel_id):

    videos = get_recent_video_engagement(
        channel_id,
        max_videos=10
    )

    st.session_state.engagement_data[channel_id] = videos

    return videos


def render_engagement(creator):

    channel_id = creator["channel_id"]

    if st.button(
        "Analyze Video Performance",
        key=f"engagement_{channel_id}"
    ):

        try:

            with st.spinner("Analyzing YouTube videos..."):

                videos = analyze_videos(channel_id)

            if videos.empty:
                st.warning("No public videos found.")

            else:
                st.success(
                    f"{len(videos)} videos analyzed successfully."
                )

        except Exception as error:

            st.error(f"Engagement error: {error}")

    videos = st.session_state.engagement_data.get(
        channel_id
    )

    if videos is None:
        st.info("Click Analyze Video Performance to begin.")
        return

    if videos.empty:
        st.warning("No video data available.")
        return

    summary = get_engagement_summary(videos)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Videos Analyzed",
        summary["total_videos"]
    )

    col2.metric(
        "Total Views",
        f"{summary['total_views']:,}"
    )

    col3.metric(
        "Total Likes",
        f"{summary['total_likes']:,}"
    )

    rate = summary["average_engagement_rate"]

    col4.metric(
        "Average Engagement",
        f"{rate:.2f}%" if rate is not None else "Unavailable"
    )

    st.subheader("Video Performance Details")

    st.dataframe(
        videos,
        use_container_width=True,
        hide_index=True
    )

    chart_data = videos.dropna(
        subset=["engagement_rate"]
    )

    if not chart_data.empty:

        fig = px.bar(
            chart_data,
            x="video_title",
            y="engagement_rate",
            title="Engagement Rate by Video"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_tickangle=-45
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.caption(
        "Engagement rate = (likes + comments) / views × 100. "
        "Analysis is based on up to 10 recent public videos."
    )

    st.download_button(
        "Download Video Report",
        videos.to_csv(index=False).encode("utf-8"),
        f"{channel_id}_videos.csv",
        "text/csv",
        key=f"download_{channel_id}"
    )


# =====================================================
# 5. LEFT SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">CREATOR INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    st.markdown("## Creator Intelligence Pro")

    st.caption("YouTube Creator Analytics")

    st.divider()

    st.markdown("### WORKSPACE")

    page = st.radio(
        "Navigation",
        [
            "Discover Influencers",
            "Compare Creators",
            "Saved Shortlist",
            "Creator Profile",
            "Video Performance",
            "AI Recommendations",
            "Search History",
            "Dashboard Overview"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### PLATFORM")

    st.markdown("▶️ YouTube Data API v3")

    st.caption(
        "Public channel and video statistics."
    )

    st.divider()

    st.caption(
        f"Saved creators: "
        f"{len(st.session_state.saved_creators)}"
    )


# =====================================================
# 6. COMMON DATA
# =====================================================

creators = st.session_state.creators

creator_map = get_creator_map()


# =====================================================
# 7. DISCOVER INFLUENCERS
# =====================================================

if page == "Discover Influencers":

    show_hero(
        "Find the right creators. Compare the evidence.",
        "Discover YouTube creators based on products, brands "
        "and marketing campaign topics."
    )

    st.header("🔎 Discover Influencers")

    with st.container(border=True):

        keyword = st.text_input(
            "Product or Brand",
            placeholder="Technology, Gaming, Skincare..."
        )

        max_results = st.select_slider(
            "Number of creators to find",
            options=[5, 10, 15, 20, 25, 30, 40, 50],
            value=10
        )

        if st.button(
            "Search YouTube Creators →",
            type="primary"
        ):

            if not keyword.strip():

                st.warning("Enter a search keyword.")

            else:

 
                try:

                    with st.spinner("Searching YouTube..."):

                        st.session_state.creators = search_creators(
                            keyword.strip(),
                            max_results
                        )

                        # Save creators permanently in SQLite
                        save_creators(st.session_state.creators)

                        # Save search keyword and result count
                        save_search_history(
                            keyword.strip(),
                            len(st.session_state.creators)
                        )

                        st.session_state.comparison = None
                        st.session_state.engagement_data = {}
                        st.session_state.sentiment_data = {}

                    st.rerun()

                except Exception as error:

                    st.error(f"Search failed: {error}")

                except Exception as error:

                    st.error(f"Search failed: {error}")

    creators = st.session_state.creators

    if creators:

        df = pd.DataFrame(creators)

        st.success(
            f"Found {len(creators)} creators"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Creators Found",
            len(df)
        )

        col2.metric(
            "Total Subscribers",
            f"{df['subscribers'].sum():,}"
        )

        col3.metric(
            "Total Channel Views",
            f"{df['total_views'].sum():,}"
        )

        st.subheader("Creator Search Results")

        show_creator_table(creators)

        st.download_button(
            "Download Creator CSV",
            df.to_csv(index=False).encode("utf-8"),
            "youtube_creators.csv",
            "text/csv"
        )

        st.divider()

        st.subheader("Save Creators to Shortlist")

        selected = st.multiselect(
            "Select creators",
            options=list(creator_map.keys())
        )

        if st.button("Save Selected Creators"):

            existing_ids = {
                c["channel_id"]
                for c in st.session_state.saved_creators
            }

            added = 0

            for label in selected:

                creator = creator_map[label]

                if creator["channel_id"] not in existing_ids:

                    st.session_state.saved_creators.append(
                        creator
                    )

                    existing_ids.add(
                        creator["channel_id"]
                    )

                    added += 1

            st.success(
                f"{added} creators added to shortlist."
            )


# =====================================================
# 8. COMPARE CREATORS
# =====================================================

elif page == "Compare Creators":

    show_hero(
        "Compare Creators",
        "Compare YouTube channels using public performance data."
    )

    st.header("⚖️ Creator Comparison")

    if not creators:

        st.info(
            "Go to Discover Influencers and search creators first."
        )

    else:

        selected = st.multiselect(
            "Select 2 to 5 creators",
            options=list(creator_map.keys()),
            max_selections=5
        )

        if st.button(
            "Compare Selected Creators",
            type="primary"
        ):

            if len(selected) < 2:

                st.warning("Select at least two creators.")

            else:

                rows = []

                progress = st.progress(0)

                try:

                    for index, label in enumerate(selected):

                        creator = creator_map[label]

                        channel_id = creator["channel_id"]

                        with st.spinner(
                            f"Analyzing {creator['channel_name']}..."
                        ):

                            metrics = get_channel_video_metrics(
                                channel_id,
                                max_videos=10
                            )

                        rows.append({

                            "Channel": creator["channel_name"],

                            "Subscribers": creator["subscribers"],

                            "Total Channel Views": creator["total_views"],

                            "Total Videos": creator["total_videos"],

                            "Sample Videos": metrics["sample_videos"],

                            "Sample Video Views": metrics["sample_views"],

                            "Sample Video Likes": metrics["sample_likes"],

                            "Videos With Visible Likes": metrics[
                                "videos_with_visible_likes"
                            ]

                        })

                        progress.progress(
                            (index + 1) / len(selected)
                        )

                    st.session_state.comparison = pd.DataFrame(rows)

                except Exception as error:

                    st.error(
                        f"Comparison failed: {error}"
                    )

        comparison = st.session_state.comparison

        if comparison is not None:

            st.subheader("Comparison Table")

            st.dataframe(
                comparison,
                use_container_width=True,
                hide_index=True
            )

            st.subheader("🏆 Category Winners")

            metrics = [
                "Subscribers",
                "Total Channel Views",
                "Sample Video Views",
                "Sample Video Likes"
            ]

            columns = st.columns(4)

            for col, metric in zip(columns, metrics):

                winner = comparison.loc[
                    comparison[metric].idxmax()
                ]

                col.metric(
                    metric,
                    winner["Channel"],
                    f"{winner[metric]:,}"
                )

            ranking = comparison[["Channel"]].copy()

            ranking_metrics = metrics

            ranking["Overall Score"] = sum(
                comparison[metric].rank(
                    pct=True,
                    method="average"
                )
                for metric in ranking_metrics
            ) / len(ranking_metrics) * 100

            ranking = ranking.sort_values(
                "Overall Score",
                ascending=False
            )

            st.subheader("🥇 Overall Creator Ranking")

            st.dataframe(
                ranking,
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "This is a relative comparison score based on "
                "four public metrics, not a prediction of creator quality."
            )

            chart_metric = st.selectbox(
                "Select Chart Metric",
                metrics + ["Total Videos"]
            )

            fig = px.bar(
                comparison,
                x="Channel",
                y=chart_metric,
                title=f"Creator Comparison: {chart_metric}",
                text_auto=True
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.download_button(
                "Download Comparison CSV",
                comparison.to_csv(index=False).encode("utf-8"),
                "creator_comparison.csv",
                "text/csv"
            )


# =====================================================
# 9. SAVED SHORTLIST
# =====================================================

elif page == "Saved Shortlist":

    show_hero(
        "Saved Shortlist",
        "Manage your selected YouTube creators."
    )

    st.header("⭐ Saved Creators")

    saved = st.session_state.saved_creators

    if not saved:

        st.info(
            "Your shortlist is empty. "
            "Save creators from Discover Influencers."
        )

    else:

        show_creator_table(saved)

        saved_map = {
            creator_label(c): c
            for c in saved
        }

        remove = st.multiselect(
            "Select creators to remove",
            options=list(saved_map.keys())
        )

        if st.button("Remove Selected Creators"):

            remove_ids = {
                saved_map[label]["channel_id"]
                for label in remove
            }

            st.session_state.saved_creators = [
                c for c in saved
                if c["channel_id"] not in remove_ids
            ]

            st.rerun()

        saved_df = pd.DataFrame(saved)

        st.download_button(
            "Download Shortlist CSV",
            saved_df.to_csv(index=False).encode("utf-8"),
            "saved_creators.csv",
            "text/csv"
        )

    st.caption(
        "Shortlist currently remains available in this Streamlit session."
    )


# =====================================================
# 10. CREATOR PROFILE
# =====================================================

elif page == "Creator Profile":

    show_hero(
        "Creator Profile",
        "Understand a creator beyond subscriber count."
    )

    if not creators:

        st.info(
            "Search for creators first."
        )

    else:

        selected = st.selectbox(
            "Choose Creator",
            options=list(creator_map.keys())
        )

        creator = creator_map[selected]

        st.header(
            creator["channel_name"]
        )

        st.write(
            creator.get("description", "")
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Subscribers",
            f"{creator['subscribers']:,}"
        )

        col2.metric(
            "Channel Views",
            f"{creator['total_views']:,}"
        )

        col3.metric(
            "Total Videos",
            f"{creator['total_videos']:,}"
        )

        st.write(
            "**Country:**",
            creator.get("country") or "Not available"
        )

        st.write(
            "**Channel ID:**",
            creator["channel_id"]
        )

        st.info(
            "Detailed audience age, gender and viewer geography "
            "are not available through this public channel lookup. "
            "They require authorized creator analytics access "
            "or creator-supplied data."
        )

        st.divider()

        st.subheader("📈 Engagement Analytics")

        render_engagement(creator)

        st.divider()

        st.subheader("💬 Audience Sentiment Analysis")

        channel_id = creator["channel_id"]

        if st.button(
            "Analyze Latest Video Comments",
            key=f"sentiment_{channel_id}"
        ):

            try:

                with st.spinner("Analyzing audience comments..."):

                    videos = get_recent_video_engagement(
                        channel_id,
                        max_videos=10
                    )

                    if videos.empty:

                        st.warning("No public videos found.")

                    else:

                        latest_video = videos.iloc[0]

                        comments = get_video_comments(
                            latest_video["video_id"],
                            max_comments=100
                        )

                        analyzed = analyze_comment_sentiment(
                            comments
                        )

                        st.session_state.sentiment_data[channel_id] = (
                            latest_video["video_title"],
                            analyzed
                        )

            except Exception as error:

                st.error(
                    f"Sentiment analysis failed: {error}"
                )

        sentiment_result = st.session_state.sentiment_data.get(
            channel_id
        )

        if sentiment_result:

            video_title, analyzed = sentiment_result

            if analyzed.empty:

                st.warning("No public comments available.")

            else:

                summary = get_sentiment_summary(analyzed)

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Comments",
                    summary["total_comments"]
                )

                col2.metric(
                    "Positive",
                    summary["positive"]
                )

                col3.metric(
                    "Negative",
                    summary["negative"]
                )

                col4.metric(
                    "Neutral",
                    summary["neutral"]
                )

                st.metric(
                    "Positive Percentage",
                    f"{summary['positive_percentage']:.2f}%"
                )

                st.caption(
                    f"Video analyzed: {video_title}"
                )

                sentiment_counts = (
                    analyzed["sentiment"]
                    .value_counts()
                    .rename_axis("Sentiment")
                    .reset_index(name="Comments")
                )

                fig = px.pie(
                    sentiment_counts,
                    names="Sentiment",
                    values="Comments",
                    title="Audience Sentiment Distribution"
                )

                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.dataframe(
                    analyzed[
                        [
                            "comment",
                            "sentiment",
                            "sentiment_score"
                        ]
                    ],
                    use_container_width=True,
                    hide_index=True
                )

                st.caption(
                    "TextBlob sentiment is approximate. "
                    "Sarcasm and multilingual comments may be "
                    "misclassified. This sample covers one video."
                )

                st.download_button(
                    "Download Sentiment Report",
                    analyzed.to_csv(index=False).encode("utf-8"),
                    "sentiment_report.csv",
                    "text/csv"
                )


# =====================================================
# 11. VIDEO PERFORMANCE
# =====================================================

elif page == "Video Performance":

    show_hero(
        "Video Performance",
        "Discover which videos attract audience interaction."
    )

    if not creators:

        st.info(
            "Search for creators first."
        )

    else:

        selected = st.selectbox(
            "Select Creator",
            options=list(creator_map.keys())
        )

        creator = creator_map[selected]

        render_engagement(creator)

# =====================================================
# 12. AI RECOMMENDATIONS
# =====================================================

elif page == "AI Recommendations":

    show_hero(
        "AI Influencer Recommendations",
        "Find creators that best match your brand or product."
    )

    creators = st.session_state.creators

    if not creators:

        st.warning(
            "Go to Discover Influencers and search creators first."
        )

    else:

        st.subheader("Brand and Product Matching")

        brand_keyword = st.text_input(
            "Enter your brand, product or campaign keyword",
            placeholder="Example: skincare, fitness, technology"
        )

        st.caption(
            "The recommendation engine compares your keyword "
            "with creator channel names and descriptions."
        )

        if st.button(
            "Generate AI Recommendations",
            type="primary"
        ):

            if not brand_keyword.strip():

                st.warning("Please enter a brand or product keyword.")

            else:

                try:

                    with st.spinner(
                        "Analyzing creators and calculating scores..."
                    ):

                        recommendations = recommend_creators(
                            creators,
                            brand_keyword,
                            st.session_state.engagement_data
                        )

                    if recommendations.empty:

                        st.info("No recommendations available.")

                    else:

                        st.success(
                            f"Successfully ranked "
                            f"{len(recommendations)} creators!"
                        )

                        st.subheader("Creator Rankings")

                        st.dataframe(
                            recommendations,
                            use_container_width=True,
                            hide_index=True
                        )

                        st.subheader("Suitability Score Comparison")

                        chart = px.bar(
                            recommendations,
                            x="Channel",
                            y="Suitability Score",
                            color="Suitability Score",
                            title="Top Creator Recommendations",
                            text="Suitability Score"
                        )

                        chart.update_layout(
                            xaxis_title="YouTube Creator",
                            yaxis_title="Suitability Score (0-100)",
                            xaxis_tickangle=-35
                        )

                        st.plotly_chart(
                            chart,
                            use_container_width=True
                        )

                        csv_data = recommendations.to_csv(
                            index=False
                        ).encode("utf-8")

                        st.download_button(
                            "Download Recommendations CSV",
                            data=csv_data,
                            file_name="creator_recommendations.csv",
                            mime="text/csv"
                        )

                        st.info(
                            "Note: These are provisional heuristic "
                            "scores, not predictions from a model "
                            "trained on real campaign outcomes. "
                            "Engagement score is zero for creators "
                            "whose engagement has not been analyzed."
                        )

                except Exception as error:

                    st.error(
                        f"Recommendation error: {error}"
                    )


# =====================================================
# 13. DASHBOARD OVERVIEW
# =====================================================


# =====================================================
# 12. DASHBOARD OVERVIEW
# =====================================================

elif page == "Dashboard Overview":

    show_hero(
        "Dashboard Overview",
        "Your creator research at a glance."
    )

    creators = st.session_state.creators

    saved = st.session_state.saved_creators

    comparison = st.session_state.comparison

    engagement_data = st.session_state.engagement_data

    sentiment_data = st.session_state.sentiment_data

    if creators:

        df = pd.DataFrame(creators)

        total_subscribers = int(
            df["subscribers"].sum()
        )

        total_views = int(
            df["total_views"].sum()
        )

    else:

        total_subscribers = 0

        total_views = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Creator Candidates",
        len(creators)
    )

    col2.metric(
        "Saved Creators",
        len(saved)
    )

    col3.metric(
        "Total Subscribers",
        f"{total_subscribers:,}"
    )

    col4.metric(
        "Total Channel Views",
        f"{total_views:,}"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Engagement Analyses",
        len(engagement_data)
    )

    col2.metric(
        "Sentiment Analyses",
        len(sentiment_data)
    )

    col3.metric(
        "Compared Creators",
        len(comparison) if comparison is not None else 0
    )

    st.subheader("Creator Search Results")

    show_creator_table(creators)

    st.divider()

    st.subheader("Available Data")

    st.info(
        "This project currently uses public YouTube channel "
        "and video statistics. Audience demographics require "
        "authorized analytics data. Authenticity indicators, "
        "content quality scoring and campaign ROI are future "
        "modules and are not yet implemented."
    )


# =====================================================
# 13. FOOTER
# =====================================================

st.divider()

st.caption(
    "Creator Intelligence Pro | "
    "Powered by YouTube Data API v3 | "
    "Public Data Analytics"
)