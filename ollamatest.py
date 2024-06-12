import requests

def get_embeddings():
    url = "http://localhost:11434/api/embeddings"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "mxbai-embed-large",
        "prompt": "Llamas are members of the camelid family"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.text)

if __name__ == "__main__":
    get_embeddings()
