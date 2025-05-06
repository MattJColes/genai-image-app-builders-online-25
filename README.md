
# Image Analyzer App

A FastAPI application that analyzes images using Amazon Bedrock's Nova Pro model.

## Features

- Upload an image via the web interface
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
uvicorn main:app --reload
```

Or run directly:

```
python main.py
```

The application will be available at http://localhost:8000

## How It Works

The application:
1. Accepts image uploads from users
2. Converts the image to base64 format
3. Sends the image to Amazon Bedrock's Claude 3.5 Sonnet model using your configured AWS profile
4. Displays the AI's analysis of the image content

## Project Structure

```
.
├── main.py                # FastAPI application
├── bedrock_helper.py      # Helper functions for Amazon Bedrock
├── requirements.txt       # Project dependencies
├── static/                # Static files (CSS, JS)
│   └── styles.css         # Custom styles
└── templates/             # Jinja2 templates
    ├── base.html          # Base template
    ├── index.html         # Home page
    ├── result.html        # Results page
    └── error.html         # Error page
```

## Note

Ensure your AWS credentials have appropriate permissions for Amazon Bedrock and specifically for the Claude 3.5 Sonnet model.



## Deploying to AWS App Runner

This application is configured for deployment to AWS App Runner. For detailed deployment instructions, see [APPRUNNER_DEPLOYMENT.md](APPRUNNER_DEPLOYMENT.md).

### Quick Deployment Steps

1. Ensure you have AWS CLI configured with appropriate permissions
2. Deploy using either:
   - AWS Console with the provided `apprunner.yaml` configuration
   - AWS CLI using the commands in the deployment guide
3. Configure environment variables for AWS credentials in the App Runner service
4. Ensure the service has IAM permissions to access Amazon Bedrock

