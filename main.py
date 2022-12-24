from fastapi import FastAPI
from app.routes.routes import router as appRoutes
from fastapi.middleware.cors import CORSMiddleware
from app.server.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000"
]

"""app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)"""

@app.get('/')
def root():
    return "Welcome to the devHandle back-end"

app.include_router(appRoutes,prefix='/api')
