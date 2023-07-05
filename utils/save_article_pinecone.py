import os
import traceback
from dotenv import load_dotenv

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings

import pinecone

load_dotenv()


# Chunk text from article
def chunk_content(text, max_token):
    try:
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=max_token, chunk_overlap=0
        )
        chunks = text_splitter.split_text(text)
        return chunks
    except Exception as e:
        print(traceback.format_exc())
        return []


embeddings = OpenAIEmbeddings()


# Embedd texts of chunks using OpenAI
def embedding_openAI(chunks):
    embeddedData = []
    try:
        print("Embedding using OpenAI...")
        embeddedData = embeddings.embed_documents(chunks)
        if len(embeddedData) == 0:
            return []
        return embeddedData
    except Exception as e:
        print(traceback.format_exc())
        return []


# Config pinecone data
def embedding_config(chunks, embeddedData):
    vector_ids = []
    metadata = []
    for i in range(len(chunks)):
        vector_ids.append("vec" + str(i))
        metadata.append({"content": chunks[i]})

    vectors = list(zip(vector_ids, embeddedData, metadata))
    return vectors


def chunk_list(input_list, chunk_size):
    return [
        input_list[i : i + chunk_size] for i in range(0, len(input_list), chunk_size)
    ]


# Save embedded data to pinecone
def embedding_to_pinecone(vectors, namespace):
    try:
        api_key = os.getenv("PINECONE_API_KEY")
        env_value = os.getenv("PINECONE_ENV_VALUE")
        pinecone.init(api_key=api_key, environment=env_value)
        # Testing the indexs client

        active_indexes = pinecone.list_indexes()
        print("This intex of pinecone is ", active_indexes)
        if len(active_indexes) != 0:
            index = pinecone.Index(active_indexes[0])
            try:
                with index:
                    # Send requests in parallel
                    async_results = [
                        index.upsert(
                            vectors=ids_vectors_chunk,
                            async_req=True,
                            namespace=namespace,
                        )
                        for ids_vectors_chunk in chunk_list(vectors, chunk_size=50)
                    ]
                    # Wait for and retrieve responses (this raises in case of error)
                    [async_result.get() for async_result in async_results]
                print("Successfull inserted embeddings")
            except Exception as e:
                print("Error inserting embeddings:")
                print(traceback.format_exc())
        else:
            print("create index")
            pinecone.create_index("articlechat", dimension=1536)
        return True
    except Exception as e:
        print(traceback.format_exc())
        return False


# Search the best matched chunks with question from pinecone
def searchquery(query, namespace):
    embedding = embedding_openAI(query)
    api_key = "de03dd78-0bb4-46c8-84c4-501ec4585147"
    env_value = "us-west4-gcp-free"
    try:
        pinecone.init(api_key=api_key, environment=env_value)
        active_indexes = pinecone.list_indexes()
        index = pinecone.Index(active_indexes[0])
        query_response = index.query(
            namespace=namespace,
            top_k=8,
            include_values=True,
            include_metadata=True,
            vector=embedding[0],
        )
        return query_response
    except Exception as e:
        print(traceback.format_exc())
        return False


# Limit amount of articles from pinecone
def limit_string_tokens(string, max_tokens):
    tokens = string.split()  # Split the string into tokens
    if len(tokens) <= max_tokens:
        return string  # Return the original string if it has fewer or equal tokens than the limit

    # Join the first 'max_tokens' tokens and add an ellipsis at the end
    limited_string = " ".join(tokens[:max_tokens])
    return limited_string
