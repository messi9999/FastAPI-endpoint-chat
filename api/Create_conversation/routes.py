from fastapi import APIRouter, Request

from utils import get_content, openAI


create_conversation_router = APIRouter()


@create_conversation_router.post("/create_conversation")
async def create_conversation(request: Request):
    # Get request body data
    body = await request.json()
    user_id = body["user_id"]
    url = body["url"]

    # Create conversation_id
    conversation_id = 0

    result = get_content(url)

    if result["status_code"] == 200:
        article_content = result["content"]

        # Create Conversation usting ChatGPT
        prompt = """
[Base Context]
{}
[Goal]
I want to have a conversation with ChatGPT based on above article.
Return only an array of more than 10 questions that the ChatGPT will ask as the result
        """.format(
            article_content
        )
        conversations = openAI(prompt)

        # Save conversations

        # Return conversation id
        conversation_id = 0
        return {"conversation_id": conversations}

    else:
        # Return error
        return {"conversation_id": result["content"]}
