import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)


completion = client.chat.completions.create(
    model="Qwen/Qwen3-VL-8B-Instruct",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "return only the text from this image."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://swharden.com/csdv/skiasharp/text/measure.png"
                    }
                }
            ]
        }
    ],
)

print(completion.choices[0].message.content)