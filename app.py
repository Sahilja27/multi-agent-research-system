
import streamlit as st
from pipeline import run_research_pipeline
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Research AI | Multi-Agent System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- CUSTOM STYLING ----------------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    .hero {
        padding: 1.8rem;
        border-radius: 16px;
        background: linear-gradient(120deg, #101827, #243b60);
        color: white;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        font-size: 2.3rem;
        margin-bottom: 0.5rem;
    }

    .hero p {
        color: #d6e1f0;
        font-size: 1rem;
        margin-bottom: 0;
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,0.25);
        padding: 1rem;
        border-radius: 12px;
    }

    .section-note {
        color: #808b9a;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- SESSION STATE ----------------
if "research_data" not in st.session_state:
    st.session_state.research_data = None

if "research_topic" not in st.session_state:
    st.session_state.research_topic = ""

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🔬 Research AI")
    st.caption("Multi-agent research workspace")

    st.divider()

    st.markdown("### Research pipeline")
    st.markdown(
        """
        1. 🔎 Search Agent
        2. 📄 Reader Agent
        3. ✍️ Writer Agent
        4. 🧐 Critic Agent
        """
    )

    st.divider()

    st.markdown("### About")
    st.caption(
        "Powered by your existing Gemini, LangChain, "
        "web-search, scraping, writer and critic pipeline."
    )

    st.caption("API credentials remain in your local environment.")

# ---------------- HEADER ----------------
st.markdown(
    """
    <div class="hero">
        <h1>Research AI Workspace</h1>
        <p>
            Research a topic, collect web sources, analyze content,
            generate a report, and review its quality in one place.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- TOPIC INPUT ----------------
st.subheader("Start a new research task")

with st.form("research_form"):
    topic = st.text_area(
        "Research topic",
        placeholder=(
            "Example: Recent advances in agentic AI "
            "and multi-agent systems in 2026"
        ),
        height=100,
        help="Enter a specific topic for more focused research.",
    )

    submitted = st.form_submit_button(
        "🚀 Start Research",
        type="primary",
        use_container_width=True,
    )

# ---------------- RUN PIPELINE ----------------
if submitted:
    cleaned_topic = topic.strip()

    if not cleaned_topic:
        st.warning("Please enter a research topic before continuing.")
    else:
        try:
            with st.spinner(
                "Research in progress: searching, scraping, "
                "writing, and reviewing..."
            ):
                result = run_research_pipeline(cleaned_topic)

            if not isinstance(result, dict):
                raise ValueError(
                    "The research pipeline did not return a dictionary."
                )

            required_keys = [
                "search_results",
                "scraped_content",
                "report",
                "feedback",
            ]

            missing_keys = [
                key for key in required_keys if key not in result
            ]

            if missing_keys:
                raise ValueError(
                    "Pipeline output is missing: "
                    + ", ".join(missing_keys)
                )

            st.session_state.research_data = result
            st.session_state.research_topic = cleaned_topic

            st.success("Research completed successfully!")

        except Exception as exc:
            st.error(
                "Research failed. Check your API configuration, "
                "network connection, and terminal logs."
            )
            with st.expander("Technical error details"):
                st.code(f"{type(exc).__name__}: {exc}")

# ---------------- DISPLAY RESULTS ----------------
data = st.session_state.research_data

if data:
    st.divider()

    st.subheader("Research overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Pipeline stages", "4")

    with col2:
        report_text = str(data["report"])
        st.metric("Report words", f"{len(report_text.split()):,}")

    with col3:
        st.metric("Status", "Completed")

    st.caption(
        f"Topic: {st.session_state.research_topic}"
    )

    # Convert the report into a Markdown document.
    report_markdown = (
        f"# Research Report\n\n"
        f"**Topic:** {st.session_state.research_topic}\n\n"
        f"**Generated:** {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}\n\n"
        f"---\n\n"
        f"{report_text}\n"
    )

    st.download_button(
        label="⬇️ Download Report as Markdown",
        data=report_markdown,
        file_name="research_report.md",
        mime="text/markdown",
        type="primary",
        use_container_width=True,
    )

    st.write("")

    # ---------------- RESULTS TABS ----------------
    search_tab, scraped_tab, report_tab, critic_tab = st.tabs(
        [
            "🔎 Search Results",
            "📄 Scraped Content",
            "📝 Final Report",
            "🧐 Critic Feedback",
        ]
    )

    with search_tab:
        st.subheader("Search agent output")
        st.caption("Sources, URLs, and summaries returned by your search agent.")

        if data["search_results"]:
            st.markdown(str(data["search_results"]))
        else:
            st.info("No search results were returned.")

    with scraped_tab:
        st.subheader("Reader agent output")
        st.caption("Extracted facts and page summaries from your reader agent.")

        if data["scraped_content"]:
            st.markdown(str(data["scraped_content"]))
        else:
            st.info("No scraped content was returned.")

    with report_tab:
        st.subheader("Generated research report")
        st.caption("The report produced by your existing writer chain.")

        if data["report"]:
            st.markdown(report_text)
        else:
            st.info("No report was generated.")

    with critic_tab:
        st.subheader("Critic agent feedback")
        st.caption("Review returned by your existing critic chain.")

        if data["feedback"]:
            st.markdown(str(data["feedback"]))
        else:
            st.info("No critic feedback was returned.")

else:
    st.info(
        "Enter a research topic above and click **Start Research** "
        "to generate your first report."
    )
