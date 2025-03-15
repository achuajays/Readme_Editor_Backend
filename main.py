from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
import os 

app = FastAPI()

# Define the request body model.
class ReadmeRequest(BaseModel):
    text: str

# Initialize the Groq client.
client = Groq(
  api_key = os.getenv("GROQ_API_KEY")
)

@app.post("/generate-readme")
async def generate_readme(request: ReadmeRequest):
    # Define chat messages, including a system message to set context
    # and a user message that includes the provided text.
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that generates Markdown code."
        },
        {
            "role": "user",
            "content": request.text,
        }
    ]

    try:
        # Call the Groq API to generate the README.
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        readme_content = chat_completion.choices[0].message.content
        return {"readme": readme_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
