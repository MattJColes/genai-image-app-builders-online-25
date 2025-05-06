import json
import boto3
import os
import base64

def get_image_description(base64_image):
    """
    Get a description of an image using Nova via Amazon Bedrock.
    
    Args:
        base64_image (str): Base64-encoded image string
        
    Returns:
        str: Description of the image
    """
    # Initialize Bedrock client using default credential provider chain
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1"  # You can adjust this default region as needed
    )
    
    # Prepare the prompt for Claude
    prompt = """
    Please analyze this image and provide a detailed description of what you see. Include:
    
    1. Main subjects and objects in the image
    2. Setting or background context
    3. Actions or activities taking place
    4. Notable visual characteristics (colors, style, lighting, etc.)
    5. Any text visible in the image
    
    Be detailed but concise in your analysis.
    """
    
    # Detect image format from base64 string
    image_format = "png"  # Default format
    if base64_image.startswith("/9j/"):
        image_format = "jpeg"
    elif base64_image.startswith("iVBORw0KGgo"):
        image_format = "png"
    elif base64_image.startswith("/9j/4AAQSkZJRg"):
        image_format = "jpg"
    
    # Prepare the request payload for Nova
    request_body = {
        "messages": [
            {
                "role": "user",
                    "content": [
                        {
                            "image": {
                                "format": image_format,
                                "source": {"bytes": base64_image},
                            }
                        },
                        {
                            "text": prompt
                        }
                    ],
                }
            ]
        }
    
    # Make the API call to Bedrock
    response = bedrock_runtime.invoke_model(
        modelId="amazon.nova-pro-v1:0",  # Bedrock Nova model ID
        body=json.dumps(request_body)
    )
    
    # Parse and extract the response
    response_body = json.loads(response.get("body").read())
    description = response_body.get("output").get("message").get("content")[0].get("text")
    
    return description
