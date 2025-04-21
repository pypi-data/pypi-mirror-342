# Development Guide

This guide provides instructions for setting up a development environment, running tests, and releasing new versions.

## Installation for Development

The project includes minimal dependencies optimized for CI workflows. To get started:

```bash
git clone https://github.com/arot-devs/procslib.git
cd procslib

# Setup environment for CI builds
make setup  

# Add the module for use in other projects
pip install -e .
```

For a complete inference environment, use the `pip_installer.sh` script:

```bash
conda create --name procslib python=3.10 ipykernel jupyterlab -y 
conda activate py310
./pip_installer.sh
```

## Testing & Linting

The following commands are available for ensuring code quality and functionality:

```bash
make format    # Auto-format the codebase
make test      # Run the test suite
make check     # Verify the code passes all checks
```

## Releasing

To release a new version, follow these steps:

1. **Update the Changelog**
   Document your changes in `CHANGELOG.md` using the command below:

   ```bash
   make changelog
   ```

2. **Bump the Version**
   Update the version number and create a new Git tag:

   ```bash
   make release version=x.y.z
   ```

3. **Publish to PyPI**
   If properly configured, the release will also be published to PyPI.