bat_script_content = """@echo off
:: Publisher: CRY0NIX5018
:: Setup script for Meshtastic environment

echo Checking Python version...
py -V

echo ---

echo Checking pip3 version...
pip3 -V

echo ---
echo Installing/Upgrading pytap2...
pip3 install --upgrade pytap2

echo ---
echo Installing/Upgrading Meshtastic CLI...
pip3 install --upgrade "meshtastic[cli]"

echo ---
echo All steps completed.
pause
"""

bat_file_path = "/mnt/data/setup_meshtastic_env.bat"
with open(bat_file_path, "w", encoding="utf-8") as f:
    f.write(bat_script_content)

bat_file_path
