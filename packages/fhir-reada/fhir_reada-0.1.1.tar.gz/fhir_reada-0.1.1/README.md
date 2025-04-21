# FHIR-READA

**FHIR Research Extractor And De-identified Analyzer**

A Python CLI tool for extracting, de-identifying, and exporting patient data from FHIR servers — built for research teams, clinicians, and medical institutions.

---

## 🔍 Features

- Filter patients by age range and diagnosis  
- Extract from any FHIR-compliant server  
- Fetch Conditions and Observations  
- Automatically de-identify patient IDs  
- Export results to CSV  
- Easy-to-use CLI with flexible filters

---

## 💻 Installation

**From PyPI**

```bash
pip install fhir-reada
```

**From Source (for development or testing)**

```bash
git clone https://github.com/TOduah/fhir-reada.git
cd fhir-reada
pip install -e .
```

---

## 🚀 Usage (CLI)

```bash
fhir-reada --url https://hapi.fhir.org/baseR4 --min-age 25 --max-age 40 --diagnosis diabetes --out output.csv
```

---

## ⚙️ CLI Options

| Option         | Description                                          |
|----------------|------------------------------------------------------|
| `--url`        | FHIR base URL (e.g. `https://hapi.fhir.org/baseR4`) |
| `--min-age`    | Minimum age for cohort (e.g. `25`)                  |
| `--max-age`    | Maximum age for cohort (e.g. `40`)                  |
| `--diagnosis`  | Diagnosis keyword (optional, e.g. `diabetes`)       |
| `--out`        | Output filename for CSV export                      |

---

## 🏥 Who Is This For?

- Research institutions running clinical studies  
- Hospital data science or IT departments  
- Medical schools teaching FHIR and analytics  
- Independent developers working with public or private FHIR APIs

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 💬 Author

Built by [Tobenna Oduah](https://github.com/toduah).