from datetime import date, timedelta

def calculate_birthdate_range(age_range):
    today = date.today()
    oldest_birthdate = today - timedelta(days=age_range[1]*365.25)
    youngest_birthdate = today - timedelta(days=age_range[0]*365.25)
    return (oldest_birthdate.isoformat(), youngest_birthdate.isoformat())

def extract_patient_info(entry):
    resource = entry["resource"]
    name = resource.get("name", [{}])[0]
    return {
        "id": resource.get("id"),
        "name": " ".join(name.get("given", [])) + " " + name.get("family", ""),
        "gender": resource.get("gender"),
        "birthDate": resource.get("birthDate"),
    }

def build_cohort(client, age_range):
    birthdate_range = calculate_birthdate_range(age_range)
    entries = client.search_patients(birthdate_range)

    patients = []
    for entry in entries:
        patient = extract_patient_info(entry)
        patients.append(patient)

    return patients
