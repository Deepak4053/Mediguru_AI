import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.vectorstores import FAISS
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.retrievers import BM25Retriever



# EMBEDDINGS
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
# LOAD VECTOR DATABASE
vectorstore = FAISS.load_local(
    "vector_db",
    embeddings,
    allow_dangerous_deserialization=True
)
vector_retriever = vectorstore.as_retriever(search_kwargs={"k":3})

# BM25 RETRIEVER (KEYWORD SEARCH)
docs = list(vectorstore.docstore._dict.values())
bm25_retriever = BM25Retriever.from_documents(docs)
bm25_retriever.k = 3

# LLM (using Gemini model)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)

# WEB SEARCH (here i have used tavily for wev search )
tavily = TavilySearchResults(max_results=3)

# FORMAT CHAT HISTORY
def format_history(chat_history):
    history = ""
    for q, a in chat_history:
        history += f"User: {q}\nAssistant: {a}\n"

    return history

# CONTEXTUALIZE FOLLOW-UP QUESTIONS

def contextualize_question(question, chat_history):
    if not chat_history:
        return question
    if len(question.split()) <= 2:
        last_q, _ = chat_history[-1]
        return f"{question} of {last_q}"

    return question

# HYBRID RETRIEVAL (from database pdf and web search)
def hybrid_retrieve(question):
    vector_docs = vector_retriever.invoke(question)
    keyword_docs = bm25_retriever.invoke(question)
    docs = vector_docs + keyword_docs

    # remove duplicates
    unique_docs = {doc.page_content: doc for doc in docs}.values()
    return list(unique_docs)[:6]

# EXTRACT SOURCES
def extract_sources(docs):
    sources = []
    for d in docs:
        if "source" in d.metadata:
            sources.append(d.metadata["source"])

    return list(set(sources))

# WEB SEARCH
def web_search(question):
    results = tavily.invoke({"query": question})
    web_text = ""
    for r in results:
        web_text += f"{r['title']}:\n{r['content']}\n\n"

    return web_text

# (it is the main rag pipline )
def medical_rag(question, chat_history):

    # contextualize follow-up question
    question = contextualize_question(question, chat_history)
    history = format_history(chat_history)

    # retrieve documents
    docs = hybrid_retrieve(question)
    context = "\n\n".join([d.page_content for d in docs])
    sources = extract_sources(docs)

    # web search
    web_text = web_search(question)

    # reasoning prompt
    prompt = f"""
    You are a medical knowledge assistant.

    Important rules:
    - Provide educational information only.
    - Do NOT diagnose diseases.
    - Do NOT prescribe medications.
    - Always encourage consulting a healthcare professional.
    - Use the provided medical context first before using general knowledge.
    - If the context does not contain enough information, say that clearly.

    Conversation History:
    {history}

    Medical Context (trusted medical documents):
    {context}

    Recent Web Information:
    {web_text}

    User Question:
    {question}

    Follow this reasoning process:

    1. Understand the medical topic.
    2. Use the provided medical context.
    3. Use web information only if needed.
    4. Produce a concise answer.

    Respond in this Markdown format:

    ## 👨‍⚕️ Condition

    ### 🌡 Explanation
    Brief explanation (2–3 sentences).

    ### ⚠ Possible Causes
    - bullet points

    ### 🤒 Symptoms
    - bullet points

    ### 🛡 Prevention / Care
    - bullet points

    ### 🚑 When to See a Doctor
    - bullet points

    ### ⚠ Disclaimer
    This information is not a substitute for professional medical advice.

    Keep the answer clear, concise, and easy to read.
    """


    response = llm.invoke(prompt)
    return response.content, sources

# MEDICAL REPORT ANALYZER(this is the second feature by using this we can analyze reports)

def analyze_medical_report(report_text):
    prompt = f"""
You are a medical report analysis assistant.

Explain the report in simple language.

Medical Report:
{report_text}

Provide:

Key Findings
Abnormal Values
Possible Conditions
When to See a Doctor
"""

    response = llm.invoke(prompt)
    return response.content