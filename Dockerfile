# Use a specific, lightweight Python base image.
FROM --platform=linux/amd64 python:3.9-slim-buster

# Set the working directory inside the container.
WORKDIR /app

# Copy and install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code.
COPY app/ .

# Set the command to run the script.
CMD ["python", "main.py"]