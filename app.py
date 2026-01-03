import streamlit as st
import pandas as pd
import json
from src.hfsm_engine import HFSMEngine

# Page Config
st.set_page_config(page_title="HFSM Book Sorter", layout="wide")

st.title("HFSM-Based Digital Book Sorter")
st.markdown("### Automata & Language Theory — Group 9")

# -----------------------------------
# Sidebar: Rule Configuration
# -----------------------------------
with st.sidebar:
    st.header("Configuration")
    rule_file = st.file_uploader("Upload Rules (JSON)", type=["json"])

    if rule_file:
        rules = json.load(rule_file)
        st.success("Custom rules loaded!")
    else:
        with open("data/rules.json", "r", encoding="utf-8") as f:
            rules = json.load(f)
        st.success("Default rules loaded.")

# Initialize HFSM Engine
engine = HFSMEngine(rules)

# -----------------------------------
# Main Layout
# -----------------------------------
import streamlit as st
import pandas as pd
import json
from src.hfsm_engine import HFSMEngine

# Page Config
st.set_page_config(page_title="HFSM Book Sorter", layout="wide")

st.title("HFSM-Based Digital Book Sorter")
st.markdown("### Automata & Language Theory — Group 9")

# -----------------------------------
# Sidebar: Rule Configuration
# -----------------------------------
with st.sidebar:
    st.header("Configuration")
    rule_file = st.file_uploader("Upload Rules (JSON)", type=["json"])

    if rule_file:
        rules = json.load(rule_file)
        st.success("Custom rules loaded!")
    else:
        with open("data/rules.json", "r", encoding="utf-8") as f:
            rules = json.load(f)
        st.success("Default rules loaded.")

# Initialize HFSM Engine
engine = HFSMEngine(rules)

# -----------------------------------
# Main Layout
# -----------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Upload Data")
    data_file = st.file_uploader("Upload Book List (CSV)", type=["csv"])

if data_file:
    df = pd.read_csv(data_file)

    # Safety check (defense-friendly)
    if "Title" not in df.columns:
        st.error("CSV must contain a 'Title' column.")
        st.stop()

    with col2:
        st.subheader("2. Results")

        if st.button("Run Classification"):
            st.info("Processing with HFSM...")

            categories = []
            traces = []

            for title in df["Title"]:
                result = engine.classify(title)
                categories.append(result["category"])
                traces.append(result["trace"])

            df["Category"] = categories
            df["Audit Trace"] = traces

            st.dataframe(df, use_container_width=True)
            st.success("Classification complete!")
            # Downloadable Results
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name="classified_books.csv",
                mime="text/csv",
            )

            # Audit Log (Critical for Defense)
            with st.expander("See Audit Logs (State Transitions)"):
                st.markdown("Example DFA Execution Path:")
                if traces:
                    st.code(traces[0])
                st.markdown("Each title's audit trace shows the sequence of states traversed during classification.")
else:
    st.info("Please upload a CSV file containing the book list.")
