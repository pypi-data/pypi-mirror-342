import csv

def export_to_csv(patients, filename="cohort.csv"):
    if not patients:
        print("No data to export.")
        return

    keys = patients[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(patients)
