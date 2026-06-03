import streamlit as st
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

st.set_page_config(
    page_title="Research Intelligence",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@300;400;500&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stApp"] {
    background: #141210 !important;
    color: #f0ebe3 !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stApp"] {
    background:
        radial-gradient(ellipse 60% 40% at 20% 0%, rgba(212,160,78,.10) 0%, transparent 55%),
        radial-gradient(ellipse 50% 35% at 80% 100%, rgba(180,120,60,.07) 0%, transparent 55%),
        #141210 !important;
    min-height: 100vh;
}

#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; visibility: hidden !important; }

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #3a3228; border-radius: 2px; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 4rem 1rem 2rem;
    max-width: 760px;
    margin: 0 auto;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: .5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .65rem;
    font-weight: 400;
    letter-spacing: .22em;
    text-transform: uppercase;
    color: #c8943a;
    border: 1px solid rgba(200,148,58,.25);
    background: rgba(200,148,58,.06);
    border-radius: 999px;
    padding: .3rem 1rem;
    margin-bottom: 1.8rem;
}
.hero-eyebrow::before {
    content: '';
    width: 6px; height: 6px;
    background: #c8943a;
    border-radius: 50%;
    display: inline-block;
}
.hero h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: clamp(2.6rem, 5.5vw, 4.2rem) !important;
    font-weight: 400 !important;
    line-height: 1.08 !important;
    color: #f5efe6 !important;
    margin-bottom: .9rem !important;
    letter-spacing: -.01em !important;
}
.hero h1 em {
    font-style: italic;
    color: #d4a04e;
}
.hero-sub {
    font-size: 1rem;
    font-weight: 300;
    color: #7a7068;
    letter-spacing: .01em;
    line-height: 1.6;
}

/* ── Divider line ── */
.thin-rule {
    width: 40px;
    height: 1px;
    background: rgba(200,148,58,.3);
    margin: 2rem auto;
}

/* ── Input area ── */
.input-wrap {
    max-width: 700px;
    margin: 0 auto 3rem;
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 18px;
    padding: 2rem 2rem 1.6rem;
}

/* Streamlit input overrides — HIGH CONTRAST */
[data-testid="stTextInput"] > div > div {
    background: #1e1a16 !important;
    border: 1.5px solid rgba(200,148,58,.35) !important;
    border-radius: 10px !important;
}
[data-testid="stTextInput"] input {
    background: #1e1a16 !important;
    border: none !important;
    border-radius: 10px !important;
    color: #f5efe6 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 400 !important;
    padding: .8rem 1rem !important;
    caret-color: #d4a04e !important;
}
[data-testid="stTextInput"] input:focus {
    background: #221d18 !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(200,148,58,.18) !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: #4a4038 !important;
    font-style: italic;
}
[data-testid="stTextInput"] label {
    color: #9a8e82 !important;
    font-size: .72rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: .12em !important;
    text-transform: uppercase !important;
    margin-bottom: .4rem !important;
}

/* ── Run button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #c8943a 0%, #a8742a 100%) !important;
    color: #0e0c09 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .9rem !important;
    font-weight: 600 !important;
    padding: .75rem 2rem !important;
    letter-spacing: .03em !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: filter .2s, transform .15s !important;
    margin-top: .6rem !important;
}
[data-testid="stButton"] > button:hover {
    filter: brightness(1.1) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
    filter: brightness(.95) !important;
}

/* ── Section label ── */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: .65rem;
    letter-spacing: .2em;
    text-transform: uppercase;
    color: #5a5248;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: .6rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,.05);
}

/* ── Step cards ── */
.step-card {
    background: rgba(255,255,255,.02);
    border: 1px solid rgba(255,255,255,.05);
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color .35s, background .35s;
}
.step-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    border-radius: 14px 0 0 14px;
    background: transparent;
    transition: background .35s;
}
.step-card.pending { opacity: .38; }
.step-card.active {
    border-color: rgba(200,148,58,.35);
    background: rgba(200,148,58,.04);
}
.step-card.active::after { background: #c8943a; }
.step-card.done {
    border-color: rgba(100,185,130,.25);
    background: rgba(100,185,130,.03);
}
.step-card.done::after { background: #64b982; }

.step-header {
    display: flex;
    align-items: center;
    gap: .8rem;
    margin-bottom: .3rem;
}
.step-num {
    width: 28px; height: 28px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: .72rem;
    font-weight: 500;
    flex-shrink: 0;
    transition: background .35s, color .35s;
}
.step-num.pending { background: rgba(255,255,255,.05); color: #5a5248; }
.step-num.active  { background: rgba(200,148,58,.18); color: #d4a04e; }
.step-num.done    { background: rgba(100,185,130,.15); color: #64b982; }

.step-title {
    font-size: .9rem;
    font-weight: 500;
    color: #e8e0d4;
    flex: 1;
}
.step-desc {
    font-size: .74rem;
    color: #5a5248;
    font-family: 'JetBrains Mono', monospace;
    margin-left: calc(28px + .8rem);
    margin-top: .1rem;
    letter-spacing: .02em;
}

/* ── Chips ── */
.chip {
    font-family: 'JetBrains Mono', monospace;
    font-size: .62rem;
    letter-spacing: .08em;
    border-radius: 999px;
    padding: .18rem .6rem;
    display: inline-block;
}
.chip-running {
    background: rgba(200,148,58,.12);
    color: #d4a04e;
    border: 1px solid rgba(200,148,58,.28);
}
.chip-done {
    background: rgba(100,185,130,.1);
    color: #64b982;
    border: 1px solid rgba(100,185,130,.25);
}

/* ── Output panels ── */
.out-panel {
    background: rgba(0,0,0,.3);
    border: 1px solid rgba(255,255,255,.05);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-top: .85rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .78rem;
    color: #8a8078;
    line-height: 1.75;
    max-height: 260px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}
.out-panel.prose {
    font-family: 'Inter', sans-serif;
    font-size: .88rem;
    color: #b8afa6;
    line-height: 1.7;
    max-height: 380px;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,.02) !important;
    border: 1px solid rgba(255,255,255,.06) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
    color: #b8afa6 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .88rem !important;
    font-weight: 500 !important;
}
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] {
    color: #c8c0b4 !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] button {
    background: rgba(100,185,130,.08) !important;
    color: #64b982 !important;
    border: 1px solid rgba(100,185,130,.22) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: .75rem !important;
    letter-spacing: .06em !important;
    padding: .5rem 1.2rem !important;
    width: auto !important;
    transition: background .2s !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: rgba(100,185,130,.16) !important;
    filter: none !important;
    transform: none !important;
}

/* ── Warning ── */
[data-testid="stAlert"] {
    background: rgba(200,148,58,.08) !important;
    border: 1px solid rgba(200,148,58,.2) !important;
    border-radius: 10px !important;
    color: #d4a04e !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] > div { border-top-color: #c8943a !important; }

/* ── Markdown in expanders ── */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #e8e0d4 !important; }
.stMarkdown p, .stMarkdown li { color: #b8afa6 !important; }
.stMarkdown a { color: #d4a04e !important; }
.stMarkdown code { background: rgba(255,255,255,.07) !important; color: #c8943a !important; border-radius: 4px; padding: .1em .35em; }
.stMarkdown strong { color: #e0d8cc !important; }
</style>
""", unsafe_allow_html=True)


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent Research Pipeline</div>
    <h1>Research<br><em>Intelligence</em></h1>
    <p class="hero-sub">Searches the web, scrapes top sources, writes a report,<br>and critiques it — fully automated.</p>
    <div class="thin-rule"></div>
</div>
""", unsafe_allow_html=True)


# ── Input ─────────────────────────────────────────────────────────────────────
with st.container():
    st.markdown('<div class="input-wrap">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Impact of quantum computing on cryptography",
        label_visibility="visible",
    )
    run_btn = st.button("Run Research Pipeline  →", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── Steps ─────────────────────────────────────────────────────────────────────
STEPS = [
    ("01", "Search Agent",  "Discovering recent and reliable sources"),
    ("02", "Reader Agent",  "Scraping top-ranked URLs for deep content"),
    ("03", "Writer Chain",  "Drafting a structured research report"),
    ("04", "Critic Chain",  "Reviewing, scoring and giving feedback"),
]


def render_pipeline(statuses: dict, outputs: dict):
    cols = st.columns(2, gap="medium")
    for i, (num, title, desc) in enumerate(STEPS):
        col = cols[i % 2]
        status = statuses.get(num, "pending")
        with col:
            chip_html = ""
            if status == "active":
                chip_html = '<span class="chip chip-running">● running</span>'
            elif status == "done":
                chip_html = '<span class="chip chip-done">✓ done</span>'

            out_html = ""
            if num in outputs and outputs[num]:
                raw = outputs[num]
                if isinstance(raw, list):
                    text = " ".join(
                        b.get("text", "") if isinstance(b, dict) else str(b)
                        for b in raw
                    )
                else:
                    text = str(raw)
                text = text[:1400] + ("…" if len(text) > 1400 else "")
                cls = "out-panel prose" if num == "03" else "out-panel"
                out_html = f'<div class="{cls}">{text}</div>'

            st.markdown(f"""
            <div class="step-card {status}">
                <div class="step-header">
                    <div class="step-num {status}">{num}</div>
                    <span class="step-title">{title}</span>
                    {chip_html}
                </div>
                <div class="step-desc">{desc}</div>
                {out_html}
            </div>
            """, unsafe_allow_html=True)


# ── Run ───────────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
        st.stop()

    state = {}
    statuses = {s[0]: "pending" for s in STEPS}
    outputs: dict = {}
    ph = st.empty()

    # Step 1 — Search
    statuses["01"] = "active"
    with ph.container():
        st.markdown('<div class="section-label">Pipeline</div>', unsafe_allow_html=True)
        render_pipeline(statuses, outputs)

    with st.spinner("Search agent working…"):
        sa = build_search_agent()
        sr = sa.invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]})
    state["search_results"] = sr["messages"][-1].content
    statuses["01"] = "done"
    outputs["01"] = state["search_results"]

    # Step 2 — Reader
    statuses["02"] = "active"
    with ph.container():
        st.markdown('<div class="section-label">Pipeline</div>', unsafe_allow_html=True)
        render_pipeline(statuses, outputs)

    with st.spinner("Reader agent scraping…"):
        ra = build_reader_agent()
        rr = ra.invoke({"messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{str(state['search_results'])[:800]}"
        )]})
    state["scraped_content"] = rr["messages"][-1].content
    statuses["02"] = "done"
    outputs["02"] = state["scraped_content"]

    # Step 3 — Writer
    statuses["03"] = "active"
    with ph.container():
        st.markdown('<div class="section-label">Pipeline</div>', unsafe_allow_html=True)
        render_pipeline(statuses, outputs)

    with st.spinner("Writer drafting report…"):
        combined = (
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({"topic": topic, "research": combined})
    statuses["03"] = "done"
    outputs["03"] = state["report"]

    # Step 4 — Critic
    statuses["04"] = "active"
    with ph.container():
        st.markdown('<div class="section-label">Pipeline</div>', unsafe_allow_html=True)
        render_pipeline(statuses, outputs)

    with st.spinner("Critic reviewing…"):
        state["feedback"] = critic_chain.invoke({"report": state["report"]})
    statuses["04"] = "done"
    outputs["04"] = state["feedback"]

    with ph.container():
        st.markdown('<div class="section-label">Pipeline</div>', unsafe_allow_html=True)
        render_pipeline(statuses, outputs)

    # ── Results ───────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Full Report</div>', unsafe_allow_html=True)
    with st.expander("Read complete report", expanded=True):
        st.markdown(state["report"])

    st.markdown('<div class="section-label" style="margin-top:1.5rem">Critic Feedback</div>', unsafe_allow_html=True)
    with st.expander("Read critic feedback", expanded=False):
        st.markdown(state["feedback"])

    full_doc = (
        f"# Research Report: {topic}\n\n{state['report']}\n\n"
        f"---\n## Critic Feedback\n\n{state['feedback']}"
    )
    st.download_button(
        label="⬇  Download Report (Markdown)",
        data=full_doc,
        file_name=f"research_{topic[:40].replace(' ', '_')}.md",
        mime="text/markdown",
    )