import random

from algorithm_core.compatibility import is_abo_compatible, is_compatible
from algorithm_core.models import BloodType


def test_o_is_universal_donor():
    for patient_type in BloodType:
        assert is_abo_compatible(BloodType.O, patient_type)


def test_ab_is_universal_recipient():
    for donor_type in BloodType:
        assert is_abo_compatible(donor_type, BloodType.AB)


def test_a_cannot_donate_to_b():
    assert is_abo_compatible(BloodType.A, BloodType.B) is False


def test_b_cannot_donate_to_a():
    assert is_abo_compatible(BloodType.B, BloodType.A) is False


def test_non_sensitized_patient_passes_when_abo_compatible():
    rng = random.Random(1)
    assert is_compatible(BloodType.O, BloodType.A, patient_sensitized=False, rng=rng) is True


def test_incompatible_abo_fails_regardless_of_sensitization():
    rng = random.Random(1)
    assert is_compatible(BloodType.A, BloodType.B, patient_sensitized=False, rng=rng) is False
    assert is_compatible(BloodType.A, BloodType.B, patient_sensitized=True, rng=rng) is False
