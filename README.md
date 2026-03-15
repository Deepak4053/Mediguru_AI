# 🧠 MediGuru AI

**MediGuru AI** is an intelligent medical knowledge assistant built using **Retrieval Augmented Generation (RAG)**.

It combines **medical document retrieval, web search, and large language models** to provide reliable medical information.

🌐 **Live Demo:**
https://mediguruaibydeepak.streamlit.app

---
# 🚀 Features
* 💬 Medical Question Answering
* 📄 Medical Report Analyzer (PDF)
* 🔎 Hybrid Retrieval (**FAISS + BM25**)
* 🌐 Web Search Integration (**Tavily**)
* 🧠 LLM Reasoning (**Google Gemini**)
* 💾 Conversational Memory
* 📚 Source Citations
* ⚡ Interactive **Streamlit UI**

---

# 🏗 Architecture

```
User Question
      │
      ▼
Hybrid Retrieval
(FAISS + BM25)
      │
      ▼
Medical Knowledge Base
      │
      ▼
Web Search (Tavily)
      │
      ▼
Gemini LLM Reasoning
      │
      ▼
Structured Medical Response
```

---

# 📂 Project Structure

```
Mediguru_AI
│
├── src
│   ├── app.py                # Streamlit interface
│   ├── rag_engine.py        # RAG pipeline
│
├── vector_db                # FAISS vector database
│
├── requirements.txt
├── README.md
```
---
# ⚙️ Installation
### Clone the repository
```
git clone https://github.com/Deepak4053/Mediguru_AI.git
cd Mediguru_AI
```
### Install dependencies

```
pip install -r requirements.txt
```

### Add environment variables

Create a `.env` file:

```
GOOGLE_API_KEY=your_key
TAVILY_API_KEY=your_key
```

### Run the app

```
streamlit run src/app.py
```

---

# 📊 Tech Stack

* **Python**
* **Streamlit**
* **LangChain**
* **FAISS Vector Database**
* **Google Gemini LLM**
* **Tavily Web Search**
* **Sentence Transformers**

---

# ⚠ Disclaimer

This project provides **educational medical information only** and **does not diagnose or prescribe treatments**.

Always consult a qualified healthcare professional for medical advice.
---

# 👨‍💻 Author
**Deepak Kumar Gaund**

AI / ML Enthusiast | Electronics & Communication Engineering Student
GitHub:
https://github.com/Deepak4053
