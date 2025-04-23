def install():
    print("✅ Running Pupdater install logic...")
    # hier roep je de echte installer aan
    from pupdater.install import install_pupdater
    install_pupdater.main()
