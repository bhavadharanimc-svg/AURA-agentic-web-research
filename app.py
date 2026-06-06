import streamlit as st
import requests
from bs4 import BeautifulSoup
from groq import Groq

# ── PASTE YOUR GROQ API KEY HERE ──
GROQ_API_KEY = "here your groq api key"
client = Groq(api_key=GROQ_API_KEY)

# ── SCRAPER ──
def scrape_url(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script","style","nav","footer","header","aside"]):
            tag.decompose()
        lines = [l.strip() for l in soup.get_text("\n").splitlines() if l.strip()]
        return "\n".join(lines)[:12000]
    except Exception as e:
        return f"ERROR: {e}"

# ── AGENT ──
def run_agent(context, goal, history):
    messages = [
        {"role": "system", "content": (
            "You are AURA, an Autonomous Web Research & Extraction Assistant. "
            "Use the scraped webpage content provided in the first message. "
            "Answer research goals with clean Markdown: tables for comparisons, "
            "bullets for facts. Never hallucinate. Be concise."
        )}
    ] + history + [{"role": "user", "content": goal}]

    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.3,
            max_tokens=1500,
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"ERROR: {e}"

# ── PAGE CONFIG ──
st.set_page_config(page_title="AURA", page_icon="🔍", layout="wide")

st.markdown("""
<h1 style='text-align:center;color:#6C63FF;'>🔍 AURA</h1>
<h4 style='text-align:center;color:gray;'>Autonomous Agentic Web Research & Extraction Assistant</h4>
<hr>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "scraped_text" not in st.session_state:
    st.session_state.scraped_text = ""
if "urls_done" not in st.session_state:
    st.session_state.urls_done = []

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("### ⚙️ AURA Settings")
    urls_raw = st.text_area("🌐 Target URLs (one per line)", height=150,
                            placeholder="https://en.wikipedia.org/wiki/AI\nhttps://groq.com")
    scrape_btn = st.button("🕷️ Scrape Pages", use_container_width=True)
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.scraped_text = ""
        st.session_state.urls_done = []
        st.rerun()
    if st.session_state.urls_done:
        st.success(f"✅ {len(st.session_state.urls_done)} page(s) loaded")
        for u in st.session_state.urls_done:
            st.caption(f"• {u[:50]}...")

# ── SCRAPE MULTIPLE URLS ──
if scrape_btn:
    urls = [u.strip() for u in urls_raw.splitlines() if u.strip()]
    if not urls:
        st.sidebar.warning("Enter at least one URL.")
    else:
        combined = ""
        done = []
        for url in urls:
            with st.spinner(f"Scraping {url[:40]}..."):
                result = scrape_url(url)
                if result.startswith("ERROR"):
                    st.sidebar.error(f"Failed: {url}")
                else:
                    combined += f"\n\n=== SOURCE: {url} ===\n{result}"
                    done.append(url)
        st.session_state.scraped_text = combined[:20000]
        st.session_state.urls_done = done
        st.session_state.chat_history = [
            {"role": "user", "content": f"Here is the scraped content:\n{st.session_state.scraped_text}"},
            {"role": "assistant", "content": f"✅ I've loaded {len(done)} page(s). Ask me anything about the content!"}
        ]
        st.rerun()

# ── CHAT UI ──
st.markdown("### 💬 Research Chat")

if not st.session_state.scraped_text:
    st.info("👈 Enter URLs in the sidebar and click **Scrape Pages** to begin.")
else:
    # Show chat history (skip first 2 system messages)
    for msg in st.session_state.chat_history[2:]:
        role = "🧑 You" if msg["role"] == "user" else "🤖 AURA"
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_q = st.chat_input("Ask AURA anything about the scraped pages...")
    if user_q:
        with st.chat_message("user"):
            st.markdown(user_q)

        with st.chat_message("assistant"):
            with st.spinner("AURA is thinking..."):
                answer = run_agent(
                    st.session_state.scraped_text,
                    user_q,
                    st.session_state.chat_history
                )
            st.markdown(answer)

        st.session_state.chat_history.append({"role": "user", "content": user_q})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

        # Download latest answer
        st.download_button("⬇️ Download Answer", answer, "aura_output.md", "text/markdown")

# ── FOOTER ──
st.markdown("""
<hr>
<p style='text-align:center;color:gray;font-size:12px;'>
AURA — Microsoft AI Hackathon 2026 | Groq + LLaMA 3.3
</p>
""", unsafe_allow_html=True)