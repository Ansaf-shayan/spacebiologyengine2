import streamlit as st
import pandas as pd
import numpy as np

# --- 1. Load Data ---
# The app looks for the CSV file in the same directory (where Colab runs)
try:
    df = pd.read_csv('space_biology_knowledge_base.csv')
except FileNotFoundError:
    st.error("Error: 'space_biology_knowledge_base.csv' not found. Please ensure the data extraction step was completed successfully.")
    st.stop() # Stop the app if data can't be loaded


# --- 2. Title and Instructions ---
st.set_page_config(layout="wide")
st.title("🚀 NASA Space Biology Knowledge Engine (AI-Generated)")
st.subheader("Explore structured findings from space biology abstracts.")

st.markdown("""
    This dynamic dashboard leverages **Gemini AI** to extract and structure key information
    from scientific abstracts, making it easy to search for the impacts of spaceflight
    on various organisms and biological systems.
""")

# --- 3. Sidebar Filters ---
st.sidebar.header("Filter the Knowledge Base")

# Filter 1: Organism Selection
organism_list = ['All Organisms'] + sorted(df['organism'].unique().tolist())
selected_organism = st.sidebar.selectbox(
    'Select Organism:',
    organism_list
)

# Filter 2: System Affected Search (Text input for broad search)
system_search = st.sidebar.text_input(
    'Search by System Affected (e.g., "muscle"):',
    ''
)

# --- 4. Apply Filters ---
filtered_df = df.copy()

# Filter by Organism
if selected_organism != 'All Organisms':
    filtered_df = filtered_df[filtered_df['organism'] == selected_organism]

# Filter by System Affected (Case-insensitive partial match)
if system_search:
    filtered_df = filtered_df[
        filtered_df['system_affected'].str.contains(system_search, case=False, na=False)
    ]

# --- 5. Display Results ---

st.header(f"Results: {len(filtered_df)} Abstracts Found")

if len(filtered_df) == 0:
    st.warning("No abstracts match your current filters. Try broadening your search.")
else:
    # Use st.dataframe for a neat, interactive, scrollable table view
    st.markdown("### Filtered Structured Data")

    # We select the columns we want to show in the main table
    display_cols = ['abstract_id', 'organism', 'system_affected', 'key_finding', 'summary']
    st.dataframe(filtered_df[display_cols], use_container_width=True, height=300)

    # --- 6. Detailed View Section (Optional but great for presentation) ---
    st.markdown("---")
    st.header("Detailed Abstract Summaries")

    # Allow user to select an abstract ID for a focused view
    selected_id = st.selectbox(
        'Select an Abstract ID for a detailed view:',
        filtered_df['abstract_id'].tolist()
    )

    if selected_id:
        detail = filtered_df[filtered_df['abstract_id'] == selected_id].iloc[0]
        st.write(f"### Details for {selected_id}")

        # Display key extracted fields in a clean format
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Organism", value=detail['organism'])
            st.metric(label="System Affected", value=detail['system_affected'])
        with col2:
            st.metric(label="Key Finding", value=detail['key_finding'])

        st.markdown(f"**AI-Generated Summary:**")
        st.info(detail['summary'])
