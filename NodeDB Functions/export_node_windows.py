import csv
import os
import time
import subprocess
from datetime import datetime
from serial.tools import list_ports
import unicodedata


def find_all_meshtastic_ports():
    ports = list_ports.comports()
    matched_ports = []
    for port in ports:
        if "Silicon Labs" in port.description or "USB" in port.description or "CP210" in port.description:
            print(f"✅ Found device on port: {port.device}")
            matched_ports.append(port.device)
    if not matched_ports:
        print("⚠️ No Meshtastic-compatible devices found.")
    return matched_ports


def get_meshtastic_output(port):
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        result = subprocess.run(
            ["meshtastic", "--port", port, "--nodes"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=True,
            env=env
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to run 'meshtastic --nodes' on {port}:", e)
        with open(f"meshtastic_raw_output_{port.replace(':', '')}.txt", "w", encoding='utf-8', errors='replace') as f:
            f.write("STDOUT:\n")
            f.write(e.stdout or "")
            f.write("\n\nSTDERR:\n")
            f.write(e.stderr or "")
        print(f"⚠️ Raw output written to meshtastic_raw_output_{port}.txt for inspection.")
        return ""


def clean_text(text):
    if not isinstance(text, str):
        text = str(text)
    text = unicodedata.normalize('NFKD', text)
    text = text.replace('°', '')
    text = text.replace('\u00A0', ' ')
    text = ''.join(c for c in text if not unicodedata.category(c).startswith('C'))
    text = ''.join(c for c in text if 32 <= ord(c) <= 126)
    return text.strip()


def parse_meshtastic_table(output):
    lines = output.strip().splitlines()
    data_lines = [line for line in lines if line.strip().startswith('│')]

    # Locate the header line
    header_line = None
    for line in data_lines:
        if "User" in line and "ID" in line and "Role" in line:
            header_line = line
            break

    if not header_line:
        print("⚠️ Could not detect a valid header line.")
        return []

    header_cells = [col.strip() for col in header_line.split('│') if col.strip()]
    header_map = {name: idx for idx, name in enumerate(header_cells)}

    start_index = data_lines.index(header_line) + 1
    data_lines = data_lines[start_index:]

    rows = []
    timestamp_now = datetime.now().date().isoformat()

    for line in data_lines:
        if "╞" in line or len(line.strip()) == 0:
            continue

        data_cells = [col.strip() for col in line.split('│') if col.strip()]
        if len(data_cells) < len(header_cells):
            print(f"⚠️ Skipping malformed row (too few columns): {line}")
            continue

        # Trim any extra trailing columns (e.g., '2 days ago')
        data_cells = data_cells[:len(header_cells)]

        def get(col_name):
            idx = header_map.get(col_name)
            return data_cells[idx] if idx is not None and idx < len(data_cells) else ''

        lat = get('Latitude')
        lon = get('Longitude')
        coords = clean_text(f"{lat} {lon}" if lat and lon else '')

        last_heard_raw = get('LastHeard')
        last_heard_date = ''
        if last_heard_raw:
            try:
                dt = datetime.strptime(last_heard_raw, "%Y-%m-%d %H:%M:%S")
                last_heard_date = dt.date().isoformat()
            except ValueError:
                last_heard_date = last_heard_raw

        clean_row = {
            'Timestamp': timestamp_now,
            'Hardware Model': get('Hardware'),
            'Long Name': get('User'),
            'Short Name': get('AKA'),
            'User ID': get('ID')[-4:],
            'Role': get('Role'),
            'Position': coords,
            'Battery': get('Battery'),
            'Channel util.': get('Channel util.'),
            'Tx air util.': get('Tx air util.'),
            'SNR': get('SNR'),
            'Hops': get('Hops'),
            'LastHeard': last_heard_date
        }

        rows.append(clean_row)

    return rows


def wrap_for_excel_safe(value):
    val = clean_text(value)
    if val.replace('.', '', 1).isdigit() and len(val) > 8:
        return f'="{val}"'
    return val


def write_csv(rows, port, filename_prefix='nodes'):
    safe_port = port.replace(':', '').replace('/', '_')
    filename = f"{filename_prefix}_{safe_port}.csv"
    fieldnames = [
        'Timestamp', 'Hardware Model', 'Long Name', 'Short Name',
        'User ID', 'Role', 'Position', 'Battery',
        'Channel util.', 'Tx air util.', 'SNR', 'Hops', 'LastHeard'
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in rows:
            cleaned_row = {k: wrap_for_excel_safe(v) for k, v in row.items()}
            writer.writerow(cleaned_row)
    print(f"✅ CSV written to '{filename}' with {len(rows)} rows.")


def main():
    print("🔍 Scanning for all Meshtastic devices...")
    ports = find_all_meshtastic_ports()

    if not ports:
        print("🚫 No Meshtastic devices found. Program Termination in 3 seconds...")
        time.sleep(3)
        print("👋 Goodbye!")
        return

    for port in ports:
        print(f"\n🚀 Starting export for device on {port}...")
        raw_output = get_meshtastic_output(port)
        if raw_output:
            rows = parse_meshtastic_table(raw_output)
            if rows:
                write_csv(rows, port)
            else:
                print(f"⚠️ No valid rows to write from device {port}.")
        else:
            print(f"⚠️ No output from device {port} to process.")

    print("\n✅ All devices processed. Program Termination in 3 seconds...")
    time.sleep(3)
    print("👋 Goodbye!")


if __name__ == "__main__":
    main()
