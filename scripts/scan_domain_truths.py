import os
import re

# 📁 Folder containing all domain truth scrolls
DOMAIN_FOLDER = "domains"

# 🔍 Patterns to detect key signals
STATUS_PATTERN = r"\*\*Status\*\*: (.+)"
COMPANION_TAG_PATTERN = r"<!-- Companion Thread: (.+) -->"

# 🧭 Section headers to scan for fidelity
SECTION_HEADERS = [
    "Core Axioms",
    "Emotional Fidelity Signals",
    "Drift Detection Flags",
    "Entry Rituals",
    "Licensing and Adaptation Notes"
]

def scan_scroll(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    results = {}
    results["filename"] = os.path.basename(file_path)

    # 🧵 Companion Thread tag
    companion_match = re.search(COMPANION_TAG_PATTERN, content)
    results["companion_tag"] = bool(companion_match)

    # 📌 Status line
    status_match = re.search(STATUS_PATTERN, content)
    results["status"] = status_match.group(1).strip() if status_match else "Unknown"

    # 🔹 Section presence
    for header in SECTION_HEADERS:
        results[header] = header in content

    return results

def scan_all_scrolls():
    print("🧠 DreamWeaver Autolearn Scan Report\n")
    for filename in sorted(os.listdir(DOMAIN_FOLDER)):
        if filename.endswith(".md"):
            path = os.path.join(DOMAIN_FOLDER, filename)
            result = scan_scroll(path)
            print(f"📜 {result['filename']}")
            print(f"   ✅ Companion Tag: {'Yes' if result['companion_tag'] else 'No'}")
            print(f"   📌 Status: {result['status']}")
            for header in SECTION_HEADERS:
                print(f"   🔹 {header}: {'✅' if result[header] else '❌'}")
            print("")

if __name__ == "__main__":
    scan_all_scrolls()
