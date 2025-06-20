import csv
import re
import os
import subprocess
from datetime import datetime
import time
from serial.tools import list_ports
import unicodedata


def find_meshtastic_port():
    ports = list_ports.comports()
    for port in ports:
        if "Silicon Labs" in port.description or "USB" in port.description or "CP210" in port.description:
            print(f"✅ Found device on port: {port.device}")
            return port.device
    print("⚠️ No Meshtastic-compatible device found.")
    return None


def get_meshtastic_output():
    port = find_meshtastic_port()
    if not port:
        return ""

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
        print("❌ Failed to run 'meshtastic --nodes':", e)
        with open("meshtastic_raw_output.txt", "w", encoding='utf-8', errors='replace') as f:
            f.write("STDOUT:\n")
            f.write(e.stdout or "")
            f.write("\n\nSTDERR:\n")
            f.write(e.stderr or "")
        print("⚠️ Raw output written to meshtastic_raw_output.txt for inspection.")
        return ""


def clean_text(text):
    """Cleans text for CSV output by removing emojis, degree symbols, and unprintable characters."""
    if not isinstance(text, str):
        return text

    # Normalize Unicode
    text = unicodedata.normalize('NFKD', text)

    # Remove degree symbol and non-breaking space
    text = text.replace('°', '')
    text = text.replace('\u00A0', ' ')

    # Remove control characters (invisible junk)
    text = ''.join(c for c in text if not unicodedata.category(c).startswith('C'))

    # Remove any character that isn't basic ASCII (optional, aggressive filter)
    text = ''.join(c for c in text if 32 <= ord(c) <= 126)

    return text.strip()


def parse_meshtastic_table(output):
    lines = output.strip().splitlines()
    data_lines = [line for line in lines if re.match(r'^\s*│', line)]

    if not data_lines:
        print("⚠️ No data lines found in output.")
        return []

    header_line = data_lines[0]
    headers = [col.strip() for col in header_line.split('│') if col.strip()]

    timestamp_now = datetime.now().date().isoformat()
    rows = []

    for line in data_lines[1:]:
        columns = [col.strip() for col in line.split('│') if col.strip()]
        if len(columns) == len(headers):
            row = dict(zip(headers, columns))

            lat = row.get('Latitude', '')
            lon = row.get('Longitude', '')
            coords_raw = f"{lat} {lon}" if lat and lon else ''
            coords = clean_text(coords_raw)

            last_heard_raw = row.get('LastHeard', '')
            last_heard_date = ''
            if last_heard_raw:
                try:
                    dt = datetime.strptime(last_heard_raw, "%Y-%m-%d %H:%M:%S")
                    last_heard_date = dt.date().isoformat()
                except ValueError:
                    last_heard_date = last_heard_raw

            clean_row = {
                'Timestamp': timestamp_now,
                'Hardware Model': row.get('Hardware', ''),
                'Long Name': row.get('User', ''),
                'Short Name': row.get('AKA', ''),
                'User ID': row.get('ID', '')[-4:],
                'Role': row.get('Role', ''),
                'Position': coords,
                'Battery': row.get('Battery', ''),
                'Channel util.': row.get('Channel util.', ''),
                'Tx air util.': row.get('Tx air util.', ''),
                'SNR': row.get('SNR', ''),
                'Hops': row.get('Hops', ''),
                'LastHeard': last_heard_date
            }

            rows.append(clean_row)
        else:
            print(f"⚠️ Skipping malformed row: {line.encode('utf-8', errors='replace').decode('utf-8')}")

    return rows


def write_csv(rows, filename='nodes.csv'):
    fieldnames = [
        'Timestamp',
        'Hardware Model',
        'Long Name',
        'Short Name',
        'User ID',
        'Role',
        'Position',
        'Battery',
        'Channel util.',
        'Tx air util.',
        'SNR',
        'Hops',
        'LastHeard'
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            cleaned_row = {k: clean_text(v) for k, v in row.items()}
            writer.writerow(cleaned_row)
    print(f"✅ CSV written to '{filename}' with {len(rows)} rows.")


def main():
    while True:
        print("\n🚀 Starting Meshtastic node export...\n")
        raw_output = get_meshtastic_output()
        if raw_output:
            rows = parse_meshtastic_table(raw_output)
            if rows:
                write_csv(rows)
            else:
                print("⚠️ No valid rows to write to CSV.")
        else:
            print("⚠️ No output from meshtastic to process.")

        print("\n✅ Export complete. Program Termination in 3 seconds...")
        time.sleep(3)
        print("👋 Program Terminated. Goodbye!")
        break


if __name__ == "__main__":
    main()
