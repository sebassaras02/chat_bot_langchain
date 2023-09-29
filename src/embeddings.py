from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import os
from rich.console import Console

console = Console()

# CREATE A FUNCTION TO PRODUCE THE VECTOR DB


def get_vector_db(path: str, db_name: str):
    """"
    Create a vector database from a given path.

    Inputs:
        path (str): The path to the text file.
        db_name (str): The name of the vector database.

    Returns:
        vector_db (VectorDB): The vector database.
    """
    # verify if the folder already exists
    if not os.path.isdir(db_name):
        console.print("Vector database is being created.", style="bold green")
        # Create a text loader
        text_loader = TextLoader(path)
        documents = text_loader.load()

        # Create a text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800, chunk_overlap=200, length_function=len)
        splits = text_splitter.split_documents(documents)

        # Create a vector store
        vector_store = Chroma()

        # Create an embedding model
        embedding = SentenceTransformerEmbeddings(
            model_name="allenai/longformer-base-4096")

        # Create a vector database
        vector_store = Chroma.from_documents(
            documents=splits, embedding=embedding, persist_directory=db_name)
        vector_store.persist()
        vector_store = Chroma(persist_directory=db_name,
                              embedding_function=embedding)
        return vector_store

    else:
        console.print("Vector database is being loaded.", style="bold green")
        # Create an embedding model
        embedding = SentenceTransformerEmbeddings(
            model_name="allenai/longformer-base-4096")
        vector_store = Chroma(persist_directory=db_name,
                              embedding_function=embedding)
        return vector_store

