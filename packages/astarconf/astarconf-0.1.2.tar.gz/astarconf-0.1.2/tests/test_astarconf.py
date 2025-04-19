import tempfile
import os
import yaml
import json
from astarconf import Astarconf, encrypt_yaml_fields, decrypt_yaml_fields, generate_secret_key


def test_astarconf_from_yaml(tmp_path):
    yaml_path = tmp_path / "cfg.yaml"
    key_path = tmp_path / "key.key"
    data = {"user": "john", "password": "secret"}
    with open(yaml_path, "w") as f:
        yaml.dump(data, f)
    generate_secret_key(str(key_path))
    os.environ["ASTARCONF_SECRET"] = str(key_path)
    encrypt_yaml_fields(str(yaml_path), key_path.read_bytes())

    conf = Astarconf(str(yaml_path))
    assert conf.user == "john"
    assert conf["password"] == "secret"
    assert isinstance(conf.to_dict(), dict)


def test_astarconf_from_json(tmp_path):
    json_path = tmp_path / "cfg.json"
    key_path = tmp_path / "key.key"
    data = {"user": "alice", "password": "qwerty"}
    with open(json_path, "w") as f:
        json.dump(data, f)
    generate_secret_key(str(key_path))
    os.environ["ASTARCONF_SECRET"] = str(key_path)
    f = key_path.read_bytes()

    # simulate encryption
    encrypt_yaml_fields(str(json_path), f)

    # load & check
    conf = Astarconf(str(json_path))
    assert conf.user == "alice"
    assert conf["password"] == "qwerty"


def test_astarconf_from_env_file(tmp_path):
    env_file = tmp_path / ".env"
    key_path = tmp_path / "key.key"

    env_file.write_text("user=jdoe\npassword=topsecret\n")
    generate_secret_key(str(key_path))
    os.environ["ASTARCONF_SECRET"] = str(key_path)

    conf = Astarconf(str(env_file))
    assert conf.user == "jdoe"
    assert conf.password == "topsecret"


def test_astarconf_from_dict(monkeypatch):
    generate_secret_key(".test.key")
    monkeypatch.setenv("ASTARCONF_SECRET", ".test.key")

    conf = Astarconf({"user": "root", "password": "admin"})
    assert conf.user == "root"
    assert "password" in conf
    assert isinstance(conf.to_dict(), dict)

    os.remove(".test.key")

