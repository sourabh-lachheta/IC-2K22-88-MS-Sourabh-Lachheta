import json
import os


def save_report(report, output_path="reports/report.json"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print("Report saved to:", output_path)