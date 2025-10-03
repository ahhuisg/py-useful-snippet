from fastapi import FastAPI, Depends

app = FastAPI()

def get_user_by_id(user_id: int):
    return {"user_id": user_id, "username": "user123"}

@app.get("/items/{user_id}/")
async def read_items(user: dict = Depends(get_user_by_id)):
    return {"message": "Hello, " + user["username"] + ", " + str(user["user_id"])}


async def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    # http://localhost:8000/items/?q=test&skip=1&limit=8
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)