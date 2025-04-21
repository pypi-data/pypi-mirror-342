from hashlib import sha256
from datetime import datetime

def get_birth_year_and_age(birth_date_str):
    try:
        birth = datetime.strptime(birth_date_str, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        birth_year = birth.year
        return (
            "90+" if age >= 90 else str(birth_year),
            "90+" if age >= 90 else str(age)
        )
    except Exception:
        return ("UNKNOWN", "UNKNOWN")

def deidentify_patient_bundle(bundle):
    patient = bundle["patient"]
    conditions = bundle["conditions"]
    observations = bundle["observations"]

    patient_id = patient.get("id", "")
    pseudo_id = sha256(patient_id.encode()).hexdigest()

    birth_year, age = get_birth_year_and_age(patient.get("birthDate"))

    return {
        "id": pseudo_id,
        "gender": patient.get("gender"),
        "birthYear": birth_year,
        "age": age,
        "conditions": "; ".join(conditions) if conditions else "None",
        "observations": "; ".join(observations) if observations else "None"
    }
