from __future__ import annotations

"""Runtime dependency contract and safe PyTorch bootstrap helpers."""

import importlib
import subprocess
import sys
from dataclasses import dataclass

PYTHON_MIN = (3, 10)
PYTHON_MAX_EXCLUSIVE = (3, 15)

# Supported stable PyTorch / torchvision version pairs.
TORCHVISION_PAIRS = {
    "2.10": "0.25",
    "2.11": "0.26",
    "2.12": "0.27",
    "2.13": "0.28",
}
DEFAULT_TORCH = "2.13.0"
DEFAULT_TORCHVISION = "0.28.0"


@dataclass(frozen=True)
class DependencyStatus:
    python_ok: bool
    torch_installed: bool
    torch_version: str | None
    torchvision_installed: bool
    torchvision_version: str | None
    compatible: bool


def check_python_version() -> None:
    version = sys.version_info[:2]
    if version < PYTHON_MIN or version >= PYTHON_MAX_EXCLUSIVE:
        raise RuntimeError(
            "AIEngineeringStandard 2.x requires Python 3.10-3.14; "
            f"detected Python {version[0]}.{version[1]}"
        )


def _module_version(name: str) -> str | None:
    try:
        module = importlib.import_module(name)
    except ImportError:
        return None
    return getattr(module, "__version__", None)


def _pair_is_compatible(torch_version: str | None, torchvision_version: str | None) -> bool:
    if not torch_version or not torchvision_version:
        return False
    torch_major_minor = ".".join(torch_version.split(".")[:2])
    torchvision_major_minor = ".".join(torchvision_version.split(".")[:2])
    return TORCHVISION_PAIRS.get(torch_major_minor) == torchvision_major_minor


def inspect_dependencies() -> DependencyStatus:
    check_python_version()
    torch_version = _module_version("torch")
    torchvision_version = _module_version("torchvision")
    return DependencyStatus(
        python_ok=True,
        torch_installed=torch_version is not None,
        torch_version=torch_version,
        torchvision_installed=torchvision_version is not None,
        torchvision_version=torchvision_version,
        compatible=_pair_is_compatible(torch_version, torchvision_version),
    )


def _pip_install(*packages: str) -> None:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", *packages],
        check=True,
    )


def ensure_pytorch(*, repair: bool = True) -> DependencyStatus:
    """Ensure a supported torch/torchvision pair exists.

    Existing compatible installations are preserved. Missing or incompatible
    installations are repaired with a known stable pair when ``repair`` is true.
    The installer intentionally uses the active interpreter's pip, which keeps
    Colab, venv, Jupyter, and local Python environments isolated.
    """
    status = inspect_dependencies()
    if status.compatible:
        return status
    if not repair:
        raise RuntimeError(
            "Unsupported PyTorch environment: "
            f"torch={status.torch_version!r}, torchvision={status.torchvision_version!r}"
        )

    _pip_install(f"torch=={DEFAULT_TORCH}", f"torchvision=={DEFAULT_TORCHVISION}")
    repaired = inspect_dependencies()
    if not repaired.compatible:
        raise RuntimeError(
            "PyTorch bootstrap completed but the resulting versions are incompatible: "
            f"torch={repaired.torch_version!r}, torchvision={repaired.torchvision_version!r}"
        )
    return repaired
