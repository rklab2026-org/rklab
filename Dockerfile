# 1. Official Python 3.11 lightweight Linux base image
FROM python:3.11-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Prevent Python from writing .pyc files & enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Copy requirements file & install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
COPY . .

# 6. Expose Port 8000 for FastAPI
EXPOSE 8000

# 7. Default command to run FastAPI backend server
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]