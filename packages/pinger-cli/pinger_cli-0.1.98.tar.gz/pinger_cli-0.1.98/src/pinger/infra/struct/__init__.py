#!/usr/bin/env python3
"""
Pinger Infra helpers
────────────────────
• reverse‑merge env‑level YAML fragments
• map them to packages by *package_key*
• emit config.json + backend config.hcl for every package / env
"""

from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional

import yaml


class Infra:
    # ───── new helper ───────────────────────────────────────────────
    @staticmethod
    def _lookup_key(blob: dict, key: str) -> dict:
        """
        Return the sub‑dict for *key* if it exists;
        otherwise try dash↔underscore substitution.
        """
        if key in blob:
            return blob[key]

        alt = key.replace("-", "_") if "-" in key else key.replace("_", "-")
        return blob.get(alt, {})

    # ───────────────────────── Shell helper ──────────────────────────
    @classmethod
    def sh(cls, cmd: str, *, cwd: str | None = None) -> str:
        """Run *cmd*, stream its output live, **and** return full stdout+stderr."""
        proc = subprocess.Popen(
            cmd,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        lines: List[str] = []
        assert proc.stdout is not None
        for line in proc.stdout:
            print(line, end="")
            lines.append(line)

        proc.wait()
        output = "".join(lines)
        if proc.returncode:
            raise subprocess.CalledProcessError(proc.returncode, cmd, output=output)
        return output

    # ───────────────────────── Misc helpers ──────────────────────────
    @staticmethod
    def _deep_merge(a: dict, b: dict) -> dict:
        """Recursively merge *b* into *a* (values in *b* override)."""
        for k, v in b.items():
            if isinstance(v, dict) and isinstance(a.get(k), dict):
                a[k] = Infra._deep_merge(a[k], v)
            else:
                a[k] = v
        return a

    @staticmethod
    def _package_key(pkg_dir: Path) -> Optional[str]:
        """Return the *package_key* defined in packages/<pkg>/metadata.yml."""
        meta_path = pkg_dir / "metadata.yml"
        if not meta_path.is_file():
            print(f"⚠️  {meta_path} missing")
            return None
        meta = yaml.safe_load(meta_path.read_text()) or {}
        key = meta.get("package_key")
        if not key:
            print(f"⚠️  No package_key in {meta_path}")
        return key

    # ───────────────────────── HCL writer ────────────────────────────
    @staticmethod
    def _write_backend_hcl(pkg_dir: Path, env: str, package_key: str) -> None:
        """Generate Terraform ‑backend config.hcl for one package / env."""
        region_map = {"use1": "us-east-1", "usw2": "us-west-2"}
        suffix = env[-4:]
        region = region_map.get(suffix, "us-west-2")

        hcl = f"""\
acl            = "bucket-owner-full-control"
bucket         = "{env}-terraform-state-bucket"
dynamodb_table = "{env}-terraform-state-lock-table"
encrypt        = "false"
key            = "{env}/{package_key}/terraform.tfstate"
profile        = "{env}"
region         = "{region}"
"""
        out_path = pkg_dir / "configs" / env / "config.hcl"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(hcl)
        print(f"💾  wrote {out_path}")

    # ────────────────────────────── PLAN ──────────────────────────────
    @classmethod
    def plan(cls, envs: List[str], packages: List[str]) -> Dict[str, dict]:
        """
        • reverse‑merge env‑level YAML
        • emit per‑package config.json + backend config.hcl
        • run terraform to create a binary plan
        • copy that plan into   packages/<pkg>/latest/plan/<env>.tfplan
        • return {env: {package_key: cfg, …}, …}
        """
        from shutil import copy2

        combined: Dict[str, dict] = {}

        pkg_root = Path("packages")
        if not pkg_root.is_dir():
            raise FileNotFoundError("packages/ dir not found")

        wanted_pkgs = (
            [p.strip() for p in packages]
            if packages
            else [d.name for d in pkg_root.iterdir() if d.is_dir()]
        )

        pkg_keys: Dict[str, str] = {}
        for pkg in wanted_pkgs:
            key = cls._package_key(pkg_root / pkg)  # exactly one call
            if key:  # only keep packages that
                pkg_keys[pkg] = key
                combined: Dict[str, dict] = {}

        def fetch(blob: dict, key: str) -> dict:
            alt = key.replace("-", "_") if "-" in key else key.replace("_", "-")
            for k in (key, alt, f"{key}_map", f"{alt}_map"):
                if k in blob:
                    return blob[k]
            return {}

        for env in envs:
            env_dir = Path("configs") / env
            if not env_dir.is_dir():
                print(f"⚠️  No config dir for {env}: {env_dir}")
                continue

            # 1️⃣ merge YAML
            merged: dict = {}
            for yml in sorted(env_dir.glob("*.yml")):
                merged = cls._deep_merge(merged, yaml.safe_load(yml.read_text()) or {})

            # 2️⃣ per‑package
            env_result: Dict[str, dict] = {}
            for pkg, key in pkg_keys.items():
                cfg = fetch(merged, key)
                env_result[key] = cfg

                pkg_cfg_dir = pkg_root / pkg / "configs" / env
                pkg_cfg_dir.mkdir(parents=True, exist_ok=True)

                json_path = pkg_cfg_dir / "config.json"
                json_path.write_text(json.dumps(cfg, indent=2))
                cls._write_backend_hcl(pkg_root / pkg, env, key)

                if not cfg:  # nothing to plan
                    print(f"⚠️  nothing found for “{key}” in {env}")
                    continue

                # 3️⃣ terraform
                src_dir = pkg_root / pkg / "src"
                backend_cfg = pkg_cfg_dir / "config.hcl"
                plan_path = pkg_cfg_dir / f"{env}.tfplan"

                try:
                    cls.sh(
                        f"terraform -chdir={src_dir} init -input=false "
                        f"-backend-config={backend_cfg}"
                    )
                    cls.sh(
                        f"terraform -chdir={src_dir} plan -input=false "
                        f"-var-file={json_path} -out={plan_path}"
                    )
                    print(f"🔍  {pkg}/{env}: plan -> {plan_path}")
                except subprocess.CalledProcessError as exc:
                    print(f"❌  terraform failed for {pkg}/{env}\n{exc.output}")
                    continue  # move on to next package

                # 4️⃣ copy “latest” – overwriting any previous one
                latest_dir = pkg_root / pkg / "latest" / "plan"
                latest_dir.mkdir(parents=True, exist_ok=True)
                copy_target = latest_dir / f"{env}.tfplan"
                copy2(plan_path, copy_target)
                print(f"📂  latest/plan updated → {copy_target}")
                combined[env] = env_result
                print(f"\n[PLAN:{env}] merged {len(list(env_dir.glob('*.yml')))} files")

        return combined

    # ─────────────────────────── APPLY (stub) ─────────────────────────
    @classmethod
    def apply(cls, envs: list, packages: list) -> None:
        for env in envs:
            print(f"[APPLY] {env}")
            for pkg in packages:
                print(f"  • applying {pkg} …")
                time.sleep(0.05)  # stub
            print(f"[APPLY] {env} ✅\n")
