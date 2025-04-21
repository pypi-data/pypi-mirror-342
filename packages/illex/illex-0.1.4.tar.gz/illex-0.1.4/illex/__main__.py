import argparse
import sys
import illex
import json
import os

def parse_vars(vars_list):
    if not vars_list:
        return {}

    first = vars_list[0]
    if os.path.isfile(first):
        ext = os.path.splitext(first)[1].lower()
        try:
            with open(first, "r") as f:
                if ext == ".json":
                    return json.load(f)
                elif ext in [".yaml", ".yml"]:
                    import yaml
                    return yaml.safe_load(f)
        except Exception as e:
            sys.stderr.write(f"Error reading vars file: {e}\n")
            sys.exit(1)

    vars_dict = {}
    for item in vars_list:
        if '=' not in item:
            sys.stderr.write(f"Invalid var format: {item} (expected key=value)\n")
            sys.exit(1)
        key, value = item.split("=", 1)
        vars_dict[key] = value
    return vars_dict


def run(path: str, output: bool, vars_arg: list):
    if not path.endswith(".illex"):
        sys.stderr.write("Error: Invalid file extension! Expected a .illex file.\n")
        sys.exit(1)

    try:
        with open(path, "r") as f:
            text = f.read()
    except FileNotFoundError:
        sys.stderr.write(f"Error: File not found: {path}\n")
        sys.exit(1)

    vars_dict = parse_vars(vars_arg)

    try:
        result = illex.parse(text, params=vars_dict)
    except Exception as e:
        sys.stderr.write(f"Error during parsing: {e}\n")
        sys.exit(1)

    if output:
        out_path = f"{path}.out"
        try:
            with open(out_path, "w") as f:
                f.write(str(result))
        except Exception as e:
            sys.stderr.write(f"Error writing output: {e}\n")
            sys.exit(1)
    else:
        sys.stdout.write(str(result) + "\n")


def main():
    parser = argparse.ArgumentParser(
        prog="illex",
        description="ILLEX – Inline Language for Logic and EXpressions"
    )

    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run a .illex file")
    run_parser.add_argument("path", help="Path to the .illex file")
    run_parser.add_argument("-o", "--output", action="store_true", help="Write result to .out file")
    run_parser.add_argument("--vars", nargs="+", help="Variable input (file.json, file.yaml or k=v list)")

    args = parser.parse_args()

    if args.command == "run":
        run(args.path, args.output, args.vars)
    else:
        parser.print_help()
        sys.exit(1)
