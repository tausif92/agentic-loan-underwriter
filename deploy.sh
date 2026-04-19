#!/bin/bash

set -e  # stop on error

echo "🚀 Starting deployment..."

# =========================
# CONFIG
# =========================
INSTANCE_NAME="agentic-loan-underwriter"
AMI_ID="ami-0c33c6bd24cee108b"   # Ubuntu 24.04 (ap-south-1) – verify if needed
INSTANCE_TYPE="t2.micro"
KEY_NAME="agentic-key"
SECURITY_GROUP_ID="sg-09059e234352506e9"
SUBNET_ID="subnet-05945a28891a6d228"
REGION="ap-southeast-2"

echo "🔍 Checking for existing EC2 instance..."

EXISTING_INSTANCE_ID=$(aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=$INSTANCE_NAME" \
            "Name=instance-state-name,Values=running,stopped" \
  --query "Reservations[].Instances[].InstanceId" \
  --output text \
  --region $REGION | head -n 1)

if [ -n "$EXISTING_INSTANCE_ID" ]; then
  echo "✅ Found existing instance: $EXISTING_INSTANCE_ID"
  INSTANCE_ID=$EXISTING_INSTANCE_ID
  
  STATE=$(aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query "Reservations[0].Instances[0].State.Name" \
  --output text \
  --region $REGION)

  if [ "$STATE" == "stopped" ]; then
    echo "▶️ Starting stopped instance..."
    aws ec2 start-instances --instance-ids $INSTANCE_ID --region $REGION
  fi
else
  echo "❌ No existing instance found. Creating new one..."

  INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_NAME \
    --security-group-ids $SECURITY_GROUP_ID \
    --subnet-id $SUBNET_ID \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$INSTANCE_NAME}]" \
    --query 'Instances[0].InstanceId' \
    --output text \
    --region $REGION)

  echo "✅ Instance created: $INSTANCE_ID"
fi


# =========================
# WAIT FOR INSTANCE
# =========================
echo "⏳ Waiting for instance to be running..."

aws ec2 wait instance-running \
  --instance-ids $INSTANCE_ID \
  --region $REGION

# =========================
# GET PUBLIC IP
# =========================
echo "🌐 Fetching public IP..."

EC2_HOST=$(aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text \
  --region $REGION)

echo "✅ EC2 Public IP: $EC2_HOST"


# =========================
# CREATE SSH KEY FILE
# =========================
echo "🔑 Setting up SSH key..."

printf "%s" "$EC2_SSH_KEY" > key.pem
chmod 400 key.pem


# =========================
# WAIT FOR SSH
# =========================
echo "🔐 Waiting for SSH to be ready..."

SSH_READY=false
for i in {1..10}; do
  if ssh -o StrictHostKeyChecking=no -i key.pem ubuntu@$EC2_HOST "echo SSH ready" 2>/dev/null; then
    echo "✅ SSH is ready!"
    SSH_READY=true
    break
  fi
  echo "Waiting for SSH..."
  sleep 10
done

if [ "$SSH_READY" = false ]; then
  echo "❌ SSH connection failed"
  exit 1
fi

# =========================
# REMOTE SETUP
# =========================
echo "⚙️ Setting up remote server..."

ssh -o StrictHostKeyChecking=no -i key.pem ubuntu@$EC2_HOST << EOF

set -e

echo "Updating system..."
sudo apt update -y

if ! command -v docker &> /dev/null; then
  sudo apt update -y
  sudo apt install -y docker.io docker-compose git jq
fi


sudo systemctl start docker
sudo systemctl enable docker

sudo usermod -aG docker ubuntu

echo "Cloning repo..."
if [ ! -d "agentic-loan-underwriter" ]; then
  git clone https://github.com/tausif92/agentic-loan-underwriter.git
fi

cd agentic-loan-underwriter
git reset --hard
git pull origin main

echo "Creating .env file..."    

cat <<EOT > backend/.env
OPENAI_API_KEY=$OPENAI_API_KEY
MCP_BASE_URL=http://mcp:8001
CHROMA_DB_DIR=/app/data/chroma
ENV=production
LOG_LEVEL=INFO
LANGSMITH_TRACING=$LANGSMITH_TRACING
LANGSMITH_ENDPOINT=$LANGSMITH_ENDPOINT
LANGSMITH_API_KEY=$LANGSMITH_API_KEY
LANGSMITH_PROJECT=$LANGSMITH_PROJECT
EOT

cat <<EOT > mcp-server/.env
ENV=production
LOG_LEVEL=INFO
EOT

echo "🧹 Cleaning old containers and volumes..."
sudo docker compose down -v --remove-orphans || true

# optional but helpful if things are messy
sudo docker system prune -f || true

echo "Starting containers..."

sudo docker compose up -d --build

echo "✅ Deployment complete!"

EOF

# =========================
# OUTPUT
# =========================
echo "🎉 Application deployed!"
echo "👉 Access: http://$EC2_HOST:8000/docs"
