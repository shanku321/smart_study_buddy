
import tempfile
import os
from sqlalchemy import false, true
import streamlit as st
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Chroma
# Use LangChain Expression Language (LCEL) to build a pipeline (chain) that connects the retriever, custom prompt, Gemini LLM,
# and an output cleaner into a single executable object

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

def Upld_embed_store(uploaded_files):
    # # Create an interactive file upload button
    # uploaded_files = st.file_uploader(
    #     label="Select files to upload", 
    #     accept_multiple_files=True
    # )

    # Process the files to mimic dictionary structure
    uploaded = {}
    if uploaded_files:
        for file in uploaded_files:
            # Read the file contents as bytes
            #uploaded[file.name] = file.read()            
            
            #st.success(f"Uploaded files: {list(uploaded.keys())}")
            # Create a temporary file on your computer disk
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                # Write the uploaded file bytes into the temporary file
                temp_file.write(file.getbuffer())
                temp_path = temp_file.name  # This gives a real file path string


            #loader = PyPDFLoader(uploaded[list(uploaded.keys())[0]])  # Load the first uploaded file
            loader = PyPDFLoader(temp_path)  # Load the first uploaded file
            pages = loader.load()

            print(f"Pages Loaded: {file.name}, {len(pages)}")

            splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=50)
            docs = splitter.split_documents(pages)
            print("Chunks:", len(docs))

            embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

            vectorstore = FAISS.from_documents(docs,embedding_model)

            vectorstore.save_local("doc_index")
            print(f"Vector store Loaded: {file.name}")

            # Clean up and delete the temporary file after you are done
            if os.path.exists(temp_path):
                os.remove(temp_path)
        st.info("Please upload at least one PDF file to proceed.")



