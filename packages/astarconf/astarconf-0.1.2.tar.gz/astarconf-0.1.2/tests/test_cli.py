import subprocess
import tempfile
import yaml
import os
import shutil
import pytest
from pathlib import Path


def run_astarconf_cli(*args):
    return subprocess.run(
        ["astarconf", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8"
    )


@pytest.mark.integration
def test_generate_encrypt_decrypt_cycle(tmp_path):
    secret_path = tmp_path / "secret.key"
    yaml_path = tmp_path / "config.yaml"
    output_path = tmp_path / "decrypted.yaml"

    yaml_data = {"user": "test", "password": "1234"}
    with open(yaml_path, "w") as f:
        yaml.dump(yaml_data, f)

    run_astarconf_cli("-g", str(secret_path))
    assert secret_path.exists()

    os.environ["ASTARCONF_SECRET"] = str(secret_path)
    run_astarconf_cli("-c", str(yaml_path))
    encrypted = yaml.safe_load(open(yaml_path))
    assert encrypted["user"].startswith("gAAAA")

    run_astarconf_cli("-d", str(yaml_path), "-o", str(output_path))
    decrypted = yaml.safe_load(open(output_path))
    assert decrypted == yaml_data


def test_cli_help_output():
    result = run_astarconf_cli("--help")
    assert "usage" in result.stdout.lower()
    assert "-g" in result.stdout
    assert "Examples" in result.stdout


def test_cli_output_force_overwrite(tmp_path):
    key_path = tmp_path / "secret.key"
    yaml_path = tmp_path / "secrets.yaml"
    out_path = tmp_path / "decrypted.yaml"

    with open(yaml_path, "w") as f:
        yaml.dump({"user": "alice", "password": "bob"}, f)

    run_astarconf_cli("-g", str(key_path))
    os.environ["ASTARCONF_SECRET"] = str(key_path)
    run_astarconf_cli("-c", str(yaml_path))
    run_astarconf_cli("-d", str(yaml_path), "-o", str(out_path))

    result = run_astarconf_cli("-d", str(yaml_path), "-o", str(out_path))
    assert "already exists" in result.stdout

    result = run_astarconf_cli("-d", str(yaml_path), "-o", str(out_path), "-f")
    assert "decrypted" in result.stdout.lower()

