from fastapi import FastAPI, Request
import requests
import random

app = FastAPI()

# List of backend server URLs
servers = [
    "http://localhost:8001",
    "http://localhost:8002"
]

@app.api_route("/{path:path}", methods=["GET", "POST"])
async def load_balance(request: Request, path: str):

    print("****path: ", path)
    print("****request.method: ", request.method)


    # Choose a server randomly (can be modified for other algorithms)
    server = random.choice(servers)
    print("****server ", server)

    # Forward the request to the chosen server
    if request.method == 'POST':
        payload = await request.json()
        print("****payload ", payload)
        response = requests.post(f"{server}/{path}", json=payload)
    else:  # Handle GET and HEAD requests
        response = requests.get(f"{server}/{path}", params=request.query_params)

    print("****response.status_code ", response.status_code)
    print("****response.json ", response.json())
    print("****response.text ", response.text)


    # Return the response from the server back to the client
    return response.json(), response.status_code

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
