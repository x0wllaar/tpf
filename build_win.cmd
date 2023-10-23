rd /s /q build
rd /s /q dist
del /s /q *.spec

pyinstaller --onefile --console --clean --name tpf --paths . --hiddenimport _cffi_backend .\main.py