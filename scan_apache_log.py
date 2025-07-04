import re
import gzip
from pathlib import Path
from collections import defaultdict

LOG_DIR = "/var/log/apache2"
OUTPUT_FILE = str(Path.home() / "install_activity.md")

# Matches UUID and ?t time from URL
UUID_PATTERN = re.compile(r"user=([a-f0-9\-]{36})")
TIME_PATTERN = re.compile(r"[?&]t=([a-zA-Z0-9]+)")

def parse_log_file(path):
    open_func = gzip.open if str(path).endswith('.gz') else open
    with open_func(path, 'rt', errors='ignore') as f:
        for line in f:
            if "/dixels/newaicp.html" in line:
                uuid_match = UUID_PATTERN.search(line)
                time_match = TIME_PATTERN.search(line)
                ip_match = line.split(" ")[0]  # IP is the first item before the first space

                if uuid_match:
                    uuid = uuid_match.group(1)
                    time = time_match.group(1) if time_match else "unknown"
                    yield uuid, time, ip_match

def main():
    user_activity = defaultdict(lambda: {"count": 0, "records": []})

    for log_file in Path(LOG_DIR).glob("access.log*"):
        for uuid, t, ip in parse_log_file(log_file):
            user_activity[uuid]["count"] += 1
            user_activity[uuid]["records"].append((t, ip))

    # Write Markdown
    with open(OUTPUT_FILE, "w") as f:
        f.write("# Install Activity Report\n\n")
        for uuid, data in sorted(user_activity.items()):
            f.write(f"## {uuid}\n")
            f.write(f"- Seen: {data['count']} times\n")
            f.write("- Entries:\n")
            for t, ip in data["records"]:
                f.write(f"  - Time: `{t}`, IP: `{ip}`\n")
            f.write("\n")

    print(f"Updated {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
