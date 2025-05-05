# Deploying to AWS App Runner

This document provides instructions for deploying the Image Analyzer application to AWS App Runner.

## Prerequisites

1. AWS Account with appropriate permissions
2. AWS CLI installed and configured
3. Access to Amazon Bedrock service for Claude 3.5 Sonnet model

## Deployment Options

### Option 1: Using the AWS Console

1. Log in to the AWS Management Console
2. Navigate to AWS App Runner
3. Click "Create service"
4. Choose your source:
   - For source code repository: Connect your GitHub/Bitbucket repository
   - For container image: Build a container image from your source code
5. Configure build:
   - Select "Use a configuration file"
   - App Runner will use the `apprunner.yaml` file in your repository
6. Configure service:
   - Service name: `image-analyzer` (or your preferred name)
   - CPU/Memory: Choose appropriate resources (recommended: 1 vCPU, 2 GB)
7. Configure networking and security:
   - Set up appropriate IAM roles with permissions for Amazon Bedrock
8. Review and create the service

### Option 2: Using the AWS CLI

1. Create an App Runner service with the following command:

```bash
aws apprunner create-service \
  --service-name image-analyzer \
  --source-configuration sourceCodeRepository='{repositoryUrl="YOUR_REPO_URL",codeConfiguration={configurationSource="REPOSITORY",configurationValues={runtime="PYTHON_3",buildCommand="pip install -r requirements.txt",startCommand="uvicorn main:app --host 0.0.0.0 --port 8080",port="8080"}}}' \
  --instance-configuration cpu="1 vCPU",memory="2 GB" \
  --auto-scaling-configuration-arn YOUR_AUTO_SCALING_CONFIG_ARN
```

## Environment Variables

Make sure to configure the following environment variables in your App Runner service:

- `AWS_ACCESS_KEY_ID`: Your AWS access key with Bedrock permissions
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_REGION`: The AWS region where Bedrock is available (e.g., us-east-1)

## IAM Permissions

Ensure your App Runner service has an IAM role with the following permissions:

- `bedrock:InvokeModel` for the Claude 3.5 Sonnet model

## Monitoring and Logs

After deployment, you can monitor your application through:

1. AWS App Runner console
2. CloudWatch Logs
3. CloudWatch Metrics

## Troubleshooting

If you encounter issues with the deployment:

1. Check the App Runner service logs
2. Verify IAM permissions for Bedrock access
3. Ensure environment variables are correctly set
4. Check that the port configuration matches (8080)