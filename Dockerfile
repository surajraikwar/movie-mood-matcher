# Unified Dockerfile for single container deployment
FROM node:18-slim

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    supervisor \
    nginx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Backend setup
COPY backend/requirements.txt backend/
RUN python3 -m venv /app/backend/venv && \
    /app/backend/venv/bin/pip install --upgrade pip && \
    /app/backend/venv/bin/pip install -r backend/requirements.txt

COPY backend/ backend/
# Remove any accidentally copied env files
RUN find /app/backend -name ".env*" -type f -delete || true

# Frontend setup
COPY frontend/package*.json frontend/
WORKDIR /app/frontend
RUN npm ci

COPY frontend/ .
RUN npm run build

# Nginx configuration
COPY nginx.unified.conf /etc/nginx/nginx.conf

# Supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /app

# Expose port
EXPOSE 80

# Start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
