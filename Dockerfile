# Build stage
FROM python:3.9-alpine

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
    tiff-dev \
    tk-dev \
    tcl-dev \
    # PyGObject dependencies
    gobject-introspection-dev \
    gtk+3.0-dev \
    # X11 dependencies for pystray
    libx11-dev \
    xorg-server-dev \
    # Additional dependencies
    cairo-dev \
    glib-dev \
    pango-dev

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
