from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import io
import base64
from PIL import Image
from bedrock_helper import get_image_description

app = FastAPI(
    title="Image Analyzer",
    description="An application that analyzes images using Amazon Bedrock's Nova model."
)

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main page"""
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "Image Analyzer"}
    )

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_image(request: Request, file: UploadFile = File(...)):
    """Process the uploaded image and get analysis from Amazon Bedrock Nova"""
    try:
        # Read and process the image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert to base64 for Bedrock
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Get image description from Claude 3.5 via Bedrock
        description = get_image_description(img_str)
        
        # Return the template with results
        return templates.TemplateResponse(
            "result.html", 
            {
                "request": request, 
                "title": "Image Analysis Results",
                "description": description,
                "image_data": f"data:image/jpeg;base64,{img_str}"
            }
        )
    except Exception as e:
        error_message = str(e)
        if "AccessDeniedException" in error_message:
            error_message = "Please check your AWS credentials and Bedrock access permissions."
        
        return templates.TemplateResponse(
            "error.html", 
            {
                "request": request, 
                "title": "Error",
                "error": error_message
            }
        )

@app.get("/health", response_class=HTMLResponse)
async def health_check():
    """Health check endpoint for monitoring application status"""
    return HTMLResponse(content="OK", status_code=200)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
