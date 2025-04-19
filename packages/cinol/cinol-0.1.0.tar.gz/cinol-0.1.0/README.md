# Cinol - Python Code Protection Toolkit

[![PyPI Version](https://img.shields.io/pypi/v/cinol)](https://pypi.org/project/cinol/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/cinol)](https://pypi.org/project/cinol/)

Cinol adalah toolkit Python untuk melindungi kode dari pembajakan dengan teknik:
- **Obfuskasi** (pengaburan kode)
- **Enkripsi Bytecode** (AES-256 + GCM)
- **Manajemen Lisensi** (RSA + Signature)
- **Proteksi Runtime** (anti-debug, checksum)

## 🔥 Fitur Utama

- **Obfuskasi AST** - Mengaburkan nama variabel/fungsi
- **Enkripsi Berlapis** - AES-256 untuk bytecode + RSA untuk lisensi
- **Validasi Lisensi** - Online/offline dengan signature digital
- **Self-Decrypting** - Eksekusi kode terenkripsi tanpa file sisa
- **Anti-Tampering** - Deteksi modifikasi kode

## 📦 Instalasi

```bash
pip install cinol
