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
    pango-dev \
    # Ayatana AppIndicator dependencies
    ayatana-appindicator-dev \
    libayatana-indicator-dev \
    libdbusmenu-gtk3-dev

# Create app directory
WORKDIR /app

# Copy your application files
COPY . .

# Create required directories for Linux build
RUN mkdir -p /app/gi_typelibs && \
# Copy the Ayatana AppIndicator typelib
cp /usr/lib/girepository-1.0/AyatanaAppIndicator3-0.1.typelib /app/gi_typelibs/AppIndicator3-0.1.typelib

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

# Runtime stage
FROM alpine:latest

# Install runtime dependencies
RUN apk add --no-cache \
    # Basic runtime dependencies
    libstdc++ \
    # GTK and X11 runtime dependencies
    gtk+3.0 \
    gobject-introspection \
    libx11 \
    # Image processing runtime dependencies
    jpeg \
    zlib \
    freetype \
    lcms2 \
    openjpeg \
    tiff \
    # Additional runtime dependencies
    cairo \
    glib \
    pango \
    # Runtime Ayatana AppIndicator dependencies
    ayatana-appindicator \
    libayatana-indicator \
    libdbusmenu-gtk3

WORKDIR /app

# Copy the built application
COPY --from=0 /app/dist/* ./

# Set environment variables for GTK
ENV GDK_BACKEND=x11

# Run the application
ENTRYPOINT ["./Twitch Drops Miner (by DevilXD)"]

# Method 2: Alternative using shell form if method 1 doesn't work
# ENTRYPOINT ./\"Twitch Drops Miner \(by DevilXD\)\"

# Method 3: Another alternative using exec form with escaped spaces
# ENTRYPOINT ["./Twitch\ Drops\ Miner\ \(by\ DevilXD\)"]
