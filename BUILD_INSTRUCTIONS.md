Windows build instructions for creating the executable with PyInstaller

Prerequisites
- Git
- Python 3.12 (recommended)
- Visual C++ Build Tools (for compiling some binary deps)

Steps
1. Create and activate a virtual environment (from project root):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # or Activate.bat on cmd
```

2. Install dependencies and PyInstaller:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install pyinstaller
```

3. Run PyInstaller with the included spec file:

```powershell
.\.venv\Scripts\python.exe -m PyInstaller replication_package.spec
```

4. The built application will be in `dist\replication_package_app`. The main executable is `replication_package_app.exe`.

Running the app
- Run `dist\replication_package_app\replication_package_app.exe` to start the Flask server.
- Open http://127.0.0.1:5000 in your browser.

Notes
- The build bundles the `templates`, `static`, `data`, `queries`, and `search` folders into the bundled application.
- If you add runtime-generated directories (e.g., `data_results` or `generated_images`) you may need to update the spec to include them or ensure they are created at runtime.
- To produce a single-file exe, adjust `replication_package.spec` flags (set `EXE(..., exclude_binaries=False, ... )` and other options) but expect larger build sizes and longer startup times.

If you want, I can run the bundled exe to verify it runs, but I will need permission to spawn it interactively on your machine.