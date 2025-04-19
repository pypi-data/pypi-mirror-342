import time
import subprocess
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

    @classmethod
    def plan(cls, envs: list, packages: list):
        """
        Generate infrastructure plans for the given list of environments and packages.

        Simulates a Terraform plan-like operation.

        :param envs: List of target environments (e.g., ["some-env"]).
        :param packages: List of package names (e.g., ["package-a", "package-b"]).
        """
        cfgs = {}
        for env in envs:
            print(f"[Config] Generating configuration for environment: {env}\n")
            for package in packages:
                with open(f"configs/{env}/config.yml", "r") as f:
                    cfgs[package] = f.read()

        print(cfgs)

        # for env in envs:
        #     print(f"[PLAN] Generating infrastructure plan for environment: {env}\n")
        #     for pkg in packages:
        #         print(f"  - [PLAN] For package '{pkg}' in {env}: generating plan...")
        #         # Stub: Insert Terraform planning abstraction here.
        #         time.sleep(0.1)  # Simulate processing delay.
        #     print(f"\n[PLAN] Infrastructure plan complete for environment: {env}\n")

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
