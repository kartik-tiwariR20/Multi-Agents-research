"""
Streamlit UI for the multi-agent research pipeline.

Run with:
    streamlit run app.py

Place this file next to agents.py, tools.py, pipeline.py and .env
"""

import streamlit as st
from agents import reader_agent, search_agent, writer_chain, critic_chain

# --------------------------------------------------------------------------
# Page config
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Research Agent Pipeline",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------------------------------
# CSS — glassmorphism + 3D tilt cards + animated gradient backdrop
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        #MainMenu, footer, header { visibility: hidden; }

        .stApp {
            background: #05060f;
            background-image:
                radial-gradient(circle at 12% 20%, rgba(99,102,241,0.28), transparent 40%),
                radial-gradient(circle at 85% 15%, rgba(217,70,239,0.22), transparent 42%),
                radial-gradient(circle at 50% 90%, rgba(16,185,129,0.16), transparent 45%),
                linear-gradient(180deg, #05060f 0%, #0a0e1f 100%);
            background-attachment: fixed;
        }

        .block-container { padding-top: 2.2rem; max-width: 1180px; }

        /* ---------- Hero ---------- */
        .hero {
            position: relative;
            text-align: center;
            padding: 3.2rem 2rem 2.6rem 2rem;
            margin-bottom: 2.2rem;
            border-radius: 26px;
            background: linear-gradient(135deg, rgba(99,102,241,0.18), rgba(217,70,239,0.14));
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow:
                0 25px 60px -20px rgba(99,102,241,0.45),
                inset 0 1px 0 rgba(255,255,255,0.08);
            backdrop-filter: blur(10px);
        }
        .hero .eyebrow {
            display: inline-block;
            padding: 0.35rem 1rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.14);
            color: #c7d2fe;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }
        .hero h1 {
            font-size: 3rem;
            font-weight: 900;
            letter-spacing: -0.03em;
            margin: 0;
            background: linear-gradient(135deg, #ffffff 10%, #c7d2fe 55%, #f0abfc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 10px 40px rgba(99,102,241,0.35);
        }
        .hero p {
            color: #94a3b8;
            font-size: 1.12rem;
            max-width: 640px;
            margin: 0.9rem auto 0 auto;
            line-height: 1.6;
        }

        /* ---------- Feature cards (3D tilt) ---------- */
        .feat-grid {
            perspective: 1200px;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.1rem;
            margin-bottom: 2.4rem;
        }
        @media (max-width: 900px) { .feat-grid { grid-template-columns: repeat(2, 1fr); } }

        .feat-card {
            position: relative;
            padding: 1.6rem 1.3rem;
            border-radius: 18px;
            background: linear-gradient(160deg, rgba(255,255,255,0.07), rgba(255,255,255,0.02));
            border: 1px solid rgba(255,255,255,0.10);
            box-shadow: 0 18px 38px -18px rgba(0,0,0,0.65), inset 0 1px 0 rgba(255,255,255,0.06);
            transform-style: preserve-3d;
            transition: transform 0.35s cubic-bezier(.2,.9,.3,1.3), box-shadow 0.35s ease, border-color 0.35s ease;
        }
        .feat-card:hover {
            transform: translateY(-10px) rotateX(6deg) rotateY(-6deg) scale(1.03);
            border-color: rgba(199,210,254,0.4);
            box-shadow: 0 30px 55px -18px rgba(99,102,241,0.55), inset 0 1px 0 rgba(255,255,255,0.12);
        }
        .feat-icon {
            font-size: 1.9rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 52px; height: 52px;
            border-radius: 14px;
            margin-bottom: 0.9rem;
            background: linear-gradient(135deg, rgba(99,102,241,0.35), rgba(217,70,239,0.28));
            box-shadow: 0 8px 20px -6px rgba(99,102,241,0.6);
        }
        .feat-card h4 {
            color: #f1f5f9;
            font-size: 1.02rem;
            font-weight: 700;
            margin: 0 0 0.45rem 0;
        }
        .feat-card p {
            color: #94a3b8;
            font-size: 0.87rem;
            line-height: 1.5;
            margin: 0;
        }

        /* ---------- Glass panel (input area) ---------- */
        .glass-panel {
            padding: 1.6rem 1.8rem;
            border-radius: 20px;
            background: rgba(255,255,255,0.045);
            border: 1px solid rgba(255,255,255,0.09);
            box-shadow: 0 20px 45px -22px rgba(0,0,0,0.7), inset 0 1px 0 rgba(255,255,255,0.06);
            margin-bottom: 1.8rem;
        }
        .glass-panel label { color: #cbd5e1 !important; font-weight: 600; }

        .stTextInput input {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            border-radius: 12px !important;
            color: #f1f5f9 !important;
            padding: 0.75rem 1rem !important;
        }
        .stTextInput input:focus {
            border-color: rgba(165,180,252,0.6) !important;
            box-shadow: 0 0 0 3px rgba(99,102,241,0.25) !important;
        }

        .stButton>button {
            background: linear-gradient(135deg, #6366f1, #d946ef);
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            padding: 0.75rem 1.4rem;
            box-shadow: 0 14px 30px -10px rgba(99,102,241,0.65);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px) scale(1.015);
            box-shadow: 0 18px 38px -10px rgba(217,70,239,0.6);
        }

        /* ---------- Step cards ---------- */
        .step-card {
            border-radius: 16px;
            padding: 1.1rem 1.4rem;
            margin-bottom: 0.85rem;
            background: rgba(255,255,255,0.045);
            border: 1px solid rgba(255,255,255,0.09);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
        }
        .step-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .step-head span.title {
            color: #e2e8f0;
            font-weight: 700;
            font-size: 0.98rem;
        }
        .pill {
            font-size: 0.7rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            padding: 0.22rem 0.7rem;
            border-radius: 999px;
        }
        .pill-run  { background: rgba(250,204,21,0.16); color: #fde047; }
        .pill-done { background: rgba(52,211,153,0.16); color: #6ee7b7; }
        .pill-err  { background: rgba(248,113,113,0.16); color: #fca5a5; }

        /* ---------- Report / feedback panels ---------- */
        .report-box {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.09);
            border-radius: 18px;
            padding: 1.8rem;
            box-shadow: 0 20px 45px -25px rgba(0,0,0,0.75);
        }

        .stTabs [data-baseweb="tab-list"] { gap: 0.4rem; }
        .stTabs [data-baseweb="tab"] {
            background: rgba(255,255,255,0.04);
            border-radius: 10px 10px 0 0;
            color: #94a3b8;
            padding: 0.6rem 1rem;
        }
        .stTabs [aria-selected="true"] {
            background: rgba(99,102,241,0.22) !important;
            color: #e0e7ff !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Hero
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <span class="eyebrow">Multi-Agent AI Workflow</span>
        <h1>🔎 Research Agent Pipeline</h1>
        <p>Four specialized AI agents work in sequence — searching, reading, writing
        and critiquing — to turn any topic into a polished, reviewed research report.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Feature cards
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="feat-grid">
        <div class="feat-card">
            <div class="feat-icon">🔍</div>
            <h4>Search Agent</h4>
            <p>Scans the web in real time to find recent, reliable sources on your topic.</p>
        </div>
        <div class="feat-card">
            <div class="feat-icon">📖</div>
            <h4>Reader Agent</h4>
            <p>Picks the most relevant result and scrapes it for deeper, richer context.</p>
        </div>
        <div class="feat-card">
            <div class="feat-icon">✍️</div>
            <h4>Writer Chain</h4>
            <p>Synthesizes the research into a clear, structured, well-written report.</p>
        </div>
        <div class="feat-card">
            <div class="feat-icon">🧐</div>
            <h4>Critic Chain</h4>
            <p>Reviews the draft for accuracy, gaps, and quality — and gives feedback.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# Input panel
# --------------------------------------------------------------------------
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
col1, col2 = st.columns([4, 1])
with col1:
    topic = st.text_input("Research topic", placeholder="e.g. The impact of quantum computing on cryptography")
with col2:
    st.write("")
    st.write("")
    run_clicked = st.button("🚀 Run Pipeline", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.session_state.result = None

# --------------------------------------------------------------------------
# Helper to render a live step card
# --------------------------------------------------------------------------
def step_card(placeholder, title, state_label, body=""):
    pill_class = {"running": "pill-run", "done": "pill-done", "error": "pill-err"}[state_label]
    pill_text = {"running": "RUNNING", "done": "DONE", "error": "ERROR"}[state_label]
    placeholder.markdown(
        f"""
        <div class="step-card">
            <div class="step-head">
                <span class="title">{title}</span>
                <span class="pill {pill_class}">{pill_text}</span>
            </div>
            {f'<div style="margin-top:0.6rem; color:#cbd5e1; font-size:0.88rem;">{body}</div>' if body else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------------------------------
# Run pipeline — real step-by-step execution, mirroring pipeline.py
# --------------------------------------------------------------------------
if run_clicked:
    if not topic or not topic.strip():
        st.warning("Please enter a topic before running the pipeline.")
    else:
        topic = topic.strip()
        state = {}

        st.markdown("### 🧠 Live pipeline progress")
        p1, p2, p3, p4 = st.empty(), st.empty(), st.empty(), st.empty()

        try:
            # Step 1 — Search
            step_card(p1, "Step 1 · Search Agent", "running", "Finding recent, reliable sources...")
            search = search_agent()
            search_result = search.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
            })
            state["search_results"] = search_result["messages"][-1].content
            step_card(p1, "Step 1 · Search Agent", "done", f"Found {len(state['search_results'])} chars of source material.")

            # Step 2 — Reader
            step_card(p2, "Step 2 · Reader Agent", "running", "Scraping the most relevant page...")
            reader = reader_agent()
            reader_result = reader.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800]}"
                )]
            })
            state["scraped_content"] = reader_result["messages"][-1].content
            step_card(p2, "Step 2 · Reader Agent", "done", f"Scraped {len(state['scraped_content'])} chars of detailed content.")

            # Step 3 — Writer
            step_card(p3, "Step 3 · Writer Chain", "running", "Drafting the report...")
            research_combined = (
                f"SEARCH RESULTS : \n {state['search_results']} \n\n"
                f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
            step_card(p3, "Step 3 · Writer Chain", "done", "Report draft complete.")

            # Step 4 — Critic
            step_card(p4, "Step 4 · Critic Chain", "running", "Reviewing the report...")
            state["feedback"] = critic_chain.invoke({"report": state["report"]})
            step_card(p4, "Step 4 · Critic Chain", "done", "Review complete.")

            st.session_state.result = state
            st.success("✅ Pipeline finished successfully.")

        except Exception as e:
            st.error(f"❌ Pipeline failed: {e}")
            st.session_state.result = None

# --------------------------------------------------------------------------
# Results
# --------------------------------------------------------------------------
result = st.session_state.result

if result:
    st.markdown("### 📦 Results")
    tab_report, tab_feedback, tab_research = st.tabs(
        ["📄 Final Report", "🧐 Critic Feedback", "🔬 Raw Research"]
    )

    with tab_report:
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        report_text = result.get("report", "_No report generated._")
        report_text = getattr(report_text, "content", report_text)
        st.markdown(report_text)
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button("⬇️ Download report as .md", data=str(report_text), file_name="research_report.md", mime="text/markdown")

    with tab_feedback:
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        feedback_text = result.get("feedback", "_No feedback generated._")
        feedback_text = getattr(feedback_text, "content", feedback_text)
        st.markdown(feedback_text)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_research:
        with st.expander("🔍 Search Results", expanded=False):
            st.write(result.get("search_results", "—"))
        with st.expander("📖 Scraped Content", expanded=False):
            st.write(result.get("scraped_content", "—"))
elif not run_clicked:
    st.info("👆 Enter a topic above and click **Run Pipeline** to watch the agents work in real time.")