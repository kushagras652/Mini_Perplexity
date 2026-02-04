import streamlit as st
from graph.pipeline import pipeline

st.set_page_config(
    page_title="Mini Perplexity",
    layout="wide"
)

st.title("🔍 Mini-Perplexity Research Agent")
st.caption("Autonomous research with grounding, verification, and reflection")

# ---- Sidebar ----
st.sidebar.header("Settings")
run_reflection = st.sidebar.checkbox(
    "Enable Deep Research (Self-Reflection)",
    value=True
)

max_sources = st.sidebar.slider(
    "Max Sources to Display",
    min_value=3,
    max_value=10,
    value=5
)

# ---- Input ----
query = st.text_input(
    "Enter your research query",
    placeholder="Explain autonomous AI agents in production systems"
)

run_button = st.button("Run Research")

# ---- Execution ----
if run_button and query:
    with st.status("Running autonomous research…", expanded=True) as status:
        try:
            st.write("🧠 Planning & Researching…")
            state = {
                "query": query,
                "enable_reflection": run_reflection
            }

            result = pipeline.invoke(state)

            status.update(
                label="Research complete",
                state="complete"
            )

        except Exception as e:
            status.update(
                label="Research failed",
                state="error"
            )
            st.error(str(e))
            st.stop()

    # ---- Answer ----
    st.subheader("📌 Answer")
    st.markdown(result["answer"])

    # ---- Sources ----
    if "docs" in result:
        st.subheader("📚 Sources")

        unique_sources = {}
        for d in result["docs"]:
            unique_sources[d["url"]] = d["content"]

        for i, (url, content) in enumerate(list(unique_sources.items())[:max_sources], 1):
            with st.expander(f"[{i}] {url}"):
                st.write(content)

else:
    st.info("Enter a query and click **Run Research**")
