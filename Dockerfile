# Use the official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Set environment variable for Flask
ENV PORT=8080

# Expose port for Cloud Run
EXPOSE 8080

# Run using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
