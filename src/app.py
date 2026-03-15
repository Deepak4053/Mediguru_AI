import streamlit as st
import tempfile
import os
import json
import time
from langchain_community.document_loaders import PyPDFLoader
from rag_engine import medical_rag, analyze_medical_report

# PAGE CONFIG
st.set_page_config(
    page_title="MediGuru AI",
    page_icon="👨‍⚕️",
    layout="wide"
)
# CUSTOM CSS (Mobile Friendly)
st.markdown("""
<style>

.block-container {
    max-width: 900px;
    padding-top: 1rem;
}

h1 {
    text-align:center;
}

.stChatMessage {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# SESSION STATE

if "chats" not in st.session_state:
    st.session_state.chats = {"New Chat": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

if "disclaimer" not in st.session_state:
    st.session_state.disclaimer = False


messages = st.session_state.chats[st.session_state.current_chat]

# FORMAT CHAT HISTORY FOR RAG

def get_chat_history():
    history = []
    for i in range(0, len(messages)-1, 2):
        if messages[i]["role"] == "user":

            history.append(
                (messages[i]["content"], messages[i+1]["content"])
            )

    return history

# SIDEBAR
with st.sidebar:
    st.title("👨‍⚕️ MediGuru")
    st.warning("⚕️ Informational only. Not medical advice.")

    st.session_state.disclaimer = st.checkbox(
        "I accept the disclaimer",
        value=st.session_state.disclaimer
    )

    st.divider()
    st.subheader("💬 Conversations")
    for chat in st.session_state.chats:
        if st.button(chat):

            st.session_state.current_chat = chat
            st.rerun()

    if st.button("➕ New Conversation"):

        name = f"Chat {len(st.session_state.chats)+1}"

        st.session_state.chats[name] = []
        st.session_state.current_chat = name

        st.rerun()

    st.divider()

    show_sources = st.toggle("Show Sources", value=True)

    if messages:

        st.download_button(
            "💾 Export Chat",
            json.dumps(messages, indent=2),
            "mediguru_chat.json"
        )

# DISCLAIMER SCREEN
if not st.session_state.disclaimer:
    st.markdown("""
    <div style="text-align:center;padding:100px">
    <h2>⚕️ Medical Disclaimer</h2>
    <p>This AI provides informational medical guidance.</p>
    <p>It is NOT a substitute for professional medical advice.</p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()
# HEADER

st.title("👨‍⚕️ MediGuru AI")
st.caption("Ask medical questions and analyze medical reports.")

# TABS

chat_tab, report_tab = st.tabs(
    ["💬 Medical Chat", "📄 Report Analyzer"]
)
# CHAT TAB
with chat_tab:
    for msg in messages:
        avatar = "👨‍⚕️" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask a medical question...")
    if prompt:
        messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):

            st.markdown(prompt)
        with st.chat_message("assistant", avatar="👨‍⚕️"):
            with st.spinner("Consulting medical knowledge..."):
                history = get_chat_history()
                response, sources = medical_rag(prompt, history)
                placeholder = st.empty()
                streamed = ""
                for line in response.split("\n"):
                    streamed += line + "\n"

                    placeholder.markdown(streamed)

                    time.sleep(0.03)

                if show_sources and sources:

                    st.markdown("---")
                    st.markdown("### 📚 Sources")

                    for s in sources:

                        st.markdown(f"- {s}")

        messages.append({"role": "assistant", "content": response})

# REPORT ANALYZER TAB
with report_tab:

    st.subheader("📄 Upload Medical Report")
    uploaded_file = st.file_uploader(
        "Upload medical report (PDF)",
        type=["pdf"]
    )
    if uploaded_file:
        col1, col2 = st.columns([1,1])
        with col1:
            st.success("PDF Uploaded")

        with col2:
            analyze = st.button("Analyze Report")
        if analyze:

            with st.spinner("Reading report..."):
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as tmp:

                    tmp.write(uploaded_file.getvalue())
                    loader = PyPDFLoader(tmp.name)

                    docs = loader.load()
                    report_text = "\n".join(
                        [d.page_content for d in docs]
                    )
                    result = analyze_medical_report(
                        report_text
                    )
                st.markdown(result)
                os.unlink(tmp.name)