from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

app = FastAPI(title="13 Layers API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# DEMO data: not real stock
PRODUCTS = [
    {"id": 1, "name": "Laptop (demo)", "category": "computers",
     "description": "Example laptop for students", "availability": "demo",
     "price": "On request", "image": "/images/laptop.jpg"},
    {"id": 2, "name": "Raspberry Pi (demo)", "category": "embedded",
     "description": "Single-board computer for IoT projects", "availability": "demo",
     "price": "On request", "image": "/images/raspberry.jpg"},
    {"id": 3, "name": "Arduino Kit (demo)", "category": "embedded",
     "description": "Starter electronics kit", "availability": "demo",
     "price": "On request", "image": "/images/arduino.jpg"},
    {"id": 4, "name": "Drone (demo)", "category": "robotics",
     "description": "Example drone for workshops", "availability": "demo",
     "price": "On request", "image": "/images/drone.jpg"},
]

MESSAGES = []


class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/products")
def list_products(category: str | None = None):
    if category:
        return [p for p in PRODUCTS if p["category"] == category]
    return PRODUCTS


@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/api/contact", status_code=201)
def contact(msg: ContactMessage):
    MESSAGES.append(msg.model_dump())
    return {"status": "received"}