# Start from a small official Python image. "slim" = smaller, fewer extras.
FROM python:3.12-slim

# Where our app lives inside the container.
WORKDIR /app

# Install dependencies first, on their own layer.
# Docker caches this step, so code changes don't re-trigger a full reinstall.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the application code.
COPY app/ ./app/

# Document the port the app listens on (informational).
EXPOSE 9595

# Start the server. host 0.0.0.0 = listen on all interfaces so the port can be
# reached from outside the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9595"]
