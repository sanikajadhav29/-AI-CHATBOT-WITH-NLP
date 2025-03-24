import spacy
import openai
import wikipediaapi
import random
import os

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define chatbot responses (Intent-Response Pairs)
responses = {
    "greeting": ["Hello! How can I help you?", "Hi there! What can I do for you?"],
    "name": ["I am an AI chatbot, here to assist you."],
    "feeling": ["I'm just a bot, but I'm doing great! How about you?"],
    "help": ["Sure! How can I assist you today?"],
    "bye": ["Goodbye! Have a great day!", "See you later!"]
}

# OpenAI API key (Replace with your own key)
openai.api_key = os.getenv("your own api key")

# Function to determine user intent
def get_intent(user_input):
    doc = nlp(user_input.lower())
    if any(token.lemma_ in ["hi", "hello", "hey"] for token in doc):
        return "greeting"
    elif "name" in user_input:
        return "name"
    elif any(token.lemma_ in ["feel", "doing"] for token in doc):
        return "feeling"
    elif "help" in user_input:
        return "help"
    elif "bye" in user_input:
        return "bye"
    return "openai_search"  # Default to OpenAI if no intent is found

# Function to get response from OpenAI GPT
def get_openai_response(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful AI chatbot."},
                      {"role": "user", "content": query}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error with AI response: {str(e)}"

# Function to fetch answer from Wikipedia
def get_openai_response(query):
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful AI chatbot."},
                      {"role": "user", "content": query}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error with AI response: {str(e)}"


# Chatbot function
def chatbot():
    print("Hello! I am your AI chatbot. Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        intent = get_intent(user_input)
        if intent in responses:
            print("Chatbot:", random.choice(responses[intent]))
        elif intent == "openai_search":
            response = get_openai_response(user_input)
            print("Chatbot:", response if response else get_wikipedia_answer(user_input))
        if intent == "bye":
            break

# Run the chatbot
if __name__ == "__main__":
    chatbot()





