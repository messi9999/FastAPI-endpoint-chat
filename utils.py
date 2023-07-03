import requests
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()


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


async def openAI(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=prompt, max_tokens=1000
    )
    generated_text = response.choices[0].text.strip()
    print(generated_text)
    # array = eval(generated_text)

    return generated_text
