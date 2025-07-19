import streamlit as st
import pandas as pd
import altair as alt

# Set page config once globally, not inside function
st.set_page_config(page_title="Slang Usage Trends", layout="wide")

def load_data():
    try:
        df = pd.read_csv(r"slang_data\slang_usage_counts.csv")
        return df
    except FileNotFoundError:
        st.error("Could not find slang_usage_counts.csv. Make sure the file exists in slang_data/")
        st.stop()
    except pd.errors.EmptyDataError:
        st.warning("The slang usage counts file is empty.")
        st.stop()

def slang_usage_trend_analytics():
    st.title("📊 Slang Usage Analytics")
    st.markdown("Track the most frequently used slangs!")

    # Use a button to trigger refresh, store in session state to control reload
    if 'reload_data' not in st.session_state:
        st.session_state.reload_data = False

    if st.button("Refresh Data"):
        st.session_state.reload_data = True

    # Load or reload data based on session state
    if st.session_state.reload_data or 'data' not in st.session_state:
        st.session_state.data = load_data()
        st.session_state.reload_data = False  # reset after reload

    df = st.session_state.data

    # Check required columns
    if 'slang_term' not in df.columns or 'occurence' not in df.columns:
        st.error("CSV must contain 'slang_term' and 'occurence' columns.")
        st.stop()

    if df.empty:
        st.warning("No slang usage data found.")
        st.stop()

    # Sort by occurrence descending
    top_slangs = df.sort_values(by='occurence', ascending=False).head(10)

    # Bar chart
    bar = alt.Chart(top_slangs).mark_bar().encode(
        x=alt.X('occurence:Q', title='Total Occurrences'),
        y=alt.Y('slang_term:N', sort='-x', title='Slang Term'),
        tooltip=['slang_term', 'occurence']
    ).properties(
        title="Top 10 Most Used Slangs",
        height=400
    )

    st.altair_chart(bar, use_container_width=True)
