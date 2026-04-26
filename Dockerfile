# # Stage 1: Build
# FROM python:3.11-slim AS builder
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Stage 2: Runtime
# FROM python:3.11-slim
# WORKDIR /app
# COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
# COPY . .
# RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser
# EXPOSE 5000
# CMD ["python", "app.py"]

# Stage 1: Build
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy pytest and other binaries from builder
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
EXPOSE 5000
CMD ["python", "app.py"]