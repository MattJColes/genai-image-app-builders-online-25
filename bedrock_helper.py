import json
import boto3
import os
import base64

def get_image_description(base64_image):
    """
    Get a description of an image using Claude 3.5 Sonnet via Amazon Bedrock.
    
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
    
    # Prepare the request payload for Claude 3.5 Sonnet
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": base64_image
                        }
                    }
                ]
            }
        ]
    }
    
    # Make the API call to Bedrock
    response = bedrock_runtime.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",  # Claude 3.5 Sonnet model ID
        body=json.dumps(request_body)
    )
    
    # Parse and extract the response
    response_body = json.loads(response.get("body").read())
    description = response_body.get("content")[0].get("text")
    
    return description
