FROM        --platform=$TARGETOS/$TARGETARCH ghcr.io/astral-sh/uv:python3.13-bookworm-slim

LABEL       author="eggs@doong.me" maintainer="eggs@doong.me"
LABEL       org.opencontainers.image.description="Installer image for Python UV eggs with all build dependencies"

# Install all tools needed for git cloning and building Python packages
RUN         apt update \
            && apt -y install git curl jq file unzip make gcc g++ libtool ca-certificates dnsutils iproute2 ffmpeg procps tini\
            && apt clean \
            && useradd -m -d /home/container container \
            && rm -rf /var/lib/apt/lists/*

USER        container
ENV         USER=container HOME=/home/container
WORKDIR     /home/container

STOPSIGNAL SIGINT

COPY        --chown=container:container ./../entrypoint.sh /entrypoint.sh
RUN         chmod +x /entrypoint.sh
ENTRYPOINT    ["/usr/bin/tini", "-g", "--"]
CMD         ["/entrypoint.sh"]
