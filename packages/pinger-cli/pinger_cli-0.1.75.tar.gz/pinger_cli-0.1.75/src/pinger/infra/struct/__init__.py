import time


class Infra:
    """
    Infra encapsulates the lifecycle operations for your infrastructure,
    similar to Terraform's plan and apply. Both actions now operate over a list
    of environments and a list of package names.
    """

    @classmethod
    def plan(cls, envs: list, packages: list):
        """
        Generate infrastructure plans for the given list of environments and packages.

        Simulates a Terraform plan-like operation.

        :param envs: List of target environments (e.g., ["some-env"]).
        :param packages: List of package names (e.g., ["package-a", "package-b"]).
        """
        for env in envs:
            print(f"[PLAN] Generating infrastructure plan for environment: {env}\n")
            for pkg in packages:
                print(f"  - [PLAN] For package '{pkg}' in {env}: generating plan...")
                # Stub: Insert Terraform planning abstraction here.
                time.sleep(0.1)  # Simulate processing delay.
            print(f"\n[PLAN] Infrastructure plan complete for environment: {env}\n")

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
