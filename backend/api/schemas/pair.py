from pydantic import BaseModel


class PairOut(BaseModel):
    """A single incompatible patient-donor pair, as returned by the API."""
    id: str
    patient_blood_type: str
    donor_blood_type: str
    patient_sensitized: bool
    hospital_id: str
