# qec_martin

A Rust-based implementation suite for **Quantum Error Correction (QEC)**, **Post-Quantum Cryptography (PQC)**, and **Lattice-Based Encryption** algorithms.

---

## 🚀 Executables & Modules

| Binary Target | Source Location | Description |
| :--- | :--- | :--- |
| `digital_signature` | `src/bin/digital_signature.rs` | Post-quantum digital signature generation and verification |
| `ecc_key_gen` | `src/bin/ecc_key_gen.rs` | Elliptic Curve Cryptography (ECC) key pair generator |
| `lattice_simulation` | `src/bin/lattice_simulation.rs` | Simulation framework for lattice-based cryptographic assumptions |
| `lwe_encryption` | `src/lwe_encryption.rs` | Learning With Errors (LWE) encryption scheme |
| `message` | `src/message.rs` | Secure quantum messaging and serialization protocol |

---

## 📋 Prerequisites

- **[Rust & Cargo](https://www.rust-lang.org/tools/install)** (Edition 2021)
- **[Python 3.x](https://www.python.org/downloads/)**

---

## 🛠️ Build & Run

```bash
cargo build --release
cargo run --bin lwe_encryption
```
