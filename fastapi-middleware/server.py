from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging

class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logging.error(f"Unhandled exception: {exc}")
            return JSONResponse(
                status_code=500,
                content={"detail": str(exc)}
            )

app = FastAPI()
app.add_middleware(ExceptionHandlerMiddleware)

@app.get("/")
async def root():
    raise ValueError("A test error")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
