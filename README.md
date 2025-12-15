# UV Python Egg - An Extremely Fast Pterodactyl/Pelican Eggs and Yolks Images

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/Dong-Chen-1031/UV-Python-Egg/python.yml?branch=master&label=Build%20Runtime%20Images&style=flat-square)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/Dong-Chen-1031/UV-Python-Egg/installer.yml?branch=master&label=Build%20Installer%20Image&style=flat-square)

English | [Traditional Chinese](README.zh-TW.md)

## Features
- 180 times faster server installation speed and 10-100 times faster package installation speed compared to [regular Python Egg](https://github.com/pelican-eggs/generic/tree/main/python).
- Supports both traditional pip workflow and modern uv package management workflow.
- Optimized installer container with pre-installed build dependencies to avoid wasting time on unnecessary installations.
- Allows users to pull their own Python source code from GitHub repositories.

![Optimized egg vs Python Egg](test/test.svg)

## Quick Start

### Import the Egg Configuration

Choose the egg file based on your panel type:

#### Pelican Panel (Recommended)
```
https://raw.githubusercontent.com/Dong-Chen-1031/UV-Python-Egg/refs/heads/master/egg/egg-python-uv.json
```

#### Pterodactyl Panel
```
https://raw.githubusercontent.com/Dong-Chen-1031/UV-Python-Egg/refs/heads/master/egg/egg-pterodactyl-python-uv.json
```

**Import Steps:**
1. In your admin panel, navigate to **Egg** → **Import Egg**
2. Paste the appropriate URL above in the import field
3. Click import and the egg will be automatically configured

**Alternative Downloads:**
- [Pelican: egg-python-uv.json](https://raw.githubusercontent.com/Dong-Chen-1031/UV-Python-Egg/refs/heads/master/egg/egg-python-uv.json)
- [Pterodactyl: egg-pterodactyl-python-uv.json](https://raw.githubusercontent.com/Dong-Chen-1031/UV-Python-Egg/refs/heads/master/egg/egg-pterodactyl-python-uv.json)

### Deploy Your Application

After importing the egg:
1. Create a new server using the "UV Python" egg
2. Select your desired Python version from the Docker images dropdown
3. Choose Dependency Install Mode:
   - **pip** (default): Uses requirements.txt + Additional Python packages via `uv pip install`
   - **uv**: Uses pyproject.toml + uv.lock via `uv sync`
4. Configure other environment variables (such as GIT_ADDRESS, PY_FILE, etc.)
5. Start your server and the application will automatically deploy
>[!Tip]
> After modifying the Git repository, the server needs to be reinstalled to apply the changes.

## How It Works
This project's optimizations are mainly divided into two types:
### 1. Using uv Package Manager to Accelerate Package Installation
[uv](https://github.com/astral-sh/uv) is a drop-in replacement for pip that offers:
- 10-100x faster package installation
- Better dependency resolution
- Improved caching mechanisms
- Written in Rust for maximum performance
### 2. Optimized Installer Container with Pre-installed Build Dependencies to Avoid Wasting Time on Unnecessary Installations
#### [Python Generic Egg](https://github.com/pelican-eggs/generic/tree/main/python) Installation Process:
- Uses `python:3.12-slim-bookworm` image as the installer container
- Executes `apt-get install` in the installation script to install numerous build dependencies
- Every installation requires re-downloading and installing these dependencies, resulting in excessively long installation times
#### This Project's Installation Process:
- Uses a dedicated `ghcr.io/dong-chen-1031/yolks:python_uv_installer` image as the installer container
- This image comes pre-installed with all commonly used build dependencies
- Avoids the need to re-download and install these dependencies with each installation, reducing installation time by approximately 170 times.
> [!NOTE]
> This dual-image architecture already exists, for example, Python Generic Egg uses `python:3.12-slim-bookworm` during installation and `ghcr.io/parkervcp/yolks:python_3.xx` during runtime, so there is no issue of extra installer image consuming storage space.

Through these two optimization methods, the deployment speed and performance of Python applications on Pterodactyl and Pelican panels are significantly improved.

## Features

### Core Features
- **UV Package Manager**: Lightning-fast Python package installer and resolver, written in Rust (10-100x faster than pip)
- **Dual Installation Modes**:
  - **pip mode**: `uv pip install` with requirements.txt (traditional workflow)
  - **uv mode**: `uv sync` with pyproject.toml + uv.lock (modern project management)
- **Multi-Version Support**: Python versions from 3.8 to 3.14
- **Multi-Architecture**: Available for both `linux/amd64` and `linux/arm64`

### Security & Reliability
- Installation uses root container with all dependencies
- Runtime uses non-root container for enhanced security

### Developer Experience
- **Auto-Updates**: Built-in support for git repository auto-updates on startup
- **Flexible Dependency Management**: Support for requirements.txt, pyproject.toml, or direct package installation
- **CI/CD Ready**: GitHub Actions workflows automatically build images periodically and rebuild regularly to ensure the latest dependencies are used.

## Configuration Options

The eggs support comprehensive configuration through environment variables:

### Core Settings
- **GIT_ADDRESS**: Your git repository URL (e.g., `https://github.com/username/repo`)
- **BRANCH**: Specific branch to clone (optional, defaults to repo's default branch)
- **USERNAME/ACCESS_TOKEN**: Git authentication credentials (for private repos)
- **AUTO_UPDATE**: Enable automatic git pull on startup (`0` = disabled, `1` = enabled)
- **USER_UPLOAD**: Skip the entire installation script if you're uploading files manually

### Python Configuration
- **PY_FILE**: Main Python file to execute (default: `app.py`)
- **DEPENDENCY_INSTALL_MODE**: Choose dependency installation method
  - `pip` (default): Uses `uv pip install` with requirements.txt + additional packages
  - `uv`: Uses `uv sync` with pyproject.toml (ignores requirements.txt and PY_PACKAGES)

### Package Management (pip mode only)
- **REQUIREMENTS_FILE**: Requirements file name (default: `requirements.txt`)
- **PY_PACKAGES**: Additional packages to install (space-separated, e.g., `flask requests`)

### UV Mode (when DEPENDENCY_INSTALL_MODE=uv)
When using uv mode, dependencies are managed through:
- **pyproject.toml**: Project configuration and direct dependencies
- **uv.lock**: Locked dependency versions (auto-generated by uv)
- Environment: `/home/container/.local/uv` (set via UV_PROJECT_ENVIRONMENT)

> [!WARNING]  
> When using uv mode, the Python version settings in pyproject.toml will not be applied. Please ensure your project is compatible with the selected runtime image version.


## Available Images

All images are hosted on GitHub Container Registry (ghcr.io) and built for both amd64 and arm64 architectures.

### Runtime Images (Python with UV)

* [`python_uv_3.14`](/python_uv/3.14) - Python 3.14 with UV
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.14`
* [`python_uv_3.13`](/python_uv/3.13) - Python 3.13 with UV  
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.13`
* [`python_uv_3.12`](/python_uv/3.12) - Python 3.12 with UV
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.12`
* [`python_uv_3.11`](/python_uv/3.11) - Python 3.11 with UV
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.11`
* [`python_uv_3.10`](/python_uv/3.10) - Python 3.10 with UV
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.10`
* [`python_uv_3.9`](/python_uv/3.9) - Python 3.9 with UV
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.9`
* [`python_uv_3.8`](/python_uv/3.8) - Python 3.8 with UV
  * `ghcr.io/dong-chen-1031/yolks:python_uv_3.8`

### Installer Image

* [`python_uv_installer`](/python_uv/installer) - Dedicated installation environment
  * `ghcr.io/dong-chen-1031/yolks:python_uv_installer`
  * Based on Python 3.12 with all build dependencies
  * Runs as root for package compilation
  * Used during egg installation phase only

## Building & Development

### Automated Builds

Images are automatically built via GitHub Actions workflows:

#### Runtime Images ([.github/workflows/python.yml](.github/workflows/python.yml))
- **Triggers**: Push to `python_uv/3.*/**`, weekly schedule (Monday), manual dispatch
- **Output**: `ghcr.io/dong-chen-1031/yolks:python_uv_3.{8-14}`
- **Architectures**: linux/amd64, linux/arm64

#### Installer Image ([.github/workflows/installer.yml](.github/workflows/installer.yml))
- **Triggers**: Push to `python_uv/installer/**`, weekly schedule (Monday), manual dispatch
- **Output**: `ghcr.io/dong-chen-1031/yolks:python_uv_installer`
- **Architectures**: linux/amd64, linux/arm64

#### Egg Generation ([.github/workflows/hen.yml](.github/workflows/hen.yml))
- **Triggers**: Push to `script/install.sh`, `script/start.sh`, `script/hens/**`, `script/hen.py`, manual dispatch
- **Process**: Runs `hen.py` to regenerate eggs from templates
- **Output**: Auto-commits updated eggs to `egg/` directory

### Local Building

Build runtime images:
```bash
docker build -t python_uv:3.13 ./python_uv/3.13
```

Build installer image:
```bash
docker build -t python_uv_installer ./python_uv/installer
```

Generate eggs locally:
```bash
cd script
python3 hen.py
```

### Development Workflow

1. **Modify Scripts**: Edit `script/install.sh` or `script/start.sh`
2. **Update Templates**: Modify egg templates in `script/hens/` if needed
3. **Test Locally**: Run `python3 hen.py` to verify generation
4. **Push Changes**: GitHub Actions automatically regenerates and commits eggs
5. **No Manual Egg Editing**: Never edit files in `egg/` directly - they're auto-generated!

## Project Structure

```
UV-Python-Egg/
├── .github/workflows/
│   ├── python.yml          # Builds runtime images (3.8-3.14)
│   ├── installer.yml       # Builds installer image
│   └── hen.yml            # Auto-generates eggs from templates
├── python_uv/
│   ├── 3.8/ ... 3.14/     # Runtime image Dockerfiles
│   └── installer/         # Installer image Dockerfile
├── script/
│   ├── hens/              # Egg templates (source of truth)
│   │   ├── egg-python-uv.json              # Pelican template
│   │   └── egg-pterodactyl-python-uv.json  # Pterodactyl template
│   ├── hen.py             # Egg generator (the mother hen 🐔)
│   ├── install.sh         # Installation script
│   └── start.sh           # Startup script
├── egg/                   # Generated eggs (DO NOT EDIT)
│   ├── egg-python-uv.json              # Auto-generated Pelican egg
│   └── egg-pterodactyl-python-uv.json  # Auto-generated Pterodactyl egg
├── LICENSE.md
└── README.md
```

## License

See [LICENSE.md](LICENSE.md) for details.

## Credits

- **Yolks**: Based on [Pelican Eggs Yolks](https://github.com/pelican-eggs/yolks) with UV integration
- **Egg Configuration**: Based on [Pelican Eggs Generic](https://github.com/pelican-eggs/generic) with enhanced UV support
- **UV Package Manager**: [astral-sh/uv](https://github.com/astral-sh/uv) - An extremely fast Python package installer and resolver

## Links

- **Repository**: [Dong-Chen-1031/UV-Python-Egg](https://github.com/Dong-Chen-1031/UV-Python-Egg)
- **Docker Images**: [ghcr.io/dong-chen-1031/yolks](https://github.com/Dong-Chen-1031/UV-Python-Egg/pkgs/container/yolks)
- **Upstream Projects**:
  - [Pelican Eggs](https://github.com/pelican-eggs)
  - [UV Package Manager](https://github.com/astral-sh/uv)
  - [Pelican Panel](https://pelican.dev/)