# Image Analyzer App

A Streamlit application that analyzes images using Amazon Bedrock's Claude 3.5 Sonnet model.

## Features

- Upload an image via the Streamlit interface
- Get AI-powered analysis of image content
- View detailed descriptions of what's in the image

## Requirements

- Python 3.8+
- AWS account with Bedrock access
- Configured AWS CLI profile with appropriate permissions for Claude 3.5 Sonnet model

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Ensure your AWS CLI is configured with a profile that has access to Amazon Bedrock:
   ```
   aws configure
   ```
   Or use a named profile in your ~/.aws/credentials file.

## Running the App

```
streamlit run app.py
```

## How It Works

The application:
1. Accepts image uploads from users
2. Converts the image to base64 format
3. Sends the image to Amazon Bedrock's Claude 3.5 Sonnet model using your configured AWS profile
4. Displays the AI's analysis of the image content

## Note

Ensure your AWS credentials have appropriate permissions for Amazon Bedrock and specifically for the Claude 3.5 Sonnet model.
