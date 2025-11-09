# SAYIT — Server

Lightweight FastAPI backend for the SAYIT app. Accepts image uploads (canvas/file) and uses a vision-capable model to extract text (OCR-like). Returns extracted text or an error when no text is detected.

## Features

- POST /uploadCanvasImg-to-text — accept image file and return extracted text
- Basic CORS enabled
- Uses OpenAI-compatible client configured to route to Hugging Face model router (Qwen/Qwen3-VL-8B-Instruct)
- Returns HTTP 400 when no text is detected

## Requirements

- Python 3.12
- Recommended packages:
  - fastapi
  - uvicorn[standard]
  - python-dotenv
  - openai (or the OpenAI client package used in this repo)

Install:

```bash
python -m pip install fastapi uvicorn python-dotenv openai
```

## Environment

Create a `.env` in the project root with:

```
HF_TOKEN=your_hf_api_token_here
```

The server uses HF_TOKEN to call the model router.

## Run (development)

```bash
# from project root
fastapi dev main.py --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- GET /

  - Returns a basic welcome message.

- POST /uploadCanvasImg-to-text
  - Accepts multipart/form-data with a single file field named `file`.
  - Success: 201 Created, JSON { "text": "<extracted text>" }
  - No text detected: 400 Bad Request, detail "No text detected"
  - Server errors: 500

Example (curl):

```bash
curl -X POST "http://localhost:8000/uploadCanvasImg-to-text" \
  -H "Accept: application/json" \
  -F "file=@./example.png"
```

Example (fetch / frontend):

```js
const fd = new FormData();
fd.append("file", selectedFile);
const res = await fetch("http://localhost:8000/uploadCanvasImg-to-text", {
  method: "POST",
  body: fd,
});
if (!res.ok) {
  // handle error (e.g., 400 when no text)
  const err = await res.json();
  console.error(err);
} else {
  const data = await res.json();
  console.log(data.text);
}
```

## Behavior notes

- The server treats model replies that indicate "no text" (e.g., "There is no text content in the image.") as an error (HTTP 400).
- For large images, prefer file upload (multipart/form-data) rather than base64 JSON to avoid large request bodies.
- Adjust CORS origins in `main.py` before production.

## Troubleshooting

- Ensure HF_TOKEN is set and valid.
- If model responses are inconsistent, consider tightening prompts or post-processing checks.
- Check server logs for model request/response debugging.
