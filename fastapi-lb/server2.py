from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import HTTPException

app = FastAPI()


@app.get("/hello")
async def root():
    return {"message": "Hello World from 8002"}


@app.get("/ex")
async def execept():
    return HTTPException(detail={"error_message": "table not found"}, status_code=501)


@app.post("/test")
async def test():
    return JSONResponse(
        status_code=422,
        content={"detail": "this is a test error"},
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)