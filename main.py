from pydantic import BaseModel
from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Form, Cookie, Depends
from starlette.responses import RedirectResponse, Response
import datetime
import time
import csv
from io import BytesIO
from fastapi import FastAPI, File, UploadFile
import pandas as pd
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def check(request: Request, file: UploadFile = File(...), file2: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    df = pd.read_csv(file2.file)
    return templates.TemplateResponse("index.html", {"request": request,"result":file2.filename})
