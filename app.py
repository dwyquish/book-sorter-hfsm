import sys
# Add the src folder to system path so we can import modules from it
sys.path.append('src') 
from hfsm_engine import HFSMEngine
import streamlit as st
import pandas as pd
import json
import os

# 1. Page Config
st.set_page_config(page_title="HFSM Book Sorter", layout="wide")
st.title("📚 HFSM-Based Digital Book Sorter")
st.markdown("**Group 9 Prototype** | Deterministic Classification System")

# 2. Sidebar: Load Rules
with st.sidebar:
    st.header("⚙️ Rule Configuration")
    
    # Check if default exists
    default_rules_path = "data/rules.json"
    rules_data = None
    
    # Allow upload, fallback to default
    uploaded_rules = st.file_uploader("Upload Rules (JSON)", type=["json"])
    
    if uploaded_rules:
        rules_data = json.load(uploaded_rules)
        st.success("✅ Custom Rules Loaded")
    elif os.path.exists(default_rules_path):
        with open(default_rules_path, 'r') as f:
            rules_data = json.load(f)
        st.info("ℹ️ Using Default 'data/rules.json'")
    else:
        st.error("❌ No rules found! Please upload a JSON file.")

    # Show raw rules for debugging (Hidden by default)
    with st.expander("View Raw Rules"):
        st.json(rules_data)

# 3. Main Area: Load Data
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Input Data")
    uploaded_file = st.file_uploader("Upload Book List (CSV)", type=["csv"])
    
    if uploaded_file is None and os.path.exists("data/books.csv"):
        st.info("Using default 'data/books.csv' for demo.")
        df = pd.read_csv("data/books.csv")
    elif uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        df = None

    if df is not None:
        st.dataframe(df, height=300)

with col2:
    st.subheader("2. Classification Results")
    run_btn = st.button("🚀 Run Classification Engine", type="primary")
    
    if run_btn:
        if rules_data is None:
            st.error("Cannot run: No rules loaded.")
        elif df is None:
            st.error("Cannot run: No data loaded.")
        else:
            st.info("⏳ Engine running... Processing tokens...")
            
            # --- THE INTEGRATION POINT ---
            
            # 1. Initialize the Engine with the loaded rules
            engine = HFSMEngine(rules_data)
            
            # 2. Process every row
            results = []
            traces = []
            
            # Create a progress bar
            progress_bar = st.progress(0)
            total_rows = len(df)
            
            for index, row in df.iterrows():
                # Extract title (handle missing columns gracefully)
                title = str(row.get('Title', ''))
                
                # RUN THE CLASSIFICATION
                output = engine.classify(title)
                
                results.append(output['category'])
                traces.append(output['trace'])
                
                # Update progress
                progress_bar.progress((index + 1) / total_rows)
            
            # 3. Save results back to DataFrame
            df['Assigned Category'] = results
            df['Audit Trace'] = traces
            
            st.success("✅ Classification Complete!")
            
            # 4. Display Results
            st.dataframe(df, use_container_width=True)
            
            # 5. Download Button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download Results CSV",
                csv,
                "classified_books.csv",
                "text/csv",
                key='download-csv'
            )
            
            # 6. Audit Log Inspector
            st.markdown("### 🔍 Audit Log Inspector")
            selected_row = st.selectbox("Select a book to inspect its path:", df['Title'])
            if selected_row:
                row_data = df[df['Title'] == selected_row].iloc[0]
                st.code(f"Title: {row_data['Title']}\nResult: {row_data['Assigned Category']}\n\nPath:\n{row_data['Audit Trace']}")
