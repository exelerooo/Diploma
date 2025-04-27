from transformers import T5ForConditionalGeneration, T5Tokenizer
from multiprocessing import Queue
import torch


def load_model():
    model_name_default = "google/flan-t5-large"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = T5ForConditionalGeneration.from_pretrained("t5-large")
    tokenizer = T5Tokenizer.from_pretrained(model_name_default)
    model.to(device)
    model.eval()
    return tokenizer, model, device


def generate_text(tokenizer, model, device, original_text):
    prompt = f"Analyse the sentiment of the following text: {original_text}"
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    output = model.generate(**inputs, max_length=100)
    return tokenizer.decode(output[0], skip_special_tokens=True)


def model_process(input_queue: Queue, output_queue: Queue):
    tokenizer, model, device = load_model()
    while True:
        job_id, prompt = input_queue.get()
        try:
            result = generate_text(tokenizer, model, device, prompt)
        except Exception as e:
            result = f"Error: {e}"
        output_queue.put((job_id, result))
