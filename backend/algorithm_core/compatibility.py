"""
ABO blood type compatibility rules for kidney donation, plus a simple
crossmatch simulation for highly sensitized patients.

These rules cover ABO compatibility, the same rules real transplant
centers use as the first filter. Real matching also depends on HLA
tissue typing and a lab crossmatch test, which we approximate here with
a single sensitization flag and a random crossmatch check. This keeps
the graph from being purely ABO based, closer to how real pools behave.
"""

import random
from typing import Optional

from .models import BloodType

# Which donor blood types can safely give to which patient blood types.
# O is the universal donor, AB is the universal recipient.
_ABO_COMPATIBILITY = {
    BloodType.O: {BloodType.O, BloodType.A, BloodType.B, BloodType.AB},
    BloodType.A: {BloodType.A, BloodType.AB},
    BloodType.B: {BloodType.B, BloodType.AB},
    BloodType.AB: {BloodType.AB},
}

# Baseline chance that a highly sensitized patient clears the crossmatch
# test even when the blood types are already ABO compatible. In real
# life, sensitized patients react against a much larger share of the
# donor pool, which is exactly why they are harder to match.
SENSITIZED_CROSSMATCH_PASS_RATE = 0.35


def is_abo_compatible(donor_blood_type: BloodType, patient_blood_type: BloodType) -> bool:
    """True if the donor's blood type is ABO compatible with the patient's."""
    return patient_blood_type in _ABO_COMPATIBILITY[donor_blood_type]


def passes_crossmatch(patient_sensitized: bool, rng: random.Random) -> bool:
    """
    Simulates the crossmatch lab test. Non sensitized patients always
    pass once ABO compatibility is already confirmed. Sensitized
    patients only pass some of the time, modeling the extra antibody
    reactivity that makes them much harder to match in real exchanges.
    """
    if not patient_sensitized:
        return True
    return rng.random() < SENSITIZED_CROSSMATCH_PASS_RATE


def is_compatible(
    donor_blood_type: BloodType,
    patient_blood_type: BloodType,
    patient_sensitized: bool = False,
    rng: Optional[random.Random] = None,
) -> bool:
    """
    Full compatibility check: ABO rules first, then a simulated
    crossmatch for sensitized patients. This is the single function
    every other part of the algorithm core should call, rather than
    re-implementing the rules table elsewhere.
    """
    if not is_abo_compatible(donor_blood_type, patient_blood_type):
        return False
    active_rng = rng if rng is not None else random
    return passes_crossmatch(patient_sensitized, active_rng)
