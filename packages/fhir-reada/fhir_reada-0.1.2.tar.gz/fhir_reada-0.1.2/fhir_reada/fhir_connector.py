import requests

class FHIRClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def search_patients(self, birthdate_range=None):
        params = {}
        if birthdate_range:
            params["birthdate"] = [f"ge{birthdate_range[0]}", f"le{birthdate_range[1]}"]
        response = requests.get(f"{self.base_url}/Patient", params=params)
        response.raise_for_status()
        return response.json().get("entry", [])

    def get_conditions(self, patient_id):
        url = f"{self.base_url}/Condition?patient={patient_id}"
        response = requests.get(url)
        response.raise_for_status()
        entries = response.json().get("entry", [])
        return [entry["resource"].get("code", {}).get("text", "Unknown") for entry in entries]

    def get_observations(self, patient_id):
        url = f"{self.base_url}/Observation?patient={patient_id}"
        response = requests.get(url)
        response.raise_for_status()
        entries = response.json().get("entry", [])
        result = []
        for entry in entries:
            obs = entry["resource"]
            code = obs.get("code", {}).get("text", "Unknown")
            value = obs.get("valueQuantity", {}).get("value", "N/A")
            unit = obs.get("valueQuantity", {}).get("unit", "")
            result.append(f"{code}: {value} {unit}".strip())
        return result
