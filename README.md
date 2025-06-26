<p align="center">
  <img src="https://raw.githubusercontent.com/AbdulMods/Contacts-refine/main/assets/refiner_banner.gif" width="800" alt="Refiner Banner">
</p>

<h1 align="center">🔧 Refiner</h1>
<h2 align="center">Professional CSV to vCard Conversion Tool</h2>
<h3 align="center">Crafted by Abdul Qadeer Gabol</h3>

<div align="center">
  
[![PyPI](https://img.shields.io/badge/Python-3.8%2B-red?style=for-the-badge&logo=python)](https://python.org)
[![GitHub](https://img.shields.io/badge/Version-1.0.0-black?style=for-the-badge&logo=github)](https://github.com/AbdulMods/Contacts-refine/releases)
[![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)](LICENSE)

</div>

---

## 🚀 Features
- 📁 Automatic directory creation (Csv/Refined)
- ⚡ Batch processing of multiple CSV files
- 🌍 Worldwide phone number support
- 🔄 Sequential name generation (Trader 1, Trader 2)
- 📱 vCard 3.0 output with proper formatting
- 🎨 Colorful terminal interface with progress bars
- ⏱️ Processing time estimation
- 📊 Contact statistics reporting
- 💾 Backup system for output directory
- 🛡️ Educational purpose disclaimer

---

## 📦 Installation

### Auto Installer (Termux & Linux)
```bash
pkg install curl -y 2>/dev/null || sudo apt install curl -y && \
curl -sL https://raw.githubusercontent.com/AbdulMods/Contacts-refine/main/installation.sh -o installation.sh && \
bash installation.sh
```
### Manual Installation
```bash
# Step 1 - Clone Repository
git clone https://github.com/AbdulMods/Contacts-refine.git

# Step 2 - Navigate to Directory
cd Contacts-refine

# Step 3 - Run the Script
python3 Refine.py
```

---

## 📂 Directory Structure
```
/storage/emulated/0/
└── Qadeer/
    ├── Csv/          # Place your CSV files here
    └── Refined/      # Processed vCard files appear here
```

---

## 🖥️ Usage
After installation, simply run:
```bash
refine
```

You'll see a professional menu system:
```
=== ACCsi Forex Contact Refiner ===
1. Process Single CSV File
2. Batch Process All CSV Files
3. View Directory Info
4. Export Contact Statistics
5. Backup Directory
6. Exit
```

---

## ⚠️ Ethical Warning

> This tool is designed for EDUCATIONAL PURPOSES ONLY.  
> Do not use it for any unethical or illegal activities including:

- Spamming or unsolicited communication
- Contact list scraping without permission
- Any violation of privacy laws
- Misrepresentation of contact information

---

## 🧠 FAQ

<details>
  <summary><strong>What CSV format does Refiner accept?</strong></summary>
  Refiner processes CSV files with phone numbers in the first column. Example:
  <pre>+92 341 2022526,#account management,,Qadeer Forex</pre>
</details>

<details>
  <summary><strong>How are names generated?</strong></summary>
  Names are generated sequentially based on your input (e.g., "Trader 1", "Trader 2"). 
  The tool automatically skips existing numbers.
</details>

<details>
  <summary><strong>Can I process multiple files at once?</strong></summary>
  Yes! Use the "Batch Process All CSV Files" option to process all CSV files in the Csv directory.
</details>

<details>
  <summary><strong>Where are the output files saved?</strong></summary>
  Processed vCard files are saved in /storage/emulated/0/Qadeer/Refined/
</details>

<details>
  <summary><strong>How do I restore from backup?</strong></summary>
  Use the "Backup Directory" option to create backups. Restore by copying files from the backup directory.
</details>

---

## 🔄 Update Note – v1.0

📅 Date: 2025-06-28

### ✨ What's New
- ✅ Initial release of Refiner
- ✅ Complete CSV to vCard conversion pipeline
- ✅ Colorful terminal interface
- ✅ Batch processing capabilities
- ✅ Directory statistics and reporting

### 🛠️ Improvements
- 🧹 Optimized phone number cleaning
- ⚡ Faster processing algorithms
- 📱 Improved vCard compatibility
- 🌐 Better international number support

---

## 📞 Contact

<p align="center">
  <a href="https://t.me/TradeWithQadeer">
    <img src="https://img.shields.io/badge/Telegram-@TradeWithQadeer-blue?style=for-the-badge&logo=telegram">
  </a>
  <a href="mailto:aqbaloch6201@gmail.com">
    <img src="https://img.shields.io/badge/Email-Contact-red?style=for-the-badge&logo=gmail">
  </a>
</p>

<div align="center">
  <sub>Crafted with ❤️ by <a href="https://t.me/TradeWithQadeer">Abdul Qadeer Gabol</a></sub>
</div>
```
