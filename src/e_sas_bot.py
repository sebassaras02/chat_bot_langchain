import numpy as np
import requests
import json
from llm_models import run_chat


#load telegram token
with open('../token_telegram.txt', 'r') as file:
    TOKEN = file.read().strip()

#load the openai key
with open('../openaikey.txt', 'r') as file:
    OPENAI_KEY = file.read().strip()

openai.api_key = OPENAI_KEY

# Función para iniciar un chat
def start(update, context):
    chat_id = update.message.chat_id
    if chat_id not in chat_models:
        chat_models[chat_id] = initialize_chat_model()  # Implementa esta función según tus necesidades
    context.bot.send_message(chat_id=chat_id, text="Chat running. Type 'exit' to quit.")

# define a function to get the message
def get_updates(offset):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()["result"]

# define a function to send a message
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    response = requests.post(url, params=params)
    return response


    
# define main function
def main():
    # load vectorial database
    db = get_vector_db('../data/historia.txt', 'e-sas_company')
    retriever_chroma = db.as_retriever(search_kwargs={'k': 5})
    
    llm = load_llm_model('../openaikey.txt', 300)
    memory = memory_object('../openaikey.txt')
    response = process_query_with_memory(llm, retriever_chroma, query, memory)
    
    print("Starting bot...")
    offset = 0
    while True:
        updates = get_updates(offset)
        if updates:
            for update in updates:
                offset = update["update_id"] +1
                chat_id = update["message"]["chat"]['id']
                user_message = update["message"]["text"]
                print(f"Received message: {user_message}")
                GPT = get_openai_response(user_message)
                send_messages(chat_id, GPT)
        else:
            time.sleep(1)
    
