from __future__ import annotations

"""Shared runtime environment profiler for all codingStandard domains."""

import json
import os
import platform
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

STANDARD_VERSION = "1.17.2"


@dataclass(frozen=True)
class EnvironmentProfile:
    standard_version: str
    os: str
    architecture: str
    python: str
    executable: str
    ide: str
    execution_environment: str
    execution_type: str
    jupyter: bool
    colab: bool
    cpu_count: int | None
    ram_total_gb: float | None
    ram_available_gb: float | None
    disk_total_gb: float | None
    disk_free_gb: float | None
    accelerator_vendor: str | None
    accelerator_name: str | None
    vram_total_gb: float | None
    vram_free_gb: float | None
    cuda_available: bool
    cuda_version: str | None
    rocm_available: bool
    mps_available: bool
    directml_available: bool
    fp16_supported: bool
    bf16_supported: bool
    device: str
    recommended_batch_size: int
    recommended_gradient_accumulation_steps: int
    recommended_num_workers: int
    recommended_pin_memory: bool
    recommended_mixed_precision: str
    recommended_gradient_checkpointing: bool
    recommended_max_seq_length: int
    profile: str


def _is_colab() -> bool:
    env = os.environ
    return bool(env.get("COLAB_RELEASE_TAG") or env.get("COLAB_GPU") or "google.colab" in sys.modules)


def _detect_ide() -> str:
    env = os.environ
    if _is_colab(): return "colab"
    if env.get("VSCODE_PID") or env.get("TERM_PROGRAM") == "vscode": return "vscode"
    if "JPY_PARENT_PID" in env or "ipykernel" in sys.modules: return "jupyter"
    if env.get("JETBRAINS_IDE"): return "jetbrains"
    return "unknown"


def _ram_info() -> tuple[float | None, float | None]:
    try:
        import psutil
        m = psutil.virtual_memory()
        return round(m.total / 1024**3, 2), round(m.available / 1024**3, 2)
    except ImportError: return None, None


def _disk_info() -> tuple[float | None, float | None]:
    try:
        u = shutil.disk_usage(Path.cwd())
        return round(u.total / 1024**3, 2), round(u.free / 1024**3, 2)
    except OSError: return None, None


def _detect_accelerator() -> dict[str, Any]:
    result: dict[str, Any] = {"vendor": None, "name": None, "vram_total_gb": None, "vram_free_gb": None, "cuda": False, "cuda_version": None, "rocm": False, "mps": False, "directml": False, "fp16": False, "bf16": False}
    try:
        import torch
        result["rocm"] = bool(getattr(torch.version, "hip", None))
        result["cuda"] = bool(torch.cuda.is_available())
        result["cuda_version"] = getattr(torch.version, "cuda", None)
        if result["cuda"]:
            free, total = torch.cuda.mem_get_info()
            result["vram_total_gb"] = round(total / 1024**3, 2); result["vram_free_gb"] = round(free / 1024**3, 2)
            result["name"] = torch.cuda.get_device_name(0); result["vendor"] = "amd" if result["rocm"] else "nvidia"
            major, minor = torch.cuda.get_device_capability(0); cap = major + minor / 10
            result["fp16"] = cap >= 5.3; result["bf16"] = cap >= 8.0
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available(): result["mps"] = True; result["vendor"] = "apple"
    except (ImportError, RuntimeError, AttributeError): pass
    try:
        import torch_directml  # type: ignore
        result["directml"] = True; result["vendor"] = result["vendor"] or "directml"
    except ImportError: pass
    return result


def _resolve_device(a: dict[str, Any]) -> str:
    if a["cuda"]: return "cuda"
    if a["mps"]: return "mps"
    if a["directml"]: return "directml"
    return "cpu"


def _resolve_runtime(device: str, ram: float | None, vram: float | None, fp16: bool, bf16: bool, cpu_count: int | None) -> dict[str, Any]:
    available_ram, available_vram = ram or 0.0, vram or 0.0
    if device == "cuda":
        if available_vram <= 2.5: batch, accum, seq = 1, 16, 128
        elif available_vram <= 4.5: batch, accum, seq = 1, 8, 256
        elif available_vram <= 8.5: batch, accum, seq = 2, 4, 512
        else: batch, accum, seq = 4, 2, 512
        precision = "bf16" if bf16 else "fp16" if fp16 else "fp32"; checkpointing = available_vram <= 8.5; pin_memory = available_ram >= 4.0
    elif device in {"mps", "directml"}:
        batch, accum, seq = 1, 8, 256; precision = "fp16" if fp16 else "fp32"; checkpointing, pin_memory = True, False
    else:
        batch, accum, seq = 1, 8, 128; precision = "fp32"; checkpointing, pin_memory = False, False
    workers = 0 if available_ram and available_ram < 8 else min(4, cpu_count or 1)
    if available_ram and available_ram < 4: workers, accum = 0, max(accum, 16)
    return {"batch": batch, "accum": accum, "workers": workers, "pin_memory": pin_memory, "precision": precision, "checkpointing": checkpointing, "seq": seq}


def _profile_name(device: str, vram: float | None, ram: float | None, disk: float | None) -> str:
    if device != "cpu" and vram is not None and vram <= 4.5: return "accelerated-constrained"
    if device != "cpu" and vram is not None and vram <= 8.5: return "accelerated-limited"
    if ram is not None and ram <= 16: return "limited-system-memory"
    if disk is not None and disk <= 20: return "limited-disk-space"
    return f"{device}-standard"


def inspect_environment() -> EnvironmentProfile:
    ram_total, ram_available = _ram_info(); disk_total, disk_free = _disk_info(); acc = _detect_accelerator(); device = _resolve_device(acc)
    runtime = _resolve_runtime(device, ram_available, acc["vram_free_gb"], acc["fp16"], acc["bf16"], os.cpu_count())
    colab = _is_colab(); jupyter = "ipykernel" in sys.modules; ide = _detect_ide()
    if colab: execution_environment, execution_type = "colab", "cloud"
    elif jupyter: execution_environment, execution_type = "jupyter", "local"
    elif ide == "vscode": execution_environment, execution_type = "vscode", "local"
    else: execution_environment, execution_type = "local", "local"
    return EnvironmentProfile(standard_version=STANDARD_VERSION, os=platform.system(), architecture=platform.machine(), python=platform.python_version(), executable=sys.executable, ide=ide, execution_environment=execution_environment, execution_type=execution_type, jupyter=jupyter, colab=colab, cpu_count=os.cpu_count(), ram_total_gb=ram_total, ram_available_gb=ram_available, disk_total_gb=disk_total, disk_free_gb=disk_free, accelerator_vendor=acc["vendor"], accelerator_name=acc["name"], vram_total_gb=acc["vram_total_gb"], vram_free_gb=acc["vram_free_gb"], cuda_available=acc["cuda"], cuda_version=acc["cuda_version"], rocm_available=acc["rocm"], mps_available=acc["mps"], directml_available=acc["directml"], fp16_supported=acc["fp16"], bf16_supported=acc["bf16"], device=device, recommended_batch_size=runtime["batch"], recommended_gradient_accumulation_steps=runtime["accum"], recommended_num_workers=runtime["workers"], recommended_pin_memory=runtime["pin_memory"], recommended_mixed_precision=runtime["precision"], recommended_gradient_checkpointing=runtime["checkpointing"], recommended_max_seq_length=runtime["seq"], profile=_profile_name(device, acc["vram_total_gb"], ram_total, disk_free))


def to_runtime_config(profile: EnvironmentProfile) -> dict[str, Any]:
    return {"standard_version": profile.standard_version, "device": profile.device, "batch_size": profile.recommended_batch_size, "gradient_accumulation_steps": profile.recommended_gradient_accumulation_steps, "num_workers": profile.recommended_num_workers, "pin_memory": profile.recommended_pin_memory, "mixed_precision": profile.recommended_mixed_precision, "gradient_checkpointing": profile.recommended_gradient_checkpointing, "max_seq_length": profile.recommended_max_seq_length}


def save_profile(profile: EnvironmentProfile, path: str | Path) -> None:
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps({"environment": asdict(profile), "runtime": to_runtime_config(profile)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def print_profile(profile: EnvironmentProfile) -> None:
    print("=== Environment Profile ===")
    for k, v in asdict(profile).items(): print(f"{k}: {v}")
    print("=== Recommended Runtime Config ===")
    for k, v in to_runtime_config(profile).items(): print(f"{k}: {v}")


if __name__ == "__main__":
    profile = inspect_environment(); print_profile(profile)
    if len(sys.argv) == 2: save_profile(profile, sys.argv[1]); print(f"Saved profile: {sys.argv[1]}")
