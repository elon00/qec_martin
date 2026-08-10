#!/usr/bin/env python3
"""
Comprehensive auto-fix script for qec_martin repository.
Run from the repository ROOT (same level as .git/ and quantum_ecc_add/)
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path.cwd()
QEC_DIR = REPO_ROOT / "quantum_ecc_add"
SRC_DIR = QEC_DIR / "src"
BIN_DIR = SRC_DIR / "bin"

def run(cmd, cwd=None):
    """Run a shell command."""
    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd or QEC_DIR, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(result.stderr, file=sys.stderr)
    return result

def fix_cargo_toml():
    """Fix Cargo.toml: remove duplicate [[bin]], add missing binaries."""
    cargo_path = QEC_DIR / "Cargo.toml"
    if not cargo_path.exists():
        print(f"  ✗ {cargo_path} not found")
        return

    content = cargo_path.read_text(encoding="utf-8")

    # Remove duplicate [[bin]] section for superfast_encryption
    content = re.sub(
        r"\[\[bin\]\]\s*\n\s*name\s*=\s*\"superfast_encryption\"\s*\n\s*path\s*=\s*\"Superfast_Encryption\.rs\"",
        "",
        content,
        count=1,
    )
    # Clean up extra blank lines
    content = re.sub(r"\n{3,}", "\n\n", content)

    # Add missing bin declarations for files in src/bin/
    bin_files = list(BIN_DIR.glob("*.rs")) if BIN_DIR.exists() else []
    for bf in bin_files:
        name = bf.stem
        if name not in content:
            print(f"  → Adding missing binary: {name}")
            content += f"\n[[bin]]\nname = \"{name}\"\npath = \"src/bin/{bf.name}\"\n"

    # Also check if lwe_encryption.rs and message.rs exist in src/ (not in bin/)
    for src_file in ["lwe_encryption.rs", "message.rs"]:
        src_path = SRC_DIR / src_file
        if src_path.exists():
            txt = src_path.read_text(encoding="utf-8")
            if "fn main()" in txt:
                name = src_file.replace(".rs", "")
                if name not in content:
                    print(f"  → Adding binary declaration for src/{src_file}")
                    content += f"\n[[bin]]\nname = \"{name}\"\npath = \"src/{src_file}\"\n"

    cargo_path.write_text(content, encoding="utf-8")
    print(f"  ✓ Fixed {cargo_path}")

def fix_circuit_rs():
    """Fix circuit.rs: remove unused import, fix parse_u64_below_max."""
    path = SRC_DIR / "circuit.rs"
    if not path.exists():
        return

    content = path.read_text(encoding="utf-8")

    # Remove unused ParseIntError import
    content = content.replace("use std::num::ParseIntError;\n", "")

    # Fix parse_u64_below_max - replace entire function
    old_func = """fn parse_u64_below_max(s: &str) -> Result {
 let result: u64 = s.parse().unwrap();
 if result == u64::MAX {
 return Err("".parse::().unwrap_err());
 }
 return Ok(result);
}"""
    new_func = """fn parse_u64_below_max(s: &str) -> Result<u64, &'static str> {
    let result: u64 = s.parse().map_err(|_| "invalid integer")?;
    if result == u64::MAX {
        return Err("value must be below u64::MAX");
    }
    Ok(result)
}"""

    if old_func in content:
        content = content.replace(old_func, new_func)
    else:
        # Try looser match
        content = re.sub(
            r"fn parse_u64_below_max\(s: &str\) -> Result \{[^\}]+\}",
            new_func,
            content,
            flags=re.DOTALL,
        )

    # Ensure trailing newline
    if not content.endswith("\n"):
        content += "\n"

    path.write_text(content, encoding="utf-8")
    print(f"  ✓ Fixed {path}")

def fix_lwe_encryption_rs():
    """Fix lwe_encryption.rs: println formatting."""
    path = SRC_DIR / "lwe_encryption.rs"
    if not path.exists():
        return

    content = path.read_text(encoding="utf-8")

    # Fix println!("\nRaw decryption...") → separate println!() + println!("Raw...")
    content = content.replace(
        'println!("\\nRaw decryption result: {}", decrypted_val);',
        'println!();\n    println!("Raw decryption result: {}", decrypted_val);'
    )

    if not content.endswith("\n"):
        content += "\n"

    path.write_text(content, encoding="utf-8")
    print(f"  ✓ Fixed {path}")

def ensure_trailing_newline(filename):
    """Ensure a file ends with a newline."""
    path = SRC_DIR / filename
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    if not content.endswith("\n"):
        content += "\n"
        path.write_text(content, encoding="utf-8")
        print(f"  ✓ Fixed trailing newline in {path}")

def run_cargo_fmt():
    """Run cargo fmt if available."""
    result = run(["cargo", "fmt", "--all"])
    if result.returncode == 0:
        print("  ✓ cargo fmt completed")
    else:
        print("  ⚠ cargo fmt failed or not available")

def run_cargo_clippy_fix():
    """Run cargo clippy --fix if available."""
    result = run(["cargo", "clippy", "--all-targets", "--all-features", "--fix", "--allow-dirty", "--allow-staged"])
    if result.returncode == 0:
        print("  ✓ cargo clippy --fix completed")
    else:
        print("  ⚠ cargo clippy --fix failed or not available")

def main():
    print("=" * 60)
    print("  qec_martin Auto-Fix Script")
    print("=" * 60)

    if not QEC_DIR.exists():
        print(f"\n✗ Error: {QEC_DIR} not found. Run this from the repo root.")
        sys.exit(1)

    print("\n📦 Fixing Cargo.toml...")
    fix_cargo_toml()

    print("\n🔧 Fixing source files...")
    fix_circuit_rs()
    fix_lwe_encryption_rs()
    for f in ["lib.rs", "main.rs", "sim.rs", "weierstrass_elliptic_curve.rs", "message.rs"]:
        ensure_trailing_newline(f)
    # Also fix Superfast_Encryption.rs in root of quantum_ecc_add
    p = QEC_DIR / "Superfast_Encryption.rs"
    if p.exists():
        c = p.read_text(encoding="utf-8")
        if not c.endswith("\n"):
            c += "\n"
            p.write_text(c, encoding="utf-8")
            print(f"  ✓ Fixed trailing newline in {p}")

    print("\n🎨 Running cargo fmt...")
    run_cargo_fmt()

    print("\n🔍 Running cargo clippy --fix...")
    run_cargo_clippy_fix()

    print("\n" + "=" * 60)
    print("  Done! Review changes and commit:")
    print("  git add -A && git commit -m \"chore: auto-fix all linting and formatting issues\" && git push")
    print("=" * 60)

if __name__ == "__main__":
    main()