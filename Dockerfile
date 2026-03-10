# Use lightweight python image
FROM python:3.10-slim

# Create working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run python script
CMD ["python", "app.py"]
