from hashlib import sha256

def deidentify_patient_bundle(bundle):
    patient = bundle["patient"]
    conditions = bundle["conditions"]
    observations = bundle["observations"]

    patient_id = patient.get("id", "")
    pseudo_id = sha256(patient_id.encode()).hexdigest()[:10]

    return {
        "id": pseudo_id,
        "gender": patient.get("gender"),
        "birthDate": patient.get("birthDate"),
        "conditions": "; ".join(conditions) if conditions else "None",
        "observations": "; ".join(observations) if observations else "None"
    }
