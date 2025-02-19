# Use an official lightweight Python image
FROM python:3.10-slim

# Set environment variables to avoid buffering
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Debugging: Show Python version and installed packages
RUN python --version && pip --version

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port (only necessary if you're running a web API)
# EXPOSE 5000  

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "rag_mistral.py"]
