from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import create_document, get_documents
from schemas import Message, Project, Package, Article

app = FastAPI(title="Flutter Dev Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    message: str

@app.get("/", response_model=HealthResponse)
async def root():
    return {"message": "Backend is running"}

@app.get("/test")
async def test():
    from database import DATABASE_URL, DATABASE_NAME, get_db
    try:
        db = await get_db()
        collections = await db.list_collection_names()
        return {
            "backend": "ok",
            "database": "connected",
            "database_url": DATABASE_URL,
            "database_name": DATABASE_NAME,
            "connection_status": "ok",
            "collections": collections,
        }
    except Exception as e:
        return {"backend": "ok", "database": "error", "error": str(e)}

# Contact messages
@app.post("/contact")
async def submit_contact(message: Message):
    try:
        saved = await create_document("message", message.model_dump())
        return {"status": "success", "data": saved}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Showcase content endpoints (optional for future CMS)
@app.get("/projects", response_model=List[Project])
async def get_projects():
    docs = await get_documents("project")
    # Convert docs to Pydantic-like dicts
    return [
        {
            "title": d.get("title", ""),
            "description": d.get("description"),
            "store": d.get("store"),
            "url": d.get("url"),
            "image": d.get("image"),
            "tags": d.get("tags", []),
        }
        for d in docs
    ]

@app.get("/packages", response_model=List[Package])
async def get_packages():
    docs = await get_documents("package")
    return [
        {
            "name": d.get("name", ""),
            "description": d.get("description"),
            "url": d.get("url"),
        }
        for d in docs
    ]

@app.get("/articles", response_model=List[Article])
async def get_articles():
    docs = await get_documents("article")
    return [
        {
            "title": d.get("title", ""),
            "url": d.get("url", ""),
            "published_at": d.get("published_at"),
        }
        for d in docs
    ]
