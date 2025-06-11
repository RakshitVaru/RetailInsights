# Python Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files - DASHBOARD
COPY . .

# Install dependencies
RUN pip install --no-cache-dir streamlit pandas requests

# Expose port FastAPI will run on
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "dashboard.py", "--server.address=0.0.0.0"]