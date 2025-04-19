# astarconf

🛡 A secure, pluggable config loader for YAML, JSON, `.env` and Python dicts — with field-level encryption, CLI support, and hybrid access.

## Features

- 🔐 Encrypt/decrypt fields in YAML
- 🔌 Load from `.yaml`, `.json`, `.env`, or `dict`
- ✅ Attribute (`config.key`) and key (`config['key']`) access
- 🧰 CLI interface for encryption workflows

## Installation

```bash
pip install astarconf
```

## Usage

```python
from astarconf import Astarconf

conf = Astarconf("config.yaml")
print(conf.database.user)
```

### CLI

```bash
astarconf -g ~/.astarconf/secret.key	#Generate a new secret key (default: ~/.astartool/secret.key)
astarconf -r ~/.astarconf/secret.key	#Delete a secret key at specified path
astarconf -c config.yaml user password	#Encrypt YAML file: first argument is path, 
                                        others are field names (default: user, password)
astarconf -d config.yaml -o output.yaml	#Decrypt all encrypted fields in YAML file 
```

## License

MIT

---

## 📚 Full Documentation

See [DOCUMENTATION.md](DOCUMENTATION.md) for detailed API and CLI usage.
