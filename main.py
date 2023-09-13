from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv

# start with: uvicorn --workers 10 --host 0.0.0.0 --port 8000 main:app

app = FastAPI()
load_dotenv()

origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.include_router(api_router)