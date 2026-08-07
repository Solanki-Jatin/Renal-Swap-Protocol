from fastapi import APIRouter

from algorithm_core.generator import generate_incompatible_pairs

from ..schemas.dataset import GenerateDatasetRequest, GenerateDatasetResponse
from ..schemas.pair import PairOut

router = APIRouter(prefix="/dataset", tags=["dataset"])


@router.post("/generate", response_model=GenerateDatasetResponse)
def generate_dataset(request: GenerateDatasetRequest) -> GenerateDatasetResponse:
    """
    Generates a fresh synthetic pool of incompatible patient-donor
    pairs. This is the starting point of the whole pipeline, every
    other endpoint either calls this same generator internally or
    expects a pool already in this shape.
    """
    pairs = generate_incompatible_pairs(
        count=request.count,
        hospital_ids=request.hospital_ids,
        seed=request.seed,
    )
    pair_out = [
        PairOut(
            id=pair.pair_id,
            patient_blood_type=pair.patient.blood_type.value,
            donor_blood_type=pair.donor.blood_type.value,
            patient_sensitized=pair.patient.sensitized,
            hospital_id=pair.patient.hospital_id,
        )
        for pair in pairs
    ]
    return GenerateDatasetResponse(pairs=pair_out, total=len(pair_out))
