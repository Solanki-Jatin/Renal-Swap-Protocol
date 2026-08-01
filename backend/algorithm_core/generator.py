"""
Synthetic dataset generator for incompatible patient-donor pairs.

Generates a pool of pairs where, by construction, each patient's own
donor is not compatible with them, that incompatibility is exactly why
the pair needs the exchange system in the first place. Blood types are
drawn using population level frequencies rather than uniform randomness,
so the resulting pool behaves like a realistic patient population
instead of an artificial, evenly split one.
"""

import random
import uuid
from typing import List, Optional

from .models import BloodType, Patient, Donor, IncompatiblePair
from .compatibility import is_compatible

# Approximate global population blood type distribution. Real figures
# vary by country and region, these are representative values used to
# make the synthetic pool behave realistically rather than randomly.
BLOOD_TYPE_WEIGHTS = {
    BloodType.O: 0.44,
    BloodType.A: 0.42,
    BloodType.B: 0.10,
    BloodType.AB: 0.04,
}

# Roughly the real world share of transplant candidates considered
# highly sensitized, and therefore harder to crossmatch successfully.
SENSITIZED_RATE = 0.15


def _weighted_blood_type(rng: random.Random) -> BloodType:
    types = list(BLOOD_TYPE_WEIGHTS.keys())
    weights = list(BLOOD_TYPE_WEIGHTS.values())
    return rng.choices(types, weights=weights, k=1)[0]


def generate_incompatible_pairs(
    count: int,
    hospital_ids: Optional[List[str]] = None,
    seed: Optional[int] = None,
) -> List[IncompatiblePair]:
    """
    Generates `count` incompatible patient-donor pairs.

    hospital_ids lets you simulate a multi hospital pool, each pair is
    randomly assigned to one of the given hospital ids. If not provided,
    every pair belongs to a single default hospital.

    seed makes the output reproducible, useful for tests and for demos
    where the same dataset needs to appear every time the app runs.
    """
    rng = random.Random(seed)
    hospitals = hospital_ids or ["hospital-1"]
    pairs: List[IncompatiblePair] = []

    while len(pairs) < count:
        patient_blood_type = _weighted_blood_type(rng)
        donor_blood_type = _weighted_blood_type(rng)
        sensitized = rng.random() < SENSITIZED_RATE
        hospital_id = rng.choice(hospitals)

        # Only keep pairs where the donor is genuinely not usable for
        # their own patient, that incompatibility is the reason this
        # pair belongs in the exchange pool at all.
        if is_compatible(donor_blood_type, patient_blood_type, sensitized, rng):
            continue

        pair_id = f"pair-{uuid.uuid4().hex[:8]}"
        patient = Patient(
            id=f"patient-{uuid.uuid4().hex[:8]}",
            blood_type=patient_blood_type,
            hospital_id=hospital_id,
            sensitized=sensitized,
        )
        donor = Donor(
            id=f"donor-{uuid.uuid4().hex[:8]}",
            blood_type=donor_blood_type,
            hospital_id=hospital_id,
        )
        pairs.append(IncompatiblePair(pair_id=pair_id, patient=patient, donor=donor))

    return pairs


def generate_altruistic_donors(
    count: int,
    hospital_ids: Optional[List[str]] = None,
    seed: Optional[int] = None,
) -> List[Donor]:
    """
    Generates non directed, altruistic donors, who can start an open
    exchange chain without needing a paired patient of their own.
    """
    rng = random.Random(seed)
    hospitals = hospital_ids or ["hospital-1"]
    donors = []
    for _ in range(count):
        donors.append(
            Donor(
                id=f"altruistic-{uuid.uuid4().hex[:8]}",
                blood_type=_weighted_blood_type(rng),
                hospital_id=rng.choice(hospitals),
                is_altruistic=True,
            )
        )
    return donors
