import argparse
from fhir_reada.fhir_connector import FHIRClient
from fhir_reada.cohort_builder import build_cohort
from fhir_reada.deid_utils import deidentify_patient_bundle
from fhir_reada.exporter import export_to_csv

def run_cli(url, min_age, max_age, diagnosis, output_file):
    client = FHIRClient(url)
    age_range = (min_age, max_age)

    print(f"Fetching patients aged {min_age}–{max_age} from {url}...")
    patients = build_cohort(client, age_range)

    bundles = []
    for patient in patients:
        pid = patient["id"]
        conditions = client.get_conditions(pid)

        if diagnosis and not any(diagnosis.lower() in c.lower() for c in conditions):
            continue

        observations = client.get_observations(pid)
        bundles.append({
            "patient": patient,
            "conditions": conditions,
            "observations": observations
        })

    print("De-identifying and exporting to CSV...")
    deidentified = [deidentify_patient_bundle(b) for b in bundles]
    export_to_csv(deidentified, filename=output_file)
    print(f"Exported to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="FHIR Cohort Extractor")
    parser.add_argument("--url", required=True, help="FHIR base URL (e.g., https://hapi.fhir.org/baseR4)")
    parser.add_argument("--min-age", type=int, default=3)
    parser.add_argument("--max-age", type=int, default=90)
    parser.add_argument("--diagnosis", help="Filter for specific condition keyword (e.g., diabetes)")
    parser.add_argument("--out", required=True, help="Output CSV file")

    args = parser.parse_args()
    run_cli(args.url, args.min_age, args.max_age, args.diagnosis, args.out)
