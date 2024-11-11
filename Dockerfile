# Build stage
FROM python:3.10-alpine

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
    lcms2-dev \
    openjpeg-dev \
    tiff-dev

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

# Debug system info
RUN echo "System architecture:" && \
    uname -a && \
    echo "Python architecture:" && \
    python -c "import platform; print(platform.architecture())" && \
    echo "Build machine:" && \
    gcc -dumpmachine

# Build the application
RUN . env/bin/activate && pyinstaller build.spec

# Debug the built executable
RUN echo "Executable details:" && \
    file dist/"Twitch Drops Miner (by DevilXD)" && \
    echo "Executable architecture:" && \
    readelf -h dist/"Twitch Drops Miner (by DevilXD)"
