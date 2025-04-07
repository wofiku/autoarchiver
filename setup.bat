@echo Now compiling AutoArchiver (password and passwordless)
pyinstaller --add-binary="7z.exe;." --onefile autoarchiver_passworded.py
pyinstaller --add-binary="7z.exe;." --onefile autoarchiver.py

@echo Copying compiled files to the main path
move dist\* .

@echo Removing leftovers
del autoarchiver_passworded.spec /Q /S
del autoarchiver.spec /Q /S
rd .\dist /s /q
rd .\build /s /q

@echo Done compiling
@pause
