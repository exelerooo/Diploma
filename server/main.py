from fastapi import FastAPI
from pydantic import BaseModel
from multiprocessing import Process, Queue
import uuid
import asyncio
import threading
from fastapi.middleware.cors import CORSMiddleware
import json
import ast

from model_worker import model_process

input_queue = Queue()
output_queue = Queue()
pending_jobs = {}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # или ["*"] для разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PromptRequest(BaseModel):
    prompt: str


@app.post("/generate")
async def generate_text(req: PromptRequest):
    job_id = str(uuid.uuid4())
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    pending_jobs[job_id] = future

    input_queue.put((job_id, req.prompt))

    result = await future

    return json.dumps(ast.literal_eval("{ %s }" % result))


def response_listener(loop):
    while True:
        job_id, result = output_queue.get()
        future = pending_jobs.pop(job_id, None)
        if future:
            loop.call_soon_threadsafe(future.set_result, result)


@app.on_event("startup")
def startup_event():
    loop = asyncio.get_event_loop()

    model_proc = Process(target=model_process, args=(input_queue, output_queue), daemon=True)
    model_proc.start()

    threading.Thread(target=response_listener, args=(loop,), daemon=True).start()
