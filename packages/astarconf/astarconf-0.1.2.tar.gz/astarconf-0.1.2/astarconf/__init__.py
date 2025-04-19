import os
import sys
import argparse
import yaml
from cryptography.fernet import Fernet


class Color:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"


class AttrNamespace:
    """Provides attribute and key-style access to nested dictionaries.

    Supports `.key`, `['key']`, `.to_dict()`, `.to_json()` and JSON import.
    """
    __slots__ = ('__data',)

    def __init__(self, mapping):
        object.__setattr__(self, '_AttrNamespace__data', {})
        for k, v in mapping.items():
            if isinstance(v, dict):
                v = AttrNamespace(v)
            self.__data[k] = v

    def __getattr__(self, name):
        try:
            return self.__data[name]
        except KeyError:
            raise AttributeError(name)

    def __getitem__(self, key):
        """Allows dict-style access to top-level keys.

        Args:
            key (str): Top-level config key.

        Returns:
            Any: The corresponding config value.
        """
        return self.__data[key]

    def __setattr__(self, name, value):
        self.__data[name] = value

    def __dir__(self):
        return list(self.__data.keys())

    def __contains__(self, key):
        return key in self.__data

    def to_dict(self):
        """Recursively converts the AttrNamespace to a plain Python dictionary.

        Returns:
            dict: A deep copy of internal data as a plain dict.
        """
        def unwrap(value):
            if isinstance(value, AttrNamespace):
                return value.to_dict()
            return value
        return {k: unwrap(v) for k, v in self.__data.items()}

    def to_json(self, **kwargs):
        """Serializes the internal data to a JSON-formatted string.

        Args:
            **kwargs: Optional arguments passed to `json.dumps()`.

        Returns:
            str: JSON string representation.
        """
        import json
        return json.dumps(self.to_dict(), **kwargs)

    @classmethod
    def from_json(cls, json_str):
        """Creates an AttrNamespace object from a JSON string.

        Args:
            json_str (str): JSON-formatted string.

        Returns:
            AttrNamespace: An instance initialized from the JSON data.
        """
        import json
        data = json.loads(json_str)
        return cls(data)

    def __repr__(self):
        """Returns string representation of the configuration object.

        Returns:
            str: Debug-friendly string with current config.
        """
        return f"<AttrNamespace {self.__data}>"

    def __contains__(self, key):
        return key in self.__data

    def to_dict(self):
        def unwrap(value):
            if isinstance(value, AttrNamespace):
                return value.to_dict()
            return value
        return {k: unwrap(v) for k, v in self.__data.items()}

    def to_json(self, **kwargs):
        import json
        return json.dumps(self.to_dict(), **kwargs)

    @classmethod
    def from_json(cls, json_str):
        import json
        data = json.loads(json_str)
        return cls(data)
        return f"<AttrNamespace {self.__data}>"
        self.__data[name] = value

    def __dir__(self):
        return list(self.__data.keys())

    def __repr__(self):
        return f"<AttrNamespace {self.__data}>"
        return f"<AttrNamespace {self.__data}>"
        list(self.__data.keys())

    def __repr__(self):
        return f"<AttrNamespace {self.__data}>"

    def __init__(self, mapping):
        object.__setattr__(self, '_AttrNamespace__data', {})
        for k, v in mapping.items():
            if isinstance(v, dict):
                v = AttrNamespace(v)
            self.__data[k] = v

    def __getattr__(self, name):
        try:
            return self.__data[name]
        except KeyError:
            raise AttributeError(name)

    def __getitem__(self, key):
        return self.__data[key]

    def __setattr__(self, name, value):
        self.__data[name] = value

    def __dir__(self):
        return list(self.__data.keys())

    def __repr__(self):
        return f"<AttrNamespace {self.__data}>"

    def __init__(self, mapping):
        object.__setattr__(self, '_AttrNamespace__data', {})
        for k, v in mapping.items():
            if isinstance(v, dict):
                v = AttrNamespace(v)
            self.__data[k] = v

    def __getattr__(self, name):
        try:
            return self.__data[name]
        except KeyError:
            raise AttributeError(name)

    def __getitem__(self, key):
        return self.__data[key]

    def __setattr__(self, name, value):
        self.__data[name] = value

    def __dir__(self):
        return list(self.__data.keys())

    def __repr__(self):
        return f"<AttrNamespace {self.__data}>"

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

    def __dir__(self):
        return list(super().keys()) + list(super().__dir__())

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


DEFAULT_SECRET_LOCATIONS = [
    lambda: os.getenv("ASTARCONF_SECRET"),
    lambda: os.path.expanduser("~/.astarconf/secret.key"),
    lambda: "/etc/astarconf/secret.key",
    *[lambda dir_path=path: os.path.join(dir_path, fname)
      for path in os.getenv("PATH", "").split(os.pathsep)
      for fname in ("astarconf.key", "astarconf_secret.key", "secret.key")]
]


def find_secret_key():
    """Searches default locations for the secret key used for encryption.

    Returns:
        bytes: The loaded secret key.

    Raises:
        FileNotFoundError: If no valid key is found in known locations.
    """
    for path_func in DEFAULT_SECRET_LOCATIONS:
        try:
            path = path_func()
            if path and os.path.isfile(path):
                with open(path, "rb") as f:
                    key = f.read().strip()
                    if not key:
                        continue
                    return key
        except Exception:
            continue
    print(f"{Color.RED}Secret key not found in any of the expected locations.{Color.RESET}")
    raise FileNotFoundError()


def generate_secret_key(to_path):
    """Generates and stores a new encryption key at the given file path.

    Args:
        to_path (str): Path to save the generated key.

    Exits:
        On error creating the directory or writing the file.
    """
    try:
        os.makedirs(os.path.dirname(to_path), exist_ok=True)
    except Exception as e:
        print(f"{Color.RED}Error creating directory for secret key: {e}{Color.RESET}")
        sys.exit(1)

    key = Fernet.generate_key()
    with open(to_path, "wb") as f:
        f.write(key)
    os.chmod(to_path, 0o600)
    print(f"{Color.GREEN}Secret key saved to {to_path}{Color.RESET}")


def delete_secret_key(path):
    """Deletes the secret key file if it exists.

    Args:
        path (str): Path to the key file to be deleted.
    """
    if os.path.isfile(path):
        os.remove(path)
        print(f"{Color.YELLOW}Deleted secret key from {path}{Color.RESET}")
    else:
        print(f"{Color.RED}Key file does not exist.{Color.RESET}")


def encrypt_yaml_fields(yaml_path, key, field_names=None):
    """Encrypts specified fields in a YAML file using Fernet.

    Args:
        yaml_path (str): Path to the YAML configuration file.
        key (bytes): Encryption key (Fernet).
        field_names (list, optional): List of fields to encrypt. Defaults to ['user', 'password'].
    """
    if field_names is None:
        field_names = ["user", "password"]

    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)

    fernet = Fernet(key)

    def encrypt_fields(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in field_names and isinstance(v, str):
                    obj[k] = fernet.encrypt(v.encode()).decode()
                else:
                    encrypt_fields(v)
        elif isinstance(obj, list):
            for item in obj:
                encrypt_fields(item)

    encrypt_fields(data)

    with open(yaml_path, 'w') as f:
        yaml.dump(data, f, allow_unicode=True)

    print(f"{Color.GREEN}Encrypted fields in {yaml_path}{Color.RESET}")


def decrypt_yaml_fields(yaml_path, key, output_path=None, force=False):
    """Decrypts encrypted fields in a YAML file.

    Args:
        yaml_path (str): Path to the encrypted YAML file.
        key (bytes): Encryption key.
        output_path (str, optional): Path to save decrypted output. Defaults to overwriting input.
        force (bool): Overwrite output file if it exists. Defaults to False.
    """
    if output_path and os.path.exists(output_path) and not force:
        print(f"{Color.RED}Error: Output file '{output_path}' already exists. Use --force to overwrite.{Color.RESET}")
        sys.exit(1)

    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)

    fernet = Fernet(key)

    def decrypt_fields(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, str) and is_encrypted(v):
                    try:
                        obj[k] = fernet.decrypt(v.encode()).decode()
                    except Exception:
                        pass
                else:
                    decrypt_fields(v)
        elif isinstance(obj, list):
            for item in obj:
                decrypt_fields(item)

    decrypt_fields(data)

    output_file = output_path or yaml_path
    with open(output_file, 'w') as f:
        yaml.dump(data, f, allow_unicode=True)

    print(f"{Color.GREEN}Decrypted fields written to {output_file}{Color.RESET}")


def is_encrypted(value):
    """Determines if a given string is encrypted based on Fernet prefix.

    Args:
        value (str): String to check.

    Returns:
        bool: True if encrypted, False otherwise.
    """
    return (
        isinstance(value, str)
        and value.startswith("gAAAAAB")
        and len(value) > 50
    )


from dotenv import dotenv_values
import json

class Astarconf:
    def __init__(self, source, nested_as_attr=False, hybrid_mode=True):
        self._key = find_secret_key()
        self._fernet = Fernet(self._key)

        if isinstance(source, dict):
            self._data = source
        elif isinstance(source, str):
            if source.endswith(('.yaml', '.yml')):
                with open(source, 'r') as f:
                    self._data = yaml.safe_load(f)
            elif source.endswith('.json'):
                with open(source, 'r') as f:
                    self._data = json.load(f)
            elif source.endswith('.env'):
                self._data = dict(dotenv_values(source))
            else:
                raise ValueError(f"Unsupported config format: {source}")
        else:
            raise TypeError("Astarconf source must be dict or path to a YAML/JSON/.env file")

        self._decrypt_fields(self._data)

        for key, value in self._data.items():
            if hybrid_mode and isinstance(value, dict):
                setattr(self, key, AttrNamespace(value))
            elif nested_as_attr and isinstance(value, dict):
                setattr(self, key, AttrNamespace(value))
            else:
                setattr(self, key, value)

    def _decrypt_fields(self, obj):
        """Recursively decrypts any encrypted values in a dictionary or list."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, str) and is_encrypted(v):
                    try:
                        obj[k] = self._fernet.decrypt(v.encode()).decode()
                    except Exception:
                        pass
                else:
                    self._decrypt_fields(v)
        elif isinstance(obj, list):
            for item in obj:
                self._decrypt_fields(item)

    def __getitem__(self, key):
        return self._data[key]

    def __repr__(self):
        return f"<Astarconf {self._data}>"

