import os
import logging

from sqlalchemy.orm import Session
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate

from model import Thread
from config import llm, embedding_model, config, embeddings
from utils import load_file

class RAG:
    def __init__(self, thread: Thread):
        self.save_local = os.path.join(config.artifact_dir, str(thread.id))
        self.thread = thread
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.vector_store = None

    def load_data(self, db):
        from service.srv_thread import ThreadService
        files = ThreadService.getFiles(self.thread, db)

        if os.path.exists(os.path.join(self.save_local, "index.faiss")):
            self.vector_store = FAISS.load_local(self.save_local, embeddings, allow_dangerous_deserialization=True)
            logging.info(f"Loaded vector store from {self.save_local}")
            return self

        chunks = []
        for file in files:
            docs = load_file(file.path)
            for doc in docs:
                content = doc.page_content
                metadata = doc.metadata
                text_chunks = self.text_splitter.split_text(content)
                for chunk in text_chunks:
                    chunk_doc = Document(
                        page_content=chunk,
                        metadata={"page": metadata.get("page", 1), "source": file.path}
                    )
                    chunks.append(chunk_doc)

        self.vector_store = FAISS.from_documents(chunks, embeddings)
        self.vector_store.save_local(self.save_local)
        
        return self

    
    def retrieve(self, query: str, k: int = 4):
        docs = self.vector_store.similarity_search(query, k=k)
        context = []
        for doc in docs:
            context.append(f"{doc.page_content}\n(Trích trang {doc.metadata.get('page', 'N/A')} từ {doc.metadata.get('source', 'N/A')})\n")
        
        return "\n".join(context)
    
    def invoke(self, query: str):
        docs = self.retrieve(query)
        for chunk in RAG.get_chat_completion_stream(task="rag", params={"context": docs, "question": query}):
            yield chunk

    @staticmethod
    def get_chat_completion_stream(task: str, params: dict):
        prompt, parser = RAG.get_prompt_parser(task)
        chain = prompt | llm | parser

        for chunk in chain.stream(params):
            yield chunk

    @staticmethod
    def get_prompt_parser(task: str):
        if task == "rag":
            from utils.prompts.rag import prompt
            from utils.parsers.rag import parser
        else:
            raise ValueError(f"Unsupported task: {task}")
        
        prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", prompt + """{format_instructions}"""),
            ("human", "{question}"),
        ]
        ).partial(format_instructions=parser.get_format_instructions())

        return prompt_template, parser

