from operator import itemgetter

import faiss
from langchain_community.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import numpy as np

from sentence_transformers import SentenceTransformer

import os
from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_openai import OpenAIEmbeddings  # Keeping your database vector embeddings identical
from langchain_community.vectorstores import FAISS, Chroma
#from langchain.chains import create_retrieval_chain
#from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_core.prompts import ChatPromptTemplate

from database import db

#from services.rag_tutor_embed import format_docs

model = SentenceTransformer("all-MiniLM-L6-v2")
dimension = 384
index = faiss.IndexFlatL2(dimension)

documents = []

def add_document(text):
    embedding = model.encode([text])

    index.add(
        np.array(
            embedding,
            dtype="float32"
        )
    )

    documents.append(text)


def search(query):

    query_vector = model.encode([query])

    D, I = index.search(
        np.array(
            query_vector,
            dtype="float32"
        ),
        3
    )

    results = []

    for idx in I:
        if idx < len(documents):
            results.append(documents[idx])

    return results

# 4. Helper function to format retrieved documents into a text block
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
        

def answer_question(question: str, db_path: str = "vector_db") -> str:
    """
    Retrieves relevant documents from a vector store and answers 
    the student's question using Google Gemini.
    """
    try:
        # 1. Initialize Gemini LLM (Automatically looks for GOOGLE_API_KEY env variable)
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

        # 2. Initialize the SAME HuggingFace embedding model used to save the index
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
              
        # Load  previously saved FAISS vector database back into memory from the computer's hard drive
        db = FAISS.load_local("doc_index",embeddings,
                allow_dangerous_deserialization=True)
            
        # Use FAISS database as a retriever engine, to fetch the top 3 most relevant text chunks for a question.
        #retriever = db.as_retriever(search_kwargs={"k":3})
        # Manually retrieve the documents using the string question
        # This isolates the vector search and prevents it from getting mixed up in the chain
        docs = db.similarity_search(question, k=3)

        # 5. Safely format the retrieved chunks into a solid block of text
        retrieved_context = "\n\n".join([doc.page_content for doc in docs])
        
        if not retrieved_context.strip():
            retrieved_context = "No relevant context found in the uploaded documents."
        
        
        # 3. Define the Tutor Persona Prompt
        system_prompt = (
            "You are an encouraging and highly knowledgeable academic tutor. "
            "Use the following pieces of retrieved context to answer the student's question. "
            "If you don't know the answer, say that you don't know.\n\n"
            "Context:\n{context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are an encouraging and highly knowledgeable academic tutor. "
                "Use the following pieces of retrieved context to answer the student's question. "
                "If you don't know the answer, say that you don't know.\n\n"
                "Context:\n{context}"
            )),
            ("human", "{question}"),
        ])


        rag_chain = prompt | llm | StrOutputParser()
        
 
        # 4. Build the RAG Chain
        #question_answer_chain = create_stuff_documents_chain(llm, prompt)
        #rag_chain = create_retrieval_chain(retriever, prompt, llm=llm)
        # 6. Build the Modern LCEL RAG Chain
        # ✅ FIXED: itemgetter("question") extracts just the string from the dict 
        # so the retriever and embedding model don't break.
        # rag_chain = (
        #     {
        #         "context": itemgetter("question") | retriever | format_docs, 
        #         "question": itemgetter("question")
        #     }
        #     | prompt
        #     | llm
        #     | StrOutputParser()
        # )
        
        # 5. Execute and return the answer
        # Execute by passing the exact strings directly
        response = rag_chain.invoke({
            "context": retrieved_context, 
            "question": question
        })
        #response = rag_chain.invoke({"question": question})

        #return response["answer"]
        return response
        
    except Exception as e:
        return f"An error occurred while generating the answer: {str(e)}"


