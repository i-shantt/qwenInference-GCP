from pathlib import Path

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# Load UI HTML from file (easy to edit without touching main.py).
UI_HTML = (Path(__file__).parent / "templates" / "ui.html").read_text(encoding="utf-8")


model_name = "Qwen/Qwen3-4B-Instruct-2507"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto",
)

app = FastAPI(title="Qwen Inference", description="Simple inference API for Qwen.")


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="User prompt for generation.")


@app.get("/")
def root():
    """Health check for Cloud Run and load balancers."""
    return {"status": "ok", "service": "qwen-inference"}


@app.get("/health")
def health():
    """Liveness/readiness probe."""
    return {"status": "healthy"}


@app.get("/ui", response_class=HTMLResponse)
def ui():
    return UI_HTML


@app.post("/generate")
async def generate(body: GenerateRequest):
    message = [{"role": "user", "content": body.prompt}]

    text = tokenizer.apply_chat_template(
        message,
        tokenize=False,
        add_generation_prompt=True,
    )

    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    generated_info = model.generate(**model_inputs, max_new_tokens=100)

    output_ids = generated_info[0][len(model_inputs.input_ids[0]):].tolist()
    final_output = tokenizer.decode(output_ids, skip_special_tokens=True)

    return {"output": final_output}