# ============================================================
# Stage 1 — Build React application
# ============================================================

FROM node:22-alpine AS builder

WORKDIR /app

# Install dependencies first for Docker layer caching
COPY package*.json ./

RUN npm ci

# Copy frontend source
COPY . .

# Build-time API configuration
ARG VITE_API_BASE_URL

ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN npm run build


# ============================================================
# Stage 2 — Production web server
# ============================================================

FROM nginx:alpine

# Remove default nginx content
RUN rm -rf /usr/share/nginx/html/*

# Copy production React build
COPY --from=builder /app/dist /usr/share/nginx/html

# Custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
