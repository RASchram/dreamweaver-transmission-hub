import os
import re
import json

# 📁 Folder containing all domain truth scrolls
DOMAIN_FOLDER = "domains"

# 📁 Output files
MARKDOWN_REPORT = "scan-report.md"
JSON_REPORT = "scan-report.json"

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

    # 🚀 Promotion readiness
    results["promotion_ready"] = (
        results["companion_tag"]
        and results["status"].lower() == "active"
        and all(results[header] for header in SECTION_HEADERS)
    )

    return results

def generate_markdown_report(results_list):
    with open(MARKDOWN_REPORT, "w", encoding="utf-8") as f:
        f.write("# 🧠 DreamWeaver Autolearn Scan Report\n\n")
        for result in results_list:
            f.write(f"## 📜 {result['filename']}\n")
            f.write(f"- ✅ Companion Tag: {'Yes' if result['companion_tag'] else 'No'}\n")
            f.write(f"- 📌 Status: {result['status']}\n")
            for header in SECTION_HEADERS:
                f.write(f"- 🔹 {header}: {'✅' if result[header] else '❌'}\n")
            f.write(f"- 🚀 Promotion Ready: {'✅' if result['promotion_ready'] else '❌'}\n\n")

def generate_json_report(results_list):
    with open(JSON_REPORT, "w", encoding="utf-8") as f:
        json.dump(results_list, f, indent=2)

def scan_all_scrolls(output="console"):
    results_list = []
    print("🧠 DreamWeaver Autolearn Scan Report\n")
    for filename in sorted(os.listdir(DOMAIN_FOLDER)):
        if filename.endswith(".md"):
            path = os.path.join(DOMAIN_FOLDER, filename)
            result = scan_scroll(path)
            results_list.append(result)

            if output == "console":
                print(f"📜 {result['filename']}")
                print(f"   ✅ Companion Tag: {'Yes' if result['companion_tag'] else 'No'}")
                print(f"   📌 Status: {result['status']}")
                for header in SECTION_HEADERS:
                    print(f"   🔹 {header}: {'✅' if result[header] else '❌'}")
                print(f"   🚀 Promotion Ready: {'✅' if result['promotion_ready'] else '❌'}\n")

    if output == "markdown":
        generate_markdown_report(results_list)
        print(f"✅ Markdown report saved to {MARKDOWN_REPORT}")
    elif output == "json":
        generate_json_report(results_list)
        print(f"✅ JSON report saved to {JSON_REPORT}")

if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "console"
    scan_all_scrolls(output=mode)
