import os
import sys
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.llms import HuggingFaceHub
from langchain_community.embeddings import HuggingFaceEmbeddings


class RAG_module():
    def __init__(self, document_path):
        # change the path to the document folder
        self.document_path = document_path
        documents = []
        for file in os.listdir(self.document_path):
            if file.endswith(".pdf"):
                pdf_path = "./docs/" + file
                loader = PyPDFLoader(pdf_path)
                documents.extend(loader.load())
            elif file.endswith('.docx') or file.endswith('.doc'):
                doc_path = "./docs/" + file
                loader = Docx2txtLoader(doc_path)
                documents.extend(loader.load())
            elif file.endswith('.txt'):
                text_path = "./docs/" + file
                loader = TextLoader(text_path)
                documents.extend(loader.load())
        
        # Split the documents into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ""],
            chunk_size=300,
            chunk_overlap=30,
            length_function=len
        )
        chunks = text_splitter.split_documents(documents)

        openai_embeddings = OpenAIEmbeddings()

        # Convert the document chunks to embedding and save them to the vector store
        self.vectordb = Chroma.from_documents(chunks, embedding=openai_embeddings, persist_directory="./data")
        self.vectordb.persist()
        openai_llm = ChatOpenAI(temperature=0.7, model_name='gpt-4o')
        # create our Q&A chain
        self.pdf_qa = ConversationalRetrievalChain.from_llm(
            openai_llm,
            retriever=self.vectordb.as_retriever(search_kwargs={'k': 3}),
            return_source_documents=True,
            verbose=False
        )

    def add_document(self, document):
        self.vectordb = Chroma.from_documents(document, embedding=self.openai_embeddings, persist_directory="./data")
        self.vectordb.persist()

    def ask_question(self, query):
        result = self.pdf_qa.invoke({"question": query})
        return result["answer"]
