import time
import yaml
import json
import subprocess
from pathlib import Path
from typing import List


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

    # ─────────────────────────────────────────────────────────────
    # plan
    # ─────────────────────────────────────────────────────────────
    @classmethod
    def plan(cls, envs: list[str], packages: list[str]) -> dict:
        """
        Build an in‑memory “super‑config” by reverse‑merging **all** YAML
        fragments in configs/<env>/ for every requested environment.

        Returns
        -------
        dict
            { "<env>": {merged config}, … }
        """
        combined: dict[str, dict] = {}

        for env in envs:
            env_dir = Path("configs") / env
            if not env_dir.is_dir():
                print(f"⚠️  No config dir for {env}: {env_dir}")
                continue

            # start with an empty dict and merge every *.yml
            merged: dict = {}
            for yml_path in sorted(env_dir.glob("*.yml")):
                with yml_path.open("r") as fh:
                    data = yaml.safe_load(fh) or {}
                merged = cls._deep_merge(merged, data)

            # optionally filter to requested *packages* only
            if packages:
                merged = {k: v for k, v in merged.items() if k in packages}

            combined[env] = merged

            print(f"\n[PLAN:{env}] merged {len(list(env_dir.glob('*.yml')))} files")
            print(json.dumps(merged, indent=2))

        return combined

    @classmethod
    def apply(cls, envs: list, packages: list):
        """
        Apply infrastructure changes for the given list of environments and packages.

        Simulates a Terraform apply-like operation, waits for stabilization, and confirms completion.

        :param envs: List of target environments.
        :param packages: List of package names.
        """
        for env in envs:
            print(f"[APPLY] Applying infrastructure changes for environment: {env}\n")
            for pkg in packages:
                print(f"  - [APPLY] For package '{pkg}' in {env}: applying changes...")
                # Stub: Insert Terraform apply abstraction for the package.
                time.sleep(0.1)  # Simulate processing delay.
            print(
                f"\n[APPLY] Waiting for infrastructure changes to stabilize in {env}..."
            )
            time.sleep(0.5)  # Simulate waiting period.
            print(
                f"[APPLY] All infrastructure changes applied and stabilized successfully in {env}!\n"
            )
