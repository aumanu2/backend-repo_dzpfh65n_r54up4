from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Each model corresponds to a MongoDB collection: class name lowercased

class Message(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = Field(None, min_length=7, max_length=20)
    email: EmailStr
    remarks: str = Field(..., min_length=5, max_length=1000)

class Project(BaseModel):
    title: str
    description: Optional[str] = None
    store: Optional[str] = Field(None, description="appstore|playstore|web")
    url: Optional[str] = None
    image: Optional[str] = None
    tags: List[str] = []

class Package(BaseModel):
    name: str
    description: Optional[str] = None
    url: Optional[str] = None

class Article(BaseModel):
    title: str
    url: str
    published_at: Optional[str] = None
