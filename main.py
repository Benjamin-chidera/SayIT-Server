import os
import base64
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

import re


app = FastAPI(
    title="SAYIT Server",
    description="Backend server for SAYIT application",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific origins like ["https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

@app.get("/home")
async def read_root():
    return {"message": "Welcome to SAYIT Server. "}

@app.post("/uploadCanvasImg-to-text", status_code=status.HTTP_201_CREATED)
async def upload_canvas_image(file: UploadFile = File(...)):
    try:
        
        print(f"📩 Received file: {file.filename}")
        print(f"📄 Content type: {file.content_type}")
        print(f"📦 Size (bytes): {len(await file.read())}")
        
        await file.seek(0)

        # Read image bytes directly
        image_bytes = await file.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        # Call model for OCR / text extraction
        completion = client.chat.completions.create(
            model="Qwen/Qwen3-VL-8B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract and return only the text content from this image. Do not add any explanation."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
        )

        # Extract model response safely
        # result = completion.choices[0].message.content if completion.choices else "No text detected"

        # return {"text": result}
        if completion.choices and getattr(completion.choices[0].message, "content", None):
            result = completion.choices[0].message.content
            text = str(result).strip()

            # If model responds with a "no text" style message, return an error
            if re.search(r'\b(no text|no text detected|no text found|there is no text|nothing detected|no text content|could not detect)\b', text, re.I):
                raise HTTPException(status_code=400, detail="No text detected")

            print(f"📝 Extracted Text: {text}")
            return {"text": text}
        else:
            raise HTTPException(status_code=400, detail="No text detected")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
        
# fastapi dev main.py --host 0.0.0.0 --port 8000 --reload  