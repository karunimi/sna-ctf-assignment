# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy the entire current directory into the container's working directory
COPY . /app

# Install Flask and any other dependencies listed in requirements.txt
RUN pip install -r requirements.txt

# Expose port 4000 to the outside world (assuming your Flask app runs on port 4000)
EXPOSE 4000

# Command to run the application with Flask's built-in server
CMD ["python", "app.py"]

