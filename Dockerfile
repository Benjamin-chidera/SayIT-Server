FROM python:3.12-slim   

# Install system dependencies required for onnxruntime
RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Install uv
RUN pip install uv

# 4️⃣ Copy requirements file
COPY requirements.txt .

# 5️⃣ Install dependencies
RUN uv pip install --system --no-cache-dir -r requirements.txt

# 6️⃣ Copy application code
COPY . .

# Secrets are passed at build time via --secret flag, not ARG
RUN --mount=type=secret,id=openai_api_key \
    --mount=type=secret,id=hf_token \
    OPENAI_API_KEY=$(cat /run/secrets/openai_api_key) \
    HF_TOKEN=$(cat /run/secrets/hf_token) \
    echo "OpenAI API Key and HF Token set."  

# 7️⃣ Expose the port
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]