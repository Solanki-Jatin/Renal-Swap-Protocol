from algorithm_core.models import Patient, Donor, IncompatiblePair, BloodType


def test_incompatible_pair_creation():
    patient = Patient(id="p1", blood_type=BloodType.A, hospital_id="h1")
    donor = Donor(id="d1", blood_type=BloodType.B, hospital_id="h1")
    pair = IncompatiblePair(pair_id="pair1", patient=patient, donor=donor)

    assert pair.patient.blood_type == BloodType.A
    assert pair.donor.blood_type == BloodType.B
    assert pair.donor.is_altruistic is False


def test_altruistic_donor_flag_defaults_false():
    donor = Donor(id="d2", blood_type=BloodType.O, hospital_id="h2")
    assert donor.is_altruistic is False


def test_sensitized_patient_flag_defaults_false():
    patient = Patient(id="p2", blood_type=BloodType.AB, hospital_id="h2")
    assert patient.sensitized is False
