from pydantic import BaseModel
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Form, Cookie, Depends
from starlette.responses import RedirectResponse, Response
import datetime
import time
import csv
from fastapi import FastAPI, File, UploadFile
import pandas as pd
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/pcu", response_class=HTMLResponse)
def find_pcu(request: Request, fileName:str= Form(...)):
    #initialize the model
    return templates.TemplateResponse("list_fish.html", {"request": request})


@app.post("/")
def upload(request: Request, file: UploadFile = File(...)):
    print(file.filename)
    return templates.TemplateResponse('results.html', context={'request': request})
