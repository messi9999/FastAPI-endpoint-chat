import os, requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import openai
import tiktoken

from langchain.chat_models.openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI


load_dotenv()


# Function to scrap content from article website using URL
async def get_content(url):
    # Make a GET request to the article URL
    response = requests.get(url)
    if response.status_code == 200:
        # Extract the content from the response using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Example: Extract the article content using specific HTML tags or class names
        title = soup.find("title").get_text()
        article_content = ""
        paragraphs = soup.find_all("p")
        for paragraph in paragraphs:
            article_content = article_content + paragraph.get_text() + "\n"
        return {
            "status_code": response.status_code,
            "content": article_content,
            "title": title,
        }
    else:
        return {
            "status_code": response.status_code,
            "content": "Failed to retrieve article content",
        }


# Function to get number of tokens
def get_num_tokens(text):
    # Load the encoding for the GPT-3 Davinci model
    encoding = tiktoken.encoding_for_model("davinci")

    # Tokenize the text
    tokens = encoding.encode(text)
    return len(tokens)


async def openAI(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=prompt, max_tokens=1000
    )
    generated_text = response.choices[0].text.strip()
    # array = eval(generated_text)

    return generated_text


# Chat with ChatGPT
async def ChatGPT(context, chat_history, question):
    chat = ChatOpenAI(
        temperature=0.1,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        streaming=True,
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """You are an English teacher. Your name is Erika. You are talking to a student who is learning English. Don't say As an AI language model, I don't have a personal name.

Use the following pieces of news article context to ask and answer the users question and chat history.

Please answer user's question as a teacher or answer with some reaction in very short sentence and always ask a question about the following context at the end of what you say and let the student answer it.

If the user asks you a question or comments related to the context, please answer it with reaction in simple way and ask a question about the following context at the end of what you say and let the student answer it.

Please don't answer and reply with more than 4 sentences. Keep it short and simple.

Don't talk too much
----------------
{context}
        
----------------
{chat_history}
        
"""
            ),
            HumanMessagePromptTemplate.from_template("{question}"),
        ]
    )

    answer = chat(
        prompt.format_prompt(
            context=context,
            chat_history=chat_history,
            question=question,
        ).to_messages()
    )
    return answer.content
