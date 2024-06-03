from fastapi import FastAPI, Request, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel

from transformers import T5ForConditionalGeneration, T5Tokenizer

import time
from config import MODEL_NAME

model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(docs_url="/docs", redoc_url=None, lifespan=lifespan)


origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def check_url(request: Request, call_next):
    start_time = int(time.time())
    response = await call_next(request)
    process_time = int(time.time()) - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response


class LibreTranslateTranslateForm(BaseModel):
    q: str
    target: str


@app.post("/libretranslate/translate")
async def translate_text(form_data: LibreTranslateTranslateForm):
    try:
        text = f"<2{form_data.target}> {form_data.q}"
        input_ids = tokenizer(text, return_tensors="pt").input_ids.to(model.device)
        outputs = model.generate(input_ids=input_ids)

        translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(translation)

        return {"translatedText": translation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def get_status():
    return {"status": True}
