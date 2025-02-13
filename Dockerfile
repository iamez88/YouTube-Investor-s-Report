FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /usr/src/app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Install rustup and the latest Rust toolchain
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# Add Cargo and Rust binaries to PATH
ENV PATH="/root/.cargo/bin:${PATH}"
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Remove build dependencies to minimize image size
RUN apt-get purge -y --auto-remove build-essential && \
    rm -rf /var/lib/apt/lists/*
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
