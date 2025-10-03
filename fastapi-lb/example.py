from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# List of backend server URLs
servers: List[str] = []

def make_request(request, url, payload):
    try:
        # Forward the request to the chosen server
        func = getattr(request, request.method.lower())
        request_func = partial(
            func,
            url=url,
            headers=request.headers,
            params=request.query_params,
            cookies=request.cookies,
        )

        if payload:
            response = request_func(data=json.dumps(payload))
        else:
            response = request_func()

        status_code = response.status_code
        logger.info(f"status_code: {status_code}")

        if status_code in [200, 201]:
            if response.headers.get("content-type", None) == "application/octet-stream":

                content_dis = response.headers["content-disposition"]
                org_file_names = re.findall("filename=(.+)", content_dis)
                org_file_name = org_file_names[0].strip('"').strip()
                logger.debug(f"org_file_name: {org_file_name}")
                current_dir = Path(__file__).parent
                file_path = f"{current_dir}/files/{org_file_name}"
                logger.debug(f"file_path: {file_path}")    


                org_file_names = re.findall("filename='(.+)", content_dis)
                org_file_name = org_file_names[0].strip('"').strip()
                logger.debug(f"org_file_name: {org_file_name}")

                current_dir = Path(__file__).parent
                file_path = f"{current_dir}/files/{org_file_name}"
                logger.debug(f"file_path: {file_path}")

                return FileResponse(
                    path=file_path,
                    filename=org_file_name,
                    media_type="application/octet-stream",
                )

            return response.json()

        else:
            logger.error(f"response.text: {response.text}")
            raise HTTPException(
                detail={"error_message": response.text}, status_code=status_code
            )
    except Exception:
        logger.error(f"Error in __make_request: {traceback.format_exc()}")
        raise HTTPException(
            detail={"error_message": str(traceback.format_exc())}, status_code=500
        )

@app.api_route("/{path:path}", methods=["POST", "PUT", "GET", "DELETE"])
async def load_balance(request: Request, path: str) -> Any:
    payload = None
    if request.method in ["POST", "PUT"]:
        payload = await request.json()
    # Choose a server randomly (can be modified for other algorithms)
    server = random.choice(servers)
    url = f"{server}/{path}"
    logger.info(f"url: {url}, method: {request.method}")
    logger.info(f"query_params: {request.query_params}")
    return await_make_request(request, url, payload)