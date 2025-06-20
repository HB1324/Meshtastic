# 📡 Meshtastic Node Export

This Python utility connects to a Meshtastic device, extracts node information using the `meshtastic --nodes` command, cleans and structures the data, and outputs a clean `nodes.csv` file — ready for Excel or Google Sheets.

---

## 🚀 Features

- Automatically detects connected Meshtastic devices
- Parses and cleans terminal table output
- Generates spreadsheet-friendly CSV files
- Cleans special characters and extra spaces
- Displays friendly status icons (✅ ⚠️ ❌)
- Auto-exits 3 seconds after execution

---

## 🧰 Requirements

- Python 3.7+
- [Meshtastic Python CLI](https://meshtastic.org/docs/software/python/cli/)
- PySerial (`pyserial`)
- See "[Setup Requirements](https://github.com/HB1324/Meshtastic/tree/main/Setup%20Requirements)" for automated installations

Install the required Python packages:

```
pip install pyserial meshtastic
```

---

## 🖥️ How to Use

### 🔸 Option 1: Double-click to run
- Simply **double-tap `export_node.py`** from File Explorer.
- A terminal window will open, run the program, and close automatically after 3 seconds.

### 🔸 Option 2: Run from Command Prompt
1. Open the folder containing `export_node.py` in Command Prompt.
2. Run the script with:
```
py export_node.py
  ```

---

## 📄 Output

The script creates a file named `nodes.csv` in the same folder. It includes:

| Column           | Description                          |
|------------------|--------------------------------------|
| Timestamp        | Date of export                       |
| Hardware Model   | Device model (e.g. T-Beam)           |
| Long Name        | User-defined node name               |
| Short Name       | Short alias (AKA)                    |
| User ID          | Last 4 characters of node ID         |
| Role             | Node role (e.g. Client, Router)      |
| Position         | Latitude and Longitude               |
| Battery          | Battery voltage or status            |
| Channel util.    | Channel usage                        |
| Tx air util.     | Transmission utilization             |
| SNR              | Signal-to-noise ratio                |
| Hops             | Number of hops away                  |
| LastHeard        | Last date the node was heard         |

---

## 🛠️ Troubleshooting

- Ensure your device is connected and recognized as a USB or Silicon Labs device.
- You can test your device with:
  ```
  meshtastic --nodes
  ```
- If the script fails, a log file named `meshtastic_raw_output.txt` will be created with debug info.
- Make sure required USB drivers (e.g., CP210x) are installed.

---

## 📬 Questions or Feedback?

Suggestions and contributions are welcome! Feel free to open an issue or submit a pull request.

---

© 2025 • Powered by Meshtastic, Python, and a little ✨ CLI magic
