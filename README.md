# MP3 LSB Steganography (Educational Research)

**Repository:** [Mp3-Reverse-Shell](https://github.com/SleepTheGod/Mp3-Reverse-Shell)  
**Files:** `main.py`, `requirements.txt`  

---

## Overview

This project demonstrates how **Least Significant Bit (LSB) steganography** can be applied to MP3 files for embedding and extracting hidden data.  
It is intended for **educational purposes only**, specifically to support:

- Academic research on steganography in non-image media  
- Security training in controlled labs  
- Defensive research for intrusion detection and forensic workflows  

⚠️ **Disclaimer:**  
This repository is for **authorized red-team labs and academic research only**.  
Do **not** use this code against systems or data without **explicit written permission**. Unauthorized use may be illegal.

---

## Features

- Embed arbitrary payloads into MP3 files using LSB manipulation  
- Extract embedded payloads from MP3 files  
- Example payload generator for demonstration  
- Basic error handling and validation  

---

## Requirements

- Python 3.8+  
- Standard library modules (`os`, `socket`, `struct`, `glob`, `base64`)  

Install requirements:

```bash
pip install -r requirements.txt
```
