import os
import sys
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from rich.console import Console
from langchain.chains.conversation.memory import ConversationSummaryMemory


console = Console()

# define a function to get query from user


def get_query_from_user() -> str:
    """
    Get query from user.

    Inputs:
        None

    Returns:
        query (str): The query.
    """
    try:
        query = input()
        return query
    except EOFError:
        print("Error: Try again.")
        return get_query_from_user()

# define a function to load the llm model from openai


def load_llm_model(path_key: str, max_tokens: int = 250):
    """
    Load the LLM model from OpenAI.

    Inputs:
        path_key (str): The path to the OpenAI key.
        max_tokens (int): The maximum number of tokens.

    Returns:
        llm (LanguageModel): The LLM model.
    """
    with open(path_key, "r") as file:
        # Read the contents of the file
        OPENAI_KEY = file.read()
    llm = ChatOpenAI(openai_api_key=OPENAI_KEY,
                     model_name='gpt-3.5-turbo', temperature=0, max_tokens=max_tokens)
    return llm


# define a function to process the query
def process_query_with_memory(llm, retriever, query, memory):
    """
    Process the query.

    Inputs:
        llm (LanguageModel): The LLM model.
        retriever (Retriever): The retriever.
        query (str): The query.
        memory : The memory.

    Returns:
        respuesta (str): The answer.
    """

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory = memory
    )
    respuesta = qa_chain(query)
    console.print(respuesta['answer'], style="bold red")
    return respuesta

# define a function to create a memory object


def memory_object(path_key: str):
    """
    Create a memory object.

    Inputs:
        key_path (str): The path to the OpenAI key.
        max_tokens (int): The maximum number of tokens.

    Returns:
        memory (ConversationSummaryBufferMemory): The memory.
    """
    with open(path_key, "r") as file:
        # Read the contents of the file
        OPENAI_KEY = file.read()
    memory = ConversationSummaryMemory(llm=ChatOpenAI(openai_api_key=OPENAI_KEY, temperature=0, max_tokens=250),
                                       memory_key="chat_history", return_messages=True)
    return memory
