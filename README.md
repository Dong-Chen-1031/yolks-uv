# Python with UV - Yolks Images & Pterodactyl/Pelican Egg

A complete solution for running Python applications on Pterodactyl/Pelican panels, consisting of:

1. **Docker Images (Yolks)**: Python images with UV package manager pre-installed for blazing-fast dependency management
2. **Pterodactyl/Pelican Egg**: A ready-to-use egg configuration based on [pelican-eggs/generic](https://github.com/pelican-eggs/generic), optimized for Python applications with UV support

This project provides a modern, high-performance Python development environment with automatic dependency management and deployment workflow.

## Quick Start

### Import the Egg Configuration

Choose the egg file based on your panel type:

#### For Pelican Panel (Recommended)
```
https://raw.githubusercontent.com/Dong-Chen-1031/yolks-uv/refs/heads/master/egg/egg-python-uv.json
```

#### For Pterodactyl Panel
```
https://raw.githubusercontent.com/Dong-Chen-1031/yolks-uv/refs/heads/master/egg/egg-pterodactyl-python-uv.json
```

**Import Steps:**
1. In your admin panel, navigate to **Nests** → Select your nest → **Import Egg**
2. Paste the appropriate URL above in the import field
3. Click import and the egg will be automatically configured

**Alternative Downloads:**
- [Pelican: egg-python-uv.json](https://raw.githubusercontent.com/Dong-Chen-1031/yolks-uv/refs/heads/master/egg/egg-python-uv.json)
- [Pterodactyl: egg-pterodactyl-python-uv.json](https://raw.githubusercontent.com/Dong-Chen-1031/yolks-uv/refs/heads/master/egg/egg-pterodactyl-python-uv.json)

### Deploy Your Application

After importing the egg:
1. Create a new server using the "Python with UV" egg
2. Select your desired Python version from the Docker images dropdown
3. Configure your application:
   - **Git Repo Address**: Your repository URL
   - **App py file**: Your main Python file (default: `app.py`)
   - **Requirements file**: Your requirements file (default: `requirements.txt`)
4. Start your server and the application will automatically deploy

## Components

### 1. Docker Images (Yolks)
Pre-built Python images with UV package manager, hosted on GitHub Container Registry. These images serve as the runtime environment for your Python applications.

### 2. Pterodactyl/Pelican Egg
A complete egg configuration file (`egg/egg-python-uv.json`) based on [pelican-eggs/generic](https://github.com/pelican-eggs/generic), customized to:
- Use UV for package management instead of traditional pip
- Support git-based deployments
- Enable automatic updates
- Provide flexible configuration options

## Features

- **UV Package Manager**: Lightning-fast Python package installer and resolver, written in Rust
- **Multi-Version Support**: Python versions from 3.8 to 3.14
- **Multi-Architecture**: Available for both `linux/amd64` and `linux/arm64`
- **Auto-Updates**: Built-in support for git repository auto-updates
- **Requirements Management**: Automatic installation from requirements.txt
- **Optimized for Pterodactyl/Pelican**: Ready-to-use with the included egg configuration

## Why UV?

[UV](https://github.com/astral-sh/uv) is a drop-in replacement for pip that offers:
- 10-100x faster package installation
- Better dependency resolution
- Improved caching mechanisms
- Written in Rust for maximum performance

## Configuration Options

The images support several configuration options through environment variables:

- **GIT_ADDRESS**: Your git repository URL
- **BRANCH**: Specific branch to clone (optional)
- **PY_FILE**: Main Python file to execute (default: `app.py`)
- **REQUIREMENTS_FILE**: Requirements file name (default: `requirements.txt`)
- **PY_PACKAGES**: Additional packages to install (space-separated)
- **AUTO_UPDATE**: Enable automatic git pull on startup (0 or 1)
- **USERNAME/ACCESS_TOKEN**: Git authentication credentials (optional)


## Available Images

All images are hosted on GitHub Container Registry (ghcr.io):

### Python with UV

* [`python_uv_3.14`](/python_uv/3.14)
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.14`
* [`python_uv_3.13`](/python_uv/3.13)
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.13`
* [`python_uv_3.12`](/python_uv/3.12)
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.12`
* [`python_uv_3.11`](/python_uv/3.11)
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.11`
* [`python_uv_3.10`](/python_uv/3.10)
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.10`
* [`python_uv_3.9`](/python_uv/3.9)
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.9`
* [`python_uv_3.8`](/python_uv/3.8)
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.8`

## Installation Script

The egg includes an installation script that:
1. Clones your git repository
2. Installs UV package manager
3. Installs dependencies from requirements.txt or specified packages
4. Prepares the environment for your Python application

## Startup Behavior

On each server start, the container will:
1. Pull latest changes from git (if AUTO_UPDATE is enabled)
2. Install any additional packages specified in PY_PACKAGES
3. Install/update requirements from requirements.txt (if exists)
4. Execute your specified Python file

## Building

Images are automatically built via GitHub Actions on:
- Weekly schedule (every Monday)
- Push to master branch with changes in `python_uv/**`
- Manual workflow dispatch

To build locally:
```bash
docker build -t python_uv:3.13 ./python_uv/3.13
```

## Contributing

Contributions are welcome! When adding a new Python version:

1. Create a new directory under `python_uv/` with the version number
2. Add a Dockerfile based on the existing versions
3. Update the `.github/workflows/python.yml` matrix to include the new version
4. Update this README with the new image tag

## License

See [LICENSE.md](LICENSE.md) for details.

## Credits

- **Docker Images**: Based on [Pelican Eggs Yolks](https://github.com/pelican-eggs/yolks), modified to include UV package manager
- **Egg Configuration**: Based on [Pelican Eggs Generic](https://github.com/pelican-eggs/generic), modified to support UV package manager and enhanced workflow