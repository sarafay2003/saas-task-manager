# Start from official Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies first (faster rebuilds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]