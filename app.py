import streamlit as st
import pandas as pd
import json

# Page Config
st.set_page_config(page_title="HFSM Book Sorter", layout="wide")

st.title("📚 HFSM-Based Digital Book Sorter")
st.markdown("### Automata & Language Theory Group 9")

# Sidebar for Rules
with st.sidebar:
    st.header("⚙️ Configuration")
    rule_file = st.file_uploader("Upload Rules (JSON)", type=["json"])
    
    # Load default rules if nothing uploaded
    if not rule_file:
        with open('data/rules.json') as f:
            rules = json.load(f)
        st.success("Default rules loaded.")
    else:
        rules = json.load(rule_file)
        st.success("Custom rules loaded!")

# Main Area
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Upload Data")
    data_file = st.file_uploader("Upload Book List (CSV)", type=["csv"])

if data_file:
    df = pd.read_csv(data_file)
    
    with col2:
        st.subheader("2. Results")
        if st.button("🚀 Run Classification"):
            # -----------------------------------------------
            # TODO: CONNECT THE HFSM ENGINE HERE
            # For now, we vibe code a dummy result
            # -----------------------------------------------
            
            st.write("Processing with HFSM...")
            
            # Placeholder logic (Replace this with real engine later)
            results = []
            for title in df['Title']:
                if "Automata" in title or "Python" in title:
                    results.append("Computer Science")
                else:
                    results.append("Unknown/Review")
            
            df['Category'] = results
            st.dataframe(df, use_container_width=True)
            
            # Explainer / Audit Log (Crucial for your paper)
            with st.expander("See Audit Logs (State Transitions)"):
                st.code("START -> 'introduction' -> INTRO_SEEN -> 'to' -> PREP_SEEN -> 'automata' -> ACCEPT")