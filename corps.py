from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import fitz 
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
import uvicorn
import csv
import os
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "results": None, "job_description": "", "n_top": 3})

@app.post("/match", response_class=HTMLResponse)
async def match(request: Request, job_description: str = Form(...), n_top: int = Form(3), files: List[UploadFile] = File(...)):
    cv_texts = []
    filenames = []
    
    for file in files:
        data = await file.read()
        if not data:
            continue
            
        doc = fitz.open(stream=data, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        
        if text.strip():
            cv_texts.append(text)
            filenames.append(file.filename)
        doc.close()

    if not cv_texts:
        return templates.TemplateResponse("index.html", {"request": request, "results": [], "job_description": job_description, "n_top": n_top})

    job_embedding = model.encode([job_description])
    cv_embeddings = model.encode(cv_texts)
    similarities = cosine_similarity(job_embedding, cv_embeddings)[0]

    results = []
    for i in range(len(filenames)):
        results.append({"filename": filenames[i], "score": int(similarities[i] * 100)})

    results = sorted(results, key=lambda x: x['score'], reverse=True)[:n_top]

    return templates.TemplateResponse("index.html", {"request": request, "results": results, "job_description": job_description, "n_top": n_top})

@app.post("/feedback")
async def feedback(request: Request):
    data = await request.json()
    rating = data.get('rating')
    comment = data.get('comment')
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    file_exists = os.path.isfile('avis.csv')
    with open('avis.csv', mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Date', 'Note', 'Commentaire'])
        writer.writerow([timestamp, rating, comment])
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)