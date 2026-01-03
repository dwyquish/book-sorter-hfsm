import streamlit as st
import pandas as pd
import json
import os
from src.hfsm_engine import HFSMEngine

# -----------------------------------
# 1. Page Config
# -----------------------------------
st.set_page_config(page_title="HFSM Book Sorter", layout="wide")

st.title("HFSM-Based Digital Book Sorter")
st.markdown("### Automata & Language Theory — Group 9")

# -----------------------------------
# 2. Sidebar: Rule Configuration
# -----------------------------------
with st.sidebar:
    st.header("Configuration")
    
    rule_file = st.file_uploader("Upload Rules (JSON)", type=["json"])
    
    rules = None
    if rule_file:
        try:
            rules = json.load(rule_file)
            st.success("✅ Custom rules loaded!")
        except Exception as e:
            st.error(f"Invalid JSON: {e}")
    else:
        default_path = "data/rules.json"
        if os.path.exists(default_path):
            with open(default_path, "r", encoding="utf-8") as f:
                rules = json.load(f)
            st.success("✅ Default rules loaded.")
        else:
            st.warning("⚠️ No rules found. Please upload a JSON file.")

# Initialize Engine
engine = None
if rules:
    try:
        engine = HFSMEngine(rules)
    except ValueError as e:
        st.error(f"❌ Rule Validation Error: {e}")
        st.stop()

# -----------------------------------
# 3. Main Layout
# -----------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Upload Data")
    data_file = st.file_uploader("Upload Book List (CSV)", type=["csv"])

    if not data_file and os.path.exists("data/books.csv"):
        st.info("ℹ️ Using default 'data/books.csv' for demo.")
        df = pd.read_csv("data/books.csv")
    elif data_file:
        df = pd.read_csv(data_file)
    else:
        df = None

# -----------------------------------
# 4. Processing & State Management
# -----------------------------------
if df is not None:
    # Check for required column
    if "Title" not in df.columns:
        st.error("❌ CSV must contain a 'Title' column.")
    else:
        with col1:
            st.dataframe(df, height=150)

        with col2:
            st.subheader("2. Results")
            
            # THE FIX: We use session_state to remember that we already ran the tool
            if "classified_df" not in st.session_state:
                st.session_state.classified_df = None

            run_btn = st.button("🚀 Run Classification", type="primary")

            # Logic: If button clicked, process and SAVE to session state
            if run_btn and engine:
                st.info("⏳ Processing with HFSM...")
                
                categories = []
                traces = []
                progress_bar = st.progress(0)
                
                for i, title in enumerate(df["Title"]):
                    result = engine.classify(str(title))
                    categories.append(result["category"])
                    traces.append(result["trace"])
                    progress_bar.progress((i + 1) / len(df))
                
                df["Category"] = categories
                df["Audit Trace"] = traces
                
                # SAVE RESULTS TO MEMORY
                st.session_state.classified_df = df
                st.success("✅ Classification complete!")

            # Logic: If results exist in memory, show them (even if button isn't clicked right now)
            if st.session_state.classified_df is not None:
                result_df = st.session_state.classified_df
                
                st.dataframe(result_df, use_container_width=True)
                
                # Download
                csv = result_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name="classified_books.csv",
                    mime="text/csv",
                )
                
                # -----------------------------------
                # 5. Inspector (Now persists correctly)
                # -----------------------------------
                st.markdown("---")
                st.subheader("🔍 State Transition Inspector")
                
                # Dropdown to select book
                book_titles = result_df["Title"].tolist()
                selected_book = st.selectbox("Select a book to trace:", book_titles)
                
                if selected_book:
                    # Filter the dataframe to find the row
                    row = result_df[result_df["Title"] == selected_book].iloc[0]
                    
                    st.info(f"**Final Category:** {row['Category']}")
                    st.caption("Detailed State Path:")
                    st.code(row['Audit Trace'], language="text")