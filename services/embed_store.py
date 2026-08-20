
# from sqlalchemy import false, true
# import streamlit as st
# from langchain_community.document_loaders import TextLoader, PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_community.vectorstores import Chroma
# # Use LangChain Expression Language (LCEL) to build a pipeline (chain) that connects the retriever, custom prompt, Gemini LLM,
# # and an output cleaner into a single executable object

# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import StrOutputParser
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# # Create an interactive file upload button
# uploaded_files = st.file_uploader(
#     label="Select files to upload", 
#     accept_multiple_files=true,
# )

# # Process the files to mimic dictionary structure
# uploaded = {}
# if uploaded_files:
#     for file in uploaded_files:
#         # Read the file contents as bytes
#         uploaded[file.name] = file.read()
        
#     st.success(f"Uploaded files: {list(uploaded.keys())}")


# loader = PyPDFLoader(uploaded[list(uploaded.keys())[0]])  # Load the first uploaded file
# documents = loader.load()
# print("Pages Loaded:", len(documents))

# splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=50)
# docs = splitter.split_documents(documents)
# print("Chunks:", len(docs))

# embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# vectorstore = FAISS.from_documents(docs,embedding_model)

# vectorstore.save_local("doc_index")

# # Load  previously saved FAISS vector database back into memory from the computer's hard drive
# db = FAISS.load_local("doc_index",embedding_model,allow_dangerous_deserialization=True)

# # Connects this script to Google’s Gemini AI using the LangChain framework.
# # Temparure of 0 makes the model completely deterministic, ensuring highly factual, consistent, and predictable answers.


# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0)

# # Use FAISS database as a retriever engine, to fetch the top 3 most relevant text chunks for a question.
# retriever = db.as_retriever(search_kwargs={"k":3})

# # Set the prompt template and context to answer a query using RAG


# prompt = PromptTemplate(
#     input_variables=["context","question"],
#     template="""
# You are an expert Copilot.
# Answer ONLY from the document context.

# If information is unavailable,
# reply:
# 'Information not found in document.'

# Context:
# {context}

# Question:
# {question}

# Provide:
# 1. Answer
# 2. Source clause
# 3. Page number
# """
# )

# # 1. Define your system prompt template
# system_prompt = (
#     "Use the given pieces of retrieved context to answer the question. "
#     "If you don't know the answer, say that you don't know.\n\n"
#     "Context:\n{context}"
# )

# prompt = ChatPromptTemplate.from_messages([
#     ("system", system_prompt),
#     ("human", "{input}"),
# ])


# # 3. Helper function to format list of documents into a single text block
# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)

# # 4. Build the RAG chain natively via LCEL
# qa_chain = (
#     {
#         "context": retriever | format_docs,  # Retrieves docs and turns them to text
#         "input": RunnablePassthrough()       # Passes the user question forward
#     }
#     | prompt                                 # Plugs context + question into the prompt
#     | llm                                    # Sends the formatted prompt to your LLM
#     | StrOutputParser()                      # Parses the output directly into a clean string
# )

