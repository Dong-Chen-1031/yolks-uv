FROM        --platform=$TARGETOS/$TARGETARCH ghcr.io/astral-sh/uv:python3.12-bookworm-slim

LABEL       author="eggs@doong.me" maintainer="eggs@doong.me"
LABEL       org.opencontainers.image.description="Installer image for Python UV eggs with all build dependencies"

# Install all tools needed for git cloning and building Python packages
RUN         apt update \
            && apt -y install git curl jq file unzip make gcc g++ libtool \
            && apt clean \
            && rm -rf /var/lib/apt/lists/*

# Set working directory for installation
WORKDIR     /mnt/server