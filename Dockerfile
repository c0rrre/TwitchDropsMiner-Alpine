# Build stage
FROM python:alpine

# Install build dependencies
RUN apk add --no-cache \
    # Basic build tools
    build-base \
    python3-dev \
    musl-dev \
    linux-headers \
    git \
    # Pillow dependencies
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    # Complete Tkinter dependencies
    tk-dev \
    tcl-dev \
    python3-tkinter \

# Create app directory
WORKDIR /app

# Copy your application files
COPY . .

# Create and activate virtual environment
RUN python3 -m venv env && \
    . env/bin/activate && \
    # Upgrade pip and install wheel
    pip install --upgrade pip && \
    pip install wheel && \
    # Install requirements with optimizations
    pip install --no-cache-dir -r requirements.txt && \
    pip install pyinstaller

# Build the application
RUN . env/bin/activate && pyinstaller build.spec
