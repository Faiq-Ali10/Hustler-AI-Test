import json
import os
import requests
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Load products from JSON file
with open("products.json", "r") as f:
    PRODUCTS = json.load(f)

app = FastAPI(title="E-commerce with Groq AI Search")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (UI)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    """Serve the main HTML UI."""
    return FileResponse("static/index.html")


def groq_filter_products(query: str, products: list):
    """Use Groq LLM to pick the most relevant products for a query."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    product_text = "\n".join([
        f"{p['id']}. {p['name']} - ${p['price']} - {p['category']} - Rating: {p['rating']} - {p['description']}"
        for p in products
    ])

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful e-commerce product recommender. "
                    "Respond ONLY with a valid JSON array of matching products, "
                    "no extra text, no code fences."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Customer query: {query}\n\nHere is the product catalog:\n"
                    f"{product_text}\n\nReturn ONLY a JSON array of the best matching products."
                )
            }
        ],
        "temperature": 0.2
    }

    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    try:
        data = r.json()
    except Exception:
        return {"error": f"Invalid JSON from Groq: {r.text}"}

    if "choices" not in data:
        return {"error": f"Groq API error: {data}"}

    content = data["choices"][0]["message"]["content"].strip()

    # Remove possible code fences
    if content.startswith("```"):
        lines = content.split("\n")
        content = "\n".join(line for line in lines if not line.strip().startswith("```"))

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"error": f"Groq returned non-JSON after cleaning: {content}"}


@app.get("/products")
def get_products():
    """Return the full product catalog."""
    return PRODUCTS


# Pydantic model for POST body
class SearchQuery(BaseModel):
    query: str

@app.post("/search")
def search_products(payload: SearchQuery):
    """Return AI-filtered products for the given query."""
    return groq_filter_products(payload.query, PRODUCTS)
