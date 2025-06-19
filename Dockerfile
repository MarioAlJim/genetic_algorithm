# Base image
FROM python:3.12.2

# Prevent log buffering
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy necessary files
COPY requirements.txt ./
COPY .env ./
COPY .coveragerc ./
COPY wsgi.py ./
COPY src/ ./src/

# Install dependencies for wkhtmltopdf
RUN apt-get update && apt-get install -y \
    wget \
    xfonts-base \
    xfonts-75dpi \
    libxrender1 \
    libxext6 \
    libfreetype6 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz -o wkhtmltox.tar.xz \
    && tar -xJf wkhtmltox.tar.xz -C /opt \
    && ln -s /opt/wkhtmltox/bin/wkhtmltopdf /usr/bin/wkhtmltopdf \
    && rm wkhtmltox.tar.xz

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose port (adjust if needed)
EXPOSE 5000

# Command to start the app with Gunicorn
CMD ["gunicorn", "--chdir", "src", "--bind", "0.0.0.0:5000", "wsgi:app"]
#CMD ["gunicorn", "--config", "gunicorn.conf.py", "--chdir", "src", "--bind", "0.0.0.0:5000", "wsgi:app"]
