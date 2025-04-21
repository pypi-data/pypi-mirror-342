# Decluttering VSCode

it's recommended to hide certain files that you don't need to see in the file explorer. This can be done by adding the following to your `settings.json` file:

[ref](https://stackoverflow.com/questions/30140112/how-to-hide-specified-files-directories-e-g-git-in-the-sidebar-vscode)

1. create a `.vscode` folder in the root of your project if it doesn't exist
2. create a `settings.json` file in the `.vscode` folder
3. add the following to the `settings.json` file, change or add any additional files you want to hide:

a
```
// Workspace settings
{
    // The following will hide the js and map files in the editor
    "files.exclude": {
        "**/*.js": true,
        "**/*.map": true,    # Decluttering VSCode

For tidier workspace, hide build artifacts, venvs, or config files in `.vscode/settings.json`.

Example:

```jsonc
{
  "files.exclude": {
    "**/*.js": true,
    "**/*.map": true,
    // ...
    "**/.venv": true,
    "**/__pycache__": true,
    "**/tests": true,
    // etc
  }
}

```

This keeps your file explorer uncluttered.

For a complete version of the vscode config, check: `docs/vscode_settings.json.example`
    


        // venvs and build files
        "**/.venv": true,
        "**/.venvs": true,
        "**/.pdm-build": true,
        "**/.ruff_cache": true,
        "**/__pycache__": true,
        "**/htmlcov": true,
        "**/.coverage.310": true,

        // unused configs
        "**/config": true,

        // Additional files to hide
        "**/.copier-answers.yml": true,
        "**/.envrc": true,
        // "**/.gitignore": true,
        "**/.python-version": true,
        // "**/CHANGELOG.md": true,
        "**/CODE_OF_CONDUCT.md": true,
        "**/CONTRIBUTING.md": true,
        "**/duties.py": true,
        "**/LICENSE": true,
        "**/Makefile": true,
        "**/mkdocs.yml": true,
        "**/pyproject.toml": true,
        // "**/README.md": true,
        "**/uv.lock": true,
        "**/site": true,
        "**/tests": true,
        // "**/.github": true,
        // "**/scripts": true,


    }
}
```