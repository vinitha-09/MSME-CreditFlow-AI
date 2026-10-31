from pathlib import Path

class DocumentAgent:
    name = "Document Intake Agent"
    def run(self, applicant, uploaded_names=None):
        uploaded_names = uploaded_names or []
        required = ["applicant_name", "business_name", "requested_amount", "loan_purpose"]
        missing = [x for x in required if not applicant.get(x)]
        return {
            "status": "REVIEW" if missing else "PASS",
            "required_fields_missing": missing,
            "uploaded_files": uploaded_names,
            "note": "Prototype records filenames and checks form completeness; it does not perform OCR or verify document authenticity."
        }
