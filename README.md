# Smart Product Search (Groq + FastAPI)  
**Prepared by:** [Your Name]  
**Email:** [Your Email]  

---

## Overview

This project is an AI-powered e-commerce search application that uses Groq's LLM to filter and recommend the most relevant products from a product catalog based on natural language queries. The goal is to allow users to type a human-friendly search like  
*"running shoes under $100 with good reviews"*  
and receive only the best matches in clean JSON format, displayed through a simple web UI.

---

## How to Run the App

1. **Clone the repository**
   ```bash
   git clone https://github.com/Faiq-Ali10/Hustler-AI-Test
   cd smart-product-search

2. **Create a virtual environment and install dependencies**
    python -m venv venv
    # macOS/Linux
    source venv/bin/activate
    # Windows
    venv\Scripts\activate
    pip install -r requirements.txt

3. **Set up environment variables**
    Create a .env file in the folder:
    GROQ_API_KEY=your_groq_api_key_here

4. **Start the backend server**
    uvicorn main:app --reload

## Open the Frontend

- Open `static/index.html` in your browser,  
  **or** go to `http://127.0.0.1:8000` if using FastAPI’s static file mount.

---

## AI Feature Used

We implemented **LLM-based filtering using Groq**.  
The system sends the full product catalog and the user’s natural language query to Groq’s LLM (`meta-llama/llama-4-scout-17b-16e-instruct`) and asks it to return **only a valid JSON array** of relevant products.

This eliminates the need for embeddings or a vector database, making the setup lightweight and quick to deploy.

---

## Tools & Libraries Used

### Backend
- **FastAPI** — REST API framework  
- **Uvicorn** — ASGI server  
- **requests** — API calls to Groq  
- **python-dotenv** — load environment variables  
- **Starlette StaticFiles** — serve HTML/CSS/JS

### Frontend
- HTML, CSS, JavaScript (Fetch API for async POST requests)

### AI
- **Groq LLM API** — `meta-llama/llama-4-scout-17b-16e-instruct`

---

## Notable Assumptions

1. The product catalog is small enough to send in full with each query.  
2. Groq returns valid JSON (error handling included if not).  
3. The frontend is static with no build pipeline.  
4. CORS is fully open for development purposes — should be restricted in production.  
5. Products are loaded from a static `products.json` file (no database).

---

## License

MIT License — you are free to modify and use for your own projects.
