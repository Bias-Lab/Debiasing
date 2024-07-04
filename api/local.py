import requests

def generate_response_local(model: str, query: str) -> str:
    url = "http://localhost:11434/api/chat"
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ],
        "stream": False,
    }

    response = requests.post(url, json=data)
    return response.json()['message']['content']


def generate_review_local(model: str, query: str) -> str:
    url = "http://localhost:11434/api/chat"
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ],
        "stream": False,
        "temperature": 0.25,
        "max_tokens": 10,
    }

    response = requests.post(url, json=data)
    return response.json()['message']['content']
