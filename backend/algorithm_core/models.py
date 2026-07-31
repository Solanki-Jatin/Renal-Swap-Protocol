"""
Core data models for the kidney exchange system.
These represent the real-world entities: a patient, a donor,
and an incompatible pair formed when a patient's own donor
does not match them medically.
"""

from dataclasses import dataclass
from enum import Enum


class BloodType(str, Enum):
    """Standard ABO blood types used for compatibility checks."""
    O = "O"
    A = "A"
    B = "B"
    AB = "AB"


@dataclass
class Patient:
    """A patient who needs a kidney transplant."""
    id: str
    blood_type: BloodType
    hospital_id: str
    sensitized: bool = False  # highly sensitized patients are harder to match


@dataclass
class Donor:
    """A willing but possibly incompatible donor, linked to one patient."""
    id: str
    blood_type: BloodType
    hospital_id: str
    is_altruistic: bool = False  # true only for non-directed donors


@dataclass
class IncompatiblePair:
    """
    A patient and their willing donor, where the donor cannot
    directly donate to that patient due to a medical mismatch.
    This is the basic unit (node) of the compatibility graph.
    """
    pair_id: str
    patient: Patient
    donor: Donor
