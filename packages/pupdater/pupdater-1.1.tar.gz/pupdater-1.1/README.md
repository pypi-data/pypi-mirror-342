# 🐾 Pupdater – Pip Manager for Django Admin

**Pupdater** is a pluggable Django admin app that allows you to view, check, and manage installed Python packages directly from the Django admin interface.

## 🚀 Features

- View all installed packages with metadata
- Highlight outdated versions automatically
- Upgrade packages with one click (superuser-only)
- Create snapshots of your environment and compare them
- Export data to JSON, CSV, TXT, or XLSX
- Compare two snapshots side-by-side
- Compare `pip freeze` output to `requirements.txt`
- Optional Jazzmin integration – works standalone as well

---

## 🧪 Installation

1. Install Pupdater via GitHub:

```bash
pip install git+https://github.com/WilkoRi/pupdater.git
```

2. Run the installer script to automatically add Pupdater to your `INSTALLED_APPS` and `urls.py`:

```bash
install_pupdater
```

🖐️ This will auto-detect your `settings.py` and `urls.py` and add the required config.

---

## 📂 Screenshots

**Dashboard**
- View installed packages, their status, and metadata
- One-click upgrade per package
- Save snapshots of current state

**Compare**
- Snapshot vs snapshot
- `pip freeze` vs `requirements.txt`

---

## ⚙️ Compatibility

- Python 3.8+
- Django 3.2+
- pip
- (Optional) Jazzmin

---

## 📄 Export Formats

- JSON, CSV, TXT, XLSX
- For pip freeze, snapshots, and comparisons

---

## ⚠️ Notes

- Only Django superusers can perform package upgrades
- Export your environment as backup or for reproducibility


© Wilko Rietveld – BSD-3-Clause License

