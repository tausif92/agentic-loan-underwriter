#!/bin/bash

set -e  # stop on error

echo "🚀 Starting deployment..."

# =========================
# CONFIG
# =========================
AMI_ID="ami-0c33c6bd24cee108b"   # Ubuntu 24.04 (ap-south-1) – verify if needed
INSTANCE_TYPE="t2.micro"
KEY_NAME="agentic-key"
SECURITY_GROUP_ID="sg-09059e234352506e9"
SUBNET_ID="subnet-05945a28891a6d228"
REGION="ap-southeast-2"

# =========================
# CREATE EC2 INSTANCE
# =========================
echo "📦 Creating EC2 instance..."

INSTANCE_ID=$(aws ec2 run-instances \
  --image-id $AMI_ID \
  --instance-type $INSTANCE_TYPE \
  --key-name $KEY_NAME \
  --security-group-ids $SECURITY_GROUP_ID \
  --subnet-id $SUBNET_ID \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=agentic-loan-underwriter}]' \
  --query 'Instances[0].InstanceId' \
  --output text \
  --region $REGION)

echo "✅ Instance created: $INSTANCE_ID"

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
# WAIT FOR SSH
# =========================
echo "🔐 Waiting for SSH..."

sleep 30

# =========================
# CREATE SSH KEY FILE
# =========================
echo "🔑 Setting up SSH key..."

echo "$EC2_SSH_KEY" > key.pem
chmod 400 key.pem

# =========================
# REMOTE SETUP
# =========================
echo "⚙️ Setting up remote server..."

ssh -o StrictHostKeyChecking=no -i key.pem ubuntu@$EC2_HOST << EOF

set -e

echo "Updating system..."
sudo apt update -y
sudo apt install -y docker.io docker-compose git awscli jq

sudo systemctl start docker
sudo systemctl enable docker

sudo usermod -aG docker ubuntu

echo "Cloning repo..."
git clone https://github.com/tausif92/agentic-loan-underwriter.git
cd agentic-loan-underwriter

echo "Creating .env file..."    

cat <<EOT > .env
OPENAI_API_KEY=$OPENAI_API_KEY
MCP_BASE_URL=http://mcp:8001
CHROMA_DB_DIR=/app/data/chroma
ENV=production
LOG_LEVEL=INFO
EOT

echo "Starting containers..."
docker-compose up -d

echo "✅ Deployment complete!"

EOF

# =========================
# OUTPUT
# =========================
echo "🎉 Application deployed!"
echo "👉 Access: http://$EC2_HOST:8000/docs"
