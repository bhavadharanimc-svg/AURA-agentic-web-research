# 🔍 AURA — Autonomous Agentic Web Research & Extraction Assistant



---

## 🚀 What is AURA?

AURA is an autonomous web research agent that scrapes any webpage, reasons over the content using LLaMA 3.3, and lets you chat with the data — no static selectors, no manual parsing.

Just paste a URL, ask your question, and get structured Markdown output instantly.

---

## 🎯 Problem It Solves

Traditional scrapers break when websites update their layout. Enterprise teams waste thousands of hours manually reading pages to extract insights.

AURA fixes this by approaching web pages like a human analyst — it reads, understands, and answers questions about any page dynamically.

---

## ✨ Features

- 🌐 **Multi-URL Scraping** — research multiple pages at once
- 💬 **Chat Memory** — ask follow-up questions on the same scraped data
- 📊 **Structured Output** — tables, bullet points, summaries in Markdown
- ⬇️ **Download Results** — export any answer as a `.md` file
- ⚡ **Powered by Groq** — ultra-fast LLaMA 3.3 inference

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Scraper | BeautifulSoup4 + Requests |
| AI Agent | Groq API + LLaMA 3.3 70B |
| Language | Python 3.11 |

---

## ⚙️ Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/AURA-agentic-web-research
cd AURA-agentic-web-research
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Groq API key
Open `app.py` and replace:
```python
GROQ_API_KEY = "paste_your_groq_api_key_here"
```

### 4. Run
```bash
python -m streamlit run app.py
```

---

## 🧪 Example Use Cases

| URL | Research Goal |
|---|---|
| Wikipedia — AI page | Summarize and list key milestones in a table |
| Any SaaS pricing page | Compare all pricing plans and features |
| Hardware docs | Extract technical specs |
| News article | Summarize key facts as bullets |

---

## 📐 Architecture

```
[Target URLs] → [BS4 Scraper] → [Sanitized Text (max 12k chars)]
                                          │
[User Goal] → [Chat History] ─────────────┤
                                          ▼
[Markdown Output] ← [Groq LLaMA 3.3 Agent]
```

---

## 👩‍💻 Built By

**Bhavadharani Mummoorthi** — B.Tech Information Technology,KPRIET,Coimbatore

