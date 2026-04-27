# Start from an official Python 3.11 image (slim = smaller size)
FROM python:3.11-slim

# Set the working directory inside the container
# All commands from here on run inside /app
WORKDIR /app

# Copy requirements first (before the rest of the code)
# This is a Docker caching trick — if requirements don't change,
# Docker skips reinstalling them on every rebuild
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of your project into the container
COPY . .

# Tell Docker this container will listen on port 8000
EXPOSE 8000

# The command to run when the container starts
# Note: no --reload in production, and host 0.0.0.0 makes it
# reachable from outside the container
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
