"""
main.py

Main app module. Contains API initialization and root endpoint only.
"""


from fastapi import FastAPI

from .routers import delivery_fee

app = FastAPI()
app.include_router(delivery_fee.router)


@app.get("/")
async def root():
    """Empty root endpoint."""
    return
