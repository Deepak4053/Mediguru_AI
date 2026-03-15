import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents():

    docs = []
    data_folder = "data"
    for file in os.listdir(data_folder):
        if file.endswith(".pdf"):
            path = os.path.join(data_folder, file)
            loader = PyPDFLoader(path)
            docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    split_docs = splitter.split_documents(docs)
    return split_docs