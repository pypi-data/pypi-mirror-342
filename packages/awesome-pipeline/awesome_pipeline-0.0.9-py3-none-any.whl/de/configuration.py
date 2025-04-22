from ..utils.de_utils import *


class Configuration:

    def __init__(self, file_path: str = "configuration/config.yml"):
        self.file_path = file_path
        self.config = self._load_config()

    def _load_config(self):
        """Load the YAML configuration file."""
        try:
            with open(os.path.join(get_base_dir(), self.file_path), "r") as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            print(f"File not found at: {os.path.join(get_base_dir(), self.file_path)}")
            return {}
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML file: {exc}")
            return {}

    def get(self, key_path, default=None):
        """Get a value from the configuration using a key path (e.g., 'database.host')."""
        keys = key_path.split(".")
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set(self, key_path, value):
        """Set a value in the configuration using a key path (e.g., 'database.host')."""
        keys = key_path.split(".")
        config = self.config
        for key in keys[:-1]:
            config = config.setdefault(key, {})
        config[keys[-1]] = value

    def remove(self, key_path):
        """Remove a key from the configuration using a key path (e.g., 'database.host')."""
        keys = key_path.split(".")
        config = self.config
        for key in keys[:-1]:
            config = config.get(key, {})
            if not isinstance(config, dict):
                return  # If the path is invalid, exit without doing anything
        config.pop(keys[-1], None)

    def save(self):
        """Save the configuration back to the YAML file."""
        try:
            with open(self.file_path, "w") as file:
                yaml.safe_dump(self.config, file)
        except yaml.YAMLError as exc:
            print(f"Error writing YAML file: {exc}")

    def update(self, updates, base_path=""):
        """Update multiple values in the configuration with optional base path for nested updates."""
        if not isinstance(updates, dict):
            print("Updates should be provided as a dictionary.")
            return

        for key, value in updates.items():
            full_key_path = f"{base_path}.{key}" if base_path else key
            if isinstance(value, dict):
                self.update(value, base_path=full_key_path)
            else:
                self.set(full_key_path, value)

    def reload(self):
        """Reload the configuration from the file."""
        self.config = self._load_config()

    def read(self):
        return read_yaml(self.file_path)
