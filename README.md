# 🧠 MediGuru AI

MediGuru is an AI-powered medical assistant built using **RAG (Retrieval Augmented Generation)**.

It allows users to:

- Ask medical questions
- Analyze medical reports (PDF)
- Perform symptom triage
- Search medical knowledge

---

## 🚀 Features

- Hybrid RAG (FAISS + BM25 retrieval)
- Web search augmentation (Tavily)
- Gemini LLM reasoning
- Conversational memory
- PDF medical report analyzer
- Source citations
- Streamlit UI

---

## 🏗 Architecture

```
User Question
      ↓
Hybrid Retrieval (FAISS + BM25)
      ↓
Medical Documents
      ↓
Web Search
      ↓
Gemini LLM
      ↓
Structured Medical Answer
```

---

## 📂 Project Structure

```
src/
 ├── app.py
 ├── rag_engine.py
 ├── vector_store.py
 └── document_processor.py
```

---

## ⚙️ Installation

Clone repository

```
git clone https://https://github.com/Deepak4053/Mediguru_AI.git
cd mediguru-ai
```

Install dependencies

```
pip install -r requirements.txt
```

Add environment variables

```
GOOGLE_API_KEY=your_key
TAVILY_API_KEY=your_key
```

Run the app

```
streamlit run src/app.py
```

---

## ⚠ Disclaimer

This project provides **educational medical information only** and is not a substitute for professional medical advice.

---

## 📌 Tech Stack

- Python
- Streamlit
- LangChain
- FAISS
- Gemini LLM
- Tavily Search