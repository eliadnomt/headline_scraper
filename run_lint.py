import subprocess
import sys
from pathlib import Path

import yaml


def main():
    cfg_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("lint_config.yaml")
    if not cfg_path.exists():
        sys.exit(f"Config linter file not found: {cfg_path}")

    with cfg_path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    def run(cmd):
        print(f"\n>>> {cmd}")
        res = subprocess.run(cmd, shell=True)
        if res.returncode != 0:
            print(f"[!] {cmd} exited with {res.returncode}")

    if cfg.get("black"):
        run("black .")
    if cfg.get("isort"):
        run("isort .")
    if cfg.get("mypy"):
        run("mypy . --ignore-missing-imports")
    if cfg.get("pylint"):
        run("pylint src --disable=R1734,W0511")  # adjust to your code directory
    if cfg.get("coverage"):
        run("coverage run -m pytest && coverage report")


if __name__ == "__main__":
    main()
