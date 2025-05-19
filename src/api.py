from fastapi import FastAPI, Response

from src.db import connect

app = FastAPI()


@app.get("/healthz")
async def health_check():
    """
    Health check endpoint.
    """
    conn = connect()
    if conn is not None:
        return Response(status_code=200)
    return Response(status_code=503)
