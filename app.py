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
            st.warning("⚠️ Engine not connected yet! (Waiting for Person A)")
            # This is where we will hook up Person A's code tomorrow.