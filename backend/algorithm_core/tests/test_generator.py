from algorithm_core.generator import generate_incompatible_pairs, generate_altruistic_donors


def test_generates_requested_count():
    pairs = generate_incompatible_pairs(count=25, seed=42)
    assert len(pairs) == 25


def test_every_pair_has_a_patient_and_a_donor():
    pairs = generate_incompatible_pairs(count=10, seed=1)
    for pair in pairs:
        assert pair.patient is not None
        assert pair.donor is not None
        assert pair.patient.id != pair.donor.id


def test_reproducible_with_seed():
    pairs_a = generate_incompatible_pairs(count=10, seed=7)
    pairs_b = generate_incompatible_pairs(count=10, seed=7)
    types_a = [(p.patient.blood_type, p.donor.blood_type) for p in pairs_a]
    types_b = [(p.patient.blood_type, p.donor.blood_type) for p in pairs_b]
    assert types_a == types_b


def test_multi_hospital_assignment():
    pairs = generate_incompatible_pairs(count=20, hospital_ids=["h1", "h2"], seed=3)
    used_hospitals = {pair.donor.hospital_id for pair in pairs}
    assert used_hospitals.issubset({"h1", "h2"})


def test_altruistic_donor_flag_set():
    donors = generate_altruistic_donors(count=5, seed=1)
    assert len(donors) == 5
    assert all(donor.is_altruistic for donor in donors)
