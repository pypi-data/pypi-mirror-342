# pupdater/cli/entrypoint.py

import sys

def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "config" and sys.argv[2] == "install":
        print("🚀 Running install_pupdater from CLI...")

        try:
            from pupdater.install import install_pupdater
            install_pupdater.main()
        except Exception as e:
            print(f"❌ Failed to run installer: {e}")
    else:
        print("ℹ️ Usage: pupdater config install")
