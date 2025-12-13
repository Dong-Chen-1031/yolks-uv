#!/bin/bash
# Python App Installation Script
#
# Server Files: /mnt/server

mkdir -p /mnt/server
cd /mnt/server

if [ "${USER_UPLOAD}" == "true" ] || [ "${USER_UPLOAD}" == "1" ]; then
    echo -e "assuming user knows what they are doing have a good day."
    exit 0
fi

## add git ending if it's not on the address
if [[ ${GIT_ADDRESS} != *.git ]]; then
    GIT_ADDRESS=${GIT_ADDRESS}.git
fi

if [ -z "${USERNAME}" ] && [ -z "${ACCESS_TOKEN}" ]; then
    echo -e "using anon api call"
else
    GIT_ADDRESS="https://${USERNAME}:${ACCESS_TOKEN}@$(echo -e ${GIT_ADDRESS} | cut -d/ -f3-)"
fi

## pull git python repo
if [ "$(ls -A /mnt/server)" ]; then
    echo -e "/mnt/server directory is not empty."
    if [ -d .git ]; then
        echo -e ".git directory exists"
        if [ -f .git/config ]; then
            echo -e "loading info from git config"
            ORIGIN=$(git config --get remote.origin.url)
        else
            echo -e "files found with no git config"
            echo -e "closing out without touching things to not break anything"
            exit 10
        fi
    fi

    if [ "${ORIGIN}" == "${GIT_ADDRESS}" ]; then
        echo "pulling latest from github"
        git pull
    fi
else
    echo -e "/mnt/server is empty.\ncloning files into repo"
    if [ -z ${BRANCH} ]; then
        echo -e "cloning default branch"
        git clone ${GIT_ADDRESS} .
    else
        echo -e "cloning ${BRANCH}'"
        git clone --single-branch --branch ${BRANCH} ${GIT_ADDRESS} .
    fi

fi

export HOME=/mnt/server

DEPENDENCY_INSTALL_MODE="${DEPENDENCY_INSTALL_MODE:-pip}"

echo "Installing Python dependencies (mode: ${DEPENDENCY_INSTALL_MODE})"

if [ "${DEPENDENCY_INSTALL_MODE}" = "pip" ]; then
    if [ -n "${PY_PACKAGES}" ]; then
        uv pip install -U --prefix .local ${PY_PACKAGES}
    fi

    if [ -f "/mnt/server/${REQUIREMENTS_FILE}" ]; then
        uv pip install -U --prefix .local -r "${REQUIREMENTS_FILE}"
    fi

elif [ "${DEPENDENCY_INSTALL_MODE}" = "uv" ]; then
    if [ ! -f "/mnt/server/pyproject.toml" ]; then
        echo "No pyproject.toml found; skipping 'uv sync' (no project dependencies to install)."
    else
        # Avoid creating a per-project .venv; store the project environment elsewhere.
        export UV_PROJECT_ENVIRONMENT="/mnt/server/.local/uv"
        uv sync
    fi

else
    echo "ERROR: Unknown DEPENDENCY_INSTALL_MODE='${DEPENDENCY_INSTALL_MODE}' (expected: pip or uv)"
    exit 12
fi

echo -e "install complete"
exit 0