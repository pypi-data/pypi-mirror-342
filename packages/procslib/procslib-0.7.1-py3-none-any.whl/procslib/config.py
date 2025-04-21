# procslib/config.py

# Dictionary to store all configuration values
_config = {
    "HF_ORG": "incantor",
}


def set_config(key: str, value):
    """Set a configuration value dynamically."""
    global _config
    _config[key] = value


def get_config(key: str, default=None):
    """Retrieve a configuration value dynamically."""
    return _config.get(key, default)


def get_configs():
    """Retrieve all configuration values as a dictionary."""
    return _config.copy()
