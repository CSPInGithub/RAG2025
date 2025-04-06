from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import StreamingResponse, JSONResponse
import os
import json
import asyncio

from pipeline import run_pipeline_from_file  # Your processing pipeline

app = FastAPI()


@app.get("/mcp.json")
async def mcp_metadata():
    return JSONResponse(
        {
            "name": "Test Automation Agent",
            "description": "Generate tests from requirements!",
            "version": "1.0.0",
            "mcp_endpoint": "http://localhost:8000/mcp",
            "supports_streaming": True,
            # "supports_file_input": True,
            "icon": "🧪",
        }
    )


@app.post("/mcp")
async def handle_mcp_file(request: Request):
    # os.makedirs("./uploads", exist_ok=True)
    # file_path = f"./uploads/{file.filename}"

    # with open(file_path, "wb") as f:
    #     f.write(await file.read())

    # Run your pipeline (returns dict with summary, requirements, gherkin, selenium_code)usr
    payload = await request.json()
    user_input = payload.get("input", "")

    print(f"📥 Got MCP input: {user_input}")

    uploads_dir = "./uploads"
    os.makedirs(uploads_dir, exist_ok=True)

    result = run_pipeline_from_file(user_input, file_path=uploads_dir)

    # Format each SSE message
    def format_sse(data: dict):
        return f"data: {json.dumps(data)}\n\n"

    async def stream_response():
        # Pre-message (for instant feedback in Cursor)
        yield format_sse(
            {
                "type": "text",
                "content": "🛠️ Processing your file and generating output...",
            }
        )

        await asyncio.sleep(1)  # Optional delay for UX

        # Final output message
        yield format_sse(
            {
                "type": "text",
                "content": result.get("summary", "⚠️ No summary generated."),
            }
        )

    # Important: Return with correct media type
    return StreamingResponse(stream_response(), media_type="text/event-stream")
