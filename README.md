# 🧠 BriefMind - Weekly Research Assistant using AI Agents

**BriefMind** is an AI-powered research assistant that automatically **fetches**, **stores**, **summarizes**, and **notifies** you with the most relevant and trending research and technology news — all done autonomously like a research agent.

It integrates intelligent fetchers, local vector storage, large language model summarization, and email-based notifications to help researchers and tech enthusiasts stay up-to-date without the noise.

---

## 🤖 Powered by AI Agents

At its core, BriefMind works like a **modular AI agent system**, with each component acting like a dedicated sub-agent:

| Agent Role         | Description |
|--------------------|-------------|
| 🕵️‍♂️ Fetchers      | Collect data from multiple research/news APIs (e.g., ArXiv, HackerNews, etc.) |
| 🧠 Summarizer Agent | Uses an LLM to distill key ideas from content |
| 💾 Memory Agent     | Stores information in a vector store (ChromaDB) for semantic querying |
| 📬 Notifier Agent   | Generates and sends a weekly email digest |
| ⏱️ Scheduler Agent  | Runs the entire pipeline automatically every week |

This pipeline mimics an intelligent assistant who:
1. Finds relevant research for you.
2. Understands and summarizes it.
3. Sends it to your inbox without being asked.

---

## 💡 Why BriefMind?

Keeping up with research is overwhelming. BriefMind:
- Filters only **useful** content.
- Summarizes using **state-of-the-art LLMs**.
- Frees up **your cognitive bandwidth** for deep work.

Perfect for:
- 🧑‍🔬 Researchers
- 🧑‍💻 Developers
- 📊 Data Scientists
- 🎓 Students
- 📚 Lifelong Learners

---

## 🚀 What Powers It?

### ⚙️ LLM Used — `Gemma-3B-it`

- **Model**: `google/gemma-3b-it`  
- **Type**: Instruction-tuned open-weight LLM from Google  
- **Mode**: Loaded locally using `transformers` with `torch_dtype=torch.bfloat16` and `load_in_8bit=True` for faster inference  
- **Use**: Generates fluent and context-aware summaries of technical articles and papers  
- **Why Gemma?**:  
  - Lightweight (~3B) and fast inference
  - Instruction-tuned for better summarization
  - Fully open-weight and deployable on consumer-grade GPUs

💡 You can also swap in:
- **Mistral** (`mistralai/Mistral-7B-Instruct-v0.2`)
- Any Hugging Face-compatible summarization model

---

## 🔧 Features

- 📥 **Multi-source Research Fetching**  
  Automatically pulls and processes latest content from:
  - **ArXiv** – Computer Science, Machine Learning, and AI domains
  - **HackerNews** – Top tech and programming discussions
  - **OpenAlex** – Academic research metadata and citations
  - **PapersWithCode** – State-of-the-art ML models and benchmarks

- 💾 **Vector Storage & Retrieval**  
  All content is embedded and stored in **ChromaDB** for efficient retrieval and semantic search.

- 🧠 **Summarization Engine**  
  Uses a local or API-based **LLM pipeline** to generate concise summaries with key takeaways.

- 📬 **Email Notification**  
  A formatted digest is sent weekly to your inbox, including:
  - Research Titles
  - Sources & URLs
  - Smart Summaries (bullet points or paragraphs)

- ⏰ **Task Scheduler**  
  Automatically runs every week via a simple scheduler script (`weekly_runner.py`). You can also run it manually or integrate it with a CRON job.



