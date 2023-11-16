# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install Flask and Jinja2 (if not already installed)
RUN pip install Flask Jinja2 Streamlit

# Install Nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Copy files to root of container
COPY app.py /opt/app.py
COPY templates /opt/templates/
COPY static /opt/static

# Expose the necessary port(s)
EXPOSE 8000
EXPOSE 8080

# Start Nginx and your Flask application (replace 'app.py' with your Python file)
CMD service nginx start && python /opt/app.py