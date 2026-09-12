#!/usr/bin/env python3
"""Exercise a real pip resolver against an isolated local wheelhouse."""
from __future__ import annotations
import csv, hashlib, io, subprocess, sys, tempfile, unittest, zipfile
from pathlib import Path

def _wheel_bytes(name: str, version: str, requires: list[str] | None = None) -> bytes:
    normalized = name.replace("-", "_"); dist_info = f"{normalized}-{version}.dist-info"
    metadata = ["Metadata-Version: 2.1", f"Name: {name}", f"Version: {version}"]
    for requirement in requires or []: metadata.append(f"Requires-Dist: {requirement}")
    metadata_text = "\n".join(metadata) + "\n"
    wheel_text = "Wheel-Version: 1.0\nGenerator: codingstandard-test\nRoot-Is-Purelib: true\nTag: py3-none-any\n"
    files = {f"{normalized}/__init__.py": f"__version__ = {version!r}\n".encode(), f"{dist_info}/METADATA": metadata_text.encode(), f"{dist_info}/WHEEL": wheel_text.encode()}
    record_name = f"{dist_info}/RECORD"; record_rows = []
    for path, payload in files.items():
        digest = hashlib.sha256(payload).digest(); encoded = __import__("base64").urlsafe_b64encode(digest).rstrip(b"=").decode(); record_rows.append((path, f"sha256={encoded}", str(len(payload))))
    record_rows.append((record_name, "", "")); record_buffer = io.StringIO(); csv.writer(record_buffer, lineterminator="\n").writerows(record_rows); files[record_name] = record_buffer.getvalue().encode()
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path, payload in files.items(): archive.writestr(path, payload)
    return output.getvalue()

def _write_wheel(directory: Path, name: str, version: str, requires: list[str] | None = None) -> None:
    normalized = name.replace("-", "_"); (directory / f"{normalized}-{version}-py3-none-any.whl").write_bytes(_wheel_bytes(name, version, requires))

class PipDependencyResolverTests(unittest.TestCase):
    def test_selected_library_drives_affected_dependency_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            wheelhouse = Path(tmp); _write_wheel(wheelhouse, "compat-lib", "1.0.0"); _write_wheel(wheelhouse, "compat-lib", "2.0.0"); _write_wheel(wheelhouse, "anchor-lib", "2.0.0", ["compat-lib>=2.0.0"])
            completed = subprocess.run([sys.executable, "-m", "pip", "install", "--dry-run", "--ignore-installed", "--no-index", "--find-links", str(wheelhouse), "anchor-lib==2.0.0"], capture_output=True, text=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stderr); combined = completed.stdout + completed.stderr
            self.assertRegex(combined, r"anchor-lib-2\.0\.0"); self.assertRegex(combined, r"compat-lib-2\.0\.0"); self.assertNotRegex(combined, r"compat-lib-1\.0\.0")

    def test_real_pip_resolver_rejects_incompatible_pinned_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            wheelhouse = Path(tmp); _write_wheel(wheelhouse, "compat-lib", "1.0.0"); _write_wheel(wheelhouse, "compat-lib", "2.0.0"); _write_wheel(wheelhouse, "anchor-lib", "2.0.0", ["compat-lib>=2.0.0"])
            completed = subprocess.run([sys.executable, "-m", "pip", "install", "--dry-run", "--ignore-installed", "--no-index", "--find-links", str(wheelhouse), "anchor-lib==2.0.0", "compat-lib==1.0.0"], capture_output=True, text=True, check=False)
            self.assertNotEqual(completed.returncode, 0); self.assertRegex(completed.stderr + completed.stdout, r"(?i)(conflict|incompatible|resolutionimpossible|cannot install)")

if __name__ == "__main__": unittest.main()
