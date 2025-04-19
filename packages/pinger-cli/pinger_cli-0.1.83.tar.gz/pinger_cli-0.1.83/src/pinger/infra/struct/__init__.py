import time
import yaml
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional


class Infra:
    """
    Infra encapsulates the lifecycle operations for your infrastructure,
    similar to Terraform's plan and apply. Both actions now operate over a list
    of environments and a list of package names.
    """

    @classmethod
    def sh(cls, cmd: str, *, cwd: str | None = None) -> str:
        """
        Run *cmd* in the shell, stream output live, **and** return the full output.

        Parameters
        ----------
        cmd : str
            The shell command to execute.
        cwd : str | None, optional
            Working directory to run the command in.

        Returns
        -------
        str
            All stdout/stderr produced by the command.

        Raises
        ------
        subprocess.CalledProcessError
            If the command exits with a non‑zero code.
        """
        # Start the process, merging stderr into stdout for a single stream.
        proc = subprocess.Popen(
            cmd,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,  # decode to str immediately
            bufsize=1,  # line‑buffered
            universal_newlines=True,
        )

        lines: List[str] = []

        # Read line‑by‑line as it appears.
        assert proc.stdout is not None  # for mypy
        for line in proc.stdout:
            print(line, end="")  # live echo (already has newline)
            lines.append(line)

        proc.wait()

        full_output = "".join(lines)

        if proc.returncode:
            raise subprocess.CalledProcessError(
                proc.returncode, cmd, output=full_output
            )

        return full_output

    # ─────────────────────────────────────────────────────────────
    # helpers
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def _deep_merge(a: dict, b: dict) -> dict:
        """
        Recursively merge dict *b* into *a* – values in *b* win.
        (Used for the “reverse merge” behaviour.)
        """
        for k, v in b.items():
            if isinstance(v, dict) and isinstance(a.get(k), dict):
                a[k] = Infra._deep_merge(a[k], v)
            else:
                a[k] = v
        return a

    # ───────────────────────── package helpers ──────────────────────────
    @staticmethod
    def _package_key(pkg_dir: Path) -> Optional[str]:
        """Read *metadata.yml* inside one package dir and return its *package_key*."""
        meta_path = pkg_dir / "metadata.yml"
        if not meta_path.is_file():
            print(f"⚠️  {meta_path} missing")
            return None
        meta = yaml.safe_load(meta_path.read_text()) or {}
        key = meta.get("package_key")
        if not key:
            print(f"⚠️  No package_key in {meta_path}")
        return key

    # ───────────────────────────── plan ─────────────────────────────────
    @classmethod
    def plan(cls, envs: List[str], packages: List[str]) -> Dict[str, dict]:
        """
        Merge configs/<env>/*.yml and then slice out the sub‑configs whose
        **package_key** matches each requested package’s metadata.yml.

        Returns
        -------
        { "<env>": { "<pkg>": {config…}, … }, … }
        """
        pkg_root = Path("packages")
        if not pkg_root.is_dir():
            raise FileNotFoundError("packages/ dir not found")

        # ── figure out which packages we’re interested in ────────────
        wanted_pkgs = (
            [p.strip() for p in packages]
            if packages
            else [d.name for d in pkg_root.iterdir() if d.is_dir()]
        )

        # map package → package_key
        pkg_keys: Dict[str, str] = {}
        for pkg in wanted_pkgs:
            key = cls._package_key(pkg_root / pkg)
            if key:
                pkg_keys[pkg] = key

        combined: Dict[str, dict] = {}

        for env in envs:
            env_dir = Path("configs") / env
            if not env_dir.is_dir():
                print(f"⚠️  No config dir for {env}: {env_dir}")
                continue

            # 1. merge every YAML file in the env dir
            merged: dict = {}
            for yml in sorted(env_dir.glob("*.yml")):
                merged = cls._deep_merge(merged, yaml.safe_load(yml.read_text()) or {})

            # 2. slice the merged blob to only the chunks each package cares about
            env_slice: Dict[str, dict] = {}
            for pkg, key in pkg_keys.items():
                env_slice[pkg] = merged.get(key, {})
                if not env_slice[pkg]:
                    print(f"⚠️  key '{key}' for pkg '{pkg}' not found in {env}")

            combined[env] = env_slice

            print(f"\n[PLAN:{env}] merged {len(list(env_dir.glob('*.yml')))} files")
            print(json.dumps(env_slice, indent=2))

        return combined
