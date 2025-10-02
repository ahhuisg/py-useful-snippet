from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI()


@app.get("/hello")
async def root():
    return "this is hello 8001"

@app.get("/ex")
async def execept():
    return HTTPException(detail={"error_message": "table not found"}, status_code=501)

@app.post("/test")
async def test():
    return "this is test 8001"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)