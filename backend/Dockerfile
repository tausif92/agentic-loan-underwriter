# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y curl && apt-get clean

# Copy only required folders (clean approach)
COPY backend/ ./backend
COPY agents/ ./agents
COPY shared/ ./shared
COPY scripts/ ./scripts

# Install dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose port
EXPOSE 8000

# Start server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
