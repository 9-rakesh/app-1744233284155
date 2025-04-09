# Base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome for Selenium
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN wget -q https://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/bin && \
    rm chromedriver_linux64.zip && \
    chmod +x /usr/bin/chromedriver

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY automation/requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# Set entrypoint
ENTRYPOINT ["pytest", "automation/tests", "-v", "--html=report.html", "--self-contained-html"]
