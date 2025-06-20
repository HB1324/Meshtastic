readme_content = """
# ⚙️ Meshtastic Environment Setup Script

---

## ⚠️ Safety & Compatibility Notice

This batch script has been tested and is safe to use on supported Windows machines running Python 3.  
However, due to Windows security features, your PC may display warnings when running this program (such as **"Windows protected your PC"**).  
These warnings are standard safety measures from Microsoft to prevent unrecognized programs from running automatically.  
You can safely proceed by choosing **More info** and then **Run anyway** if you trust this source.

---

## 📋 What It Does

When executed, this batch file will:

1. ✅ Check your installed **Python version**  
2. ✅ Check your installed **pip3 version**  
3. 📦 Install or upgrade the `pytap2` library (used by Meshtastic tools)  
4. 📦 Install or upgrade the Meshtastic Python CLI (`meshtastic[cli]`)  
5. ⏸️ Pause at the end so you can review the results  

---

## ▶️ How to Use

1. Download the `setup_meshtastic_env.bat` file to your Windows machine.  
2. Right-click the file and choose **Run as administrator** (recommended).  
3. Follow the command prompt as it executes each step.  
4. Press any key to close the window when it says `Press any key to continue...`.  

---

## 🛠️ Prerequisites

- Ensure **Python 3** is installed on your system.  
  Download it here: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)  
- Make sure `pip3` is available in your system path (it comes bundled with Python).  
- Internet access is required for `pip3 install` steps.  

---

## 📁 Output

The script does not create files but ensures:  
- `pytap2` is installed and up to date  
- `meshtastic` CLI is installed with extras for communication  

After running the script, you can use the Meshtastic CLI, for example:  
```bash
meshtastic --nodes
