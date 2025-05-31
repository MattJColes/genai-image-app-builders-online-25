#!/bin/bash
set -e

# Configuration - replace these values with your own
AWS_REGION="ap-southeast-2"
AWS_ACCOUNT_ID="669417502288"
ECR_REPOSITORY_NAME="bedrock-playground-summit"
VPC_ID="vpc-0d99760127a7a9ed1"
SUBNET_IDS="subnet-049063db4c49dfaf1,subnet-0654f02f56dd7bebd"
STACK_NAME="bedrock-playground-summit"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install it first."
    exit 1
fi

echo "=== Logging in to Amazon ECR ==="
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

echo "=== Checking if ECR repository exists ==="
if ! aws ecr describe-repositories --repository-names ${ECR_REPOSITORY_NAME} --region ${AWS_REGION} &> /dev/null; then
    echo "Creating ECR repository ${ECR_REPOSITORY_NAME}"
    aws ecr create-repository --repository-name ${ECR_REPOSITORY_NAME} --region ${AWS_REGION}
else
    echo "ECR repository ${ECR_REPOSITORY_NAME} already exists, skipping creation"
fi

echo "=== Building Docker image for linux/amd64 platform ==="
docker buildx build --platform linux/amd64 -t ${ECR_REPOSITORY_NAME} .

echo "=== Tagging Docker image ==="
docker tag ${ECR_REPOSITORY_NAME}:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:latest

echo "=== Pushing Docker image to ECR ==="
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:latest

echo "=== Updating task definition ==="
sed -i.bak "s/ACCOUNT_ID/${AWS_ACCOUNT_ID}/g" task-definition.json
sed -i.bak "s/REGION/${AWS_REGION}/g" task-definition.json

echo "=== Deploying CloudFormation stack ==="
aws cloudformation deploy \
  --template-file ecs-service.yaml \
  --stack-name ${STACK_NAME} \
  --parameter-overrides \
    VpcId=${VPC_ID} \
    SubnetIds=${SUBNET_IDS} \
    ECRImageURI=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY_NAME}:latest \
  --capabilities CAPABILITY_IAM

echo "=== Getting application URL ==="
SERVICE_URL=$(aws cloudformation describe-stacks \
  --stack-name ${STACK_NAME} \
  --query "Stacks[0].Outputs[?OutputKey=='ServiceURL'].OutputValue" \
  --output text)

echo "=== Deployment complete ==="
echo "Your Bedrock Playground is now available at: ${SERVICE_URL}"
