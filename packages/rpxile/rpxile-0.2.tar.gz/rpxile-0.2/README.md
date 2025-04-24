# 📦 rpxile  
**A simple Python library for fast and interactive file operations!**  

[![PyPI Version](https://img.shields.io/pypi/v/rpxile)](https://pypi.org/project/rpxile)  
[![GitHub Profile](https://img.shields.io/badge/GitHub-Rp--ics-blue?logo=github)](https://github.com/Rp-ics)  

---

## 🚀 Installation  
```bash
pip install rpxile

📚 Quick Start

from rpxile import fileutils

# Create a file (if it doesn't exist)
fileutils.create_file("notes.txt")  

# Overwrite content (interactive prompt)
fileutils.overwrite_file("notes.txt")  

# Append text (auto-adds \n if needed)
fileutils.append_file("notes.txt")  

# Read content
print(fileutils.read_file("notes.txt"))

🔧 Features

✔ Interactive mode – Guided CLI prompts for easy file handling.
✔ Lightweight – No external dependencies.
✔ Safety checks – Avoids silent errors (e.g., missing files).

⚠ Note: Uses input() for prompts—best for CLI tools, not automation.

🛠️ Roadmap

-Directory & batch operations

-JSON/XML/YAML support

-Non-interactive mode for scripts

📜 License

MIT

















