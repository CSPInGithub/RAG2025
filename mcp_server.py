# Example in FastAPI
from fastapi import FastAPI

app = FastAPI()

@app.get("/mcp")
def read_mcp():
    return {"message": "MCP GET request handled"}

from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
import os
import json
import asyncio

from pipeline import run_pipeline_from_file  # Your processing pipeline



@app.post("/mcp")
async def handle_mcp_file(file: UploadFile):
    # Ensure uploads directory exists
    os.makedirs("./uploads", exist_ok=True)

    # Save uploaded file to disk
    file_path = f"./uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Run your document-to-selenium pipeline
    result = run_pipeline_from_file(file_path)

    # Format data for SSE streaming
    def format_sse(data):
        return f"data: {json.dumps(data)}\n\n"

    # Stream the response in chunks (Cursor expects this)
    async def stream_response():
        # Optional pre-message (shows instant response in Cursor)
        yield format_sse({
            "type": "text",
            "content": "🤖 Analyzing your document and generating test cases..."
        })

        await asyncio.sleep(1)  # Simulate delay if needed

        # Final response (main output)
        yield format_sse({
            "type": "text",
            "content": result.get("selenium_code", "No Selenium code generated."),
            "metadata": {
                "summary": result.get("summary", ""),
                "requirements": result.get("requirements", ""),
                "gherkin": result.get("gherkin", "")
            }
        })

    return StreamingResponse(stream_response(), media_type="text/event-stream")
