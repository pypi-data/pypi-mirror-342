import os
import sys
import argparse
import yaml
from . import (
    find_secret_key,
    generate_secret_key,
    delete_secret_key,
    encrypt_yaml_fields,
    decrypt_yaml_fields,
)


def cli_entrypoint(argv=None):
    parser = argparse.ArgumentParser(
        description="astarconf — tool for managing encrypted configuration files.",
        epilog="""Examples:
  Generate a new secret key:
    astarconf -g ~/.astarconf/secret.key

  Encrypt default fields 'user' and 'password':
    astarconf -c config.yaml

  Encrypt specific fields:
    astarconf -c config.yaml token api_key

  Decrypt a file and overwrite it:
    astarconf -d config.yaml

  Decrypt to another file (if not exists):
    astarconf -d config.yaml -o config_plain.yaml

  Force overwrite:
    astarconf -d config.yaml -o config_plain.yaml -f
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-g", "--generate", nargs="?", const=os.path.expanduser("~/.astarconf/secret.key"),
        help="Generate a new secret key (default: ~/.astarconf/secret.key)"
    )
    parser.add_argument("-r", "--remove", help="Delete a secret key at specified path")
    parser.add_argument(
        "-c", "--crypt", nargs="+",
        help="Encrypt YAML file: first argument is path, others are field names (default: user, password)"
    )
    parser.add_argument("-d", "--decrypt", help="Decrypt all encrypted fields in YAML file")
    parser.add_argument("-o", "--output", help="Optional output path for decrypted YAML file")
    parser.add_argument("-f", "--force", action="store_true", help="Allow overwriting the output file if it exists")
    
    args = parser.parse_args(argv)

    if args.generate:
        generate_secret_key(args.generate)
    elif args.remove:
        delete_secret_key(args.remove)
    elif args.crypt:
        key = find_secret_key()
        yaml_file = args.crypt[0]
        custom_fields = args.crypt[1:] if len(args.crypt) > 1 else None
        encrypt_yaml_fields(yaml_file, key, custom_fields)
    elif args.decrypt:
        key = find_secret_key()
        decrypt_yaml_fields(args.decrypt, key, output_path=args.output, force=args.force)
    else:
        parser.print_help()

def main():
    import sys
    from .cli import cli_entrypoint
    cli_entrypoint(sys.argv[1:])
