FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy your application files into the container
COPY app/ /app/
COPY requirements.txt /app/requirements.txt

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the Flask server
CMD ["python", "main.py"]

