import os

def find_path(target_file):
    project_dir = os.getcwd()
    for subdir in os.listdir(project_dir):
        path = os.path.join(project_dir, subdir, target_file)
        if os.path.isfile(path):
            return path
    raise FileNotFoundError(f"❌ {target_file} not found.")

def update_settings(settings_path):
    with open(settings_path, "r") as f:
        lines = f.readlines()

    if any("'pupdater'" in line for line in lines):
        print("✅ 'pupdater' already in INSTALLED_APPS.")
        return

    for i, line in enumerate(lines):
        if line.strip().startswith("]") and "INSTALLED_APPS" in "".join(lines[max(0, i - 10):i]):
            lines.insert(i, "    'pupdater',\n")
            break

    with open(settings_path, "w") as f:
        f.writelines(lines)

    print("✅ 'pupdater' added to INSTALLED_APPS.")

def update_urls_force(urls_path):
    with open(urls_path, "r") as f:
        lines = f.readlines()

    start, end = None, None
    for i, line in enumerate(lines):
        if start is None and "urlpatterns" in line and "[" in line:
            start = i
        if start is not None and "]" in line:
            end = i
            break

    if start is not None and end is not None:
        for j in range(start, end):
            line = lines[j].strip()
            if not line.startswith("#") and "pupdater.urls" in line:
                print("✅ 'pupdater.urls' already found in urlpatterns block.")
                return

        for j in range(start, end + 1):
            if "]" in lines[j]:
                lines.insert(j, "    path('pupdater/', include('pupdater.urls')),  # ✅ required\n")
                break

        with open(urls_path, "w") as f:
            f.writelines(lines)

        print("✅ urls.py updated with pupdater route.")
    else:
        print("❌ urlpatterns block not found.")

def main():
    try:
        settings_path = find_path("settings.py")
        print(f"🎯 settings found at: {settings_path}")
        update_settings(settings_path)
    except FileNotFoundError as e:
        print(e)
        return

    try:
        urls_path = os.path.join(os.path.dirname(settings_path), "urls.py")
        if not os.path.isfile(urls_path):
            raise FileNotFoundError
        print(f"🎯 urls found at: {urls_path}")
        update_urls_force(urls_path)
    except FileNotFoundError:
        print("❌ matching urls.py not found next to settings.py")

if __name__ == "__main__":
    main()
