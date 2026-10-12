import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(title="45-File Spec Auto-Feed Engine")

# Input schema
class SpecFeedInput(BaseModel):
    file_name: str  # target markdown file name without extension, e.g., "15_DATA_MODEL"
    context_data: Dict[str, Any]  # key‑value mapping for placeholders in the template

# Directories for templates and generated output
TEMPLATE_DIR = "./templates"
OUTPUT_DIR = "./output_specs"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/api/v1/feed-spec")
async def auto_feed_markdown(payload: SpecFeedInput):
    """Receive answer data from a chat UI and inject it into a markdown template.

    The endpoint expects a JSON payload containing the target template name and a
    dictionary of placeholder values. It loads the template from ``templates/``,
    performs ``str.format(**payload.context_data)`` and writes the rendered file
    to ``output_specs/``.
    """
    template_path = os.path.join(TEMPLATE_DIR, f"{payload.file_name}.md")
    if not os.path.exists(template_path):
        raise HTTPException(
            status_code=404,
            detail=f"Template '{payload.file_name}.md' not found in {TEMPLATE_DIR}/"
        )

    try:
        # Load template content
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        # Render using the supplied context data
        filled_content = template_content.format(**payload.context_data)

        # Write rendered markdown to output directory
        output_path = os.path.join(OUTPUT_DIR, f"{payload.file_name}.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(filled_content)

        return {
            "status": "SUCCESS",
            "file_created": payload.file_name,
            "saved_location": output_path,
            "message": "Auto‑feed completed and markdown file generated."
        }
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Missing placeholder data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
