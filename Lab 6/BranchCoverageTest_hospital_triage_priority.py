
import pytest

from hospital_triage_priority import (
    process_triage_wards,
    monitor_oxygen_manifolds,
)


def test_invalid_wards_type():
    with pytest.raises(ValueError):
        process_triage_wards(None, 10)


def test_negative_default_score():
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_valid_empty_wards():
    assert process_triage_wards([], 10)["status"] == "NO_URGENT_CASES"


def test_non_accepting_ward():
    wards = [{"is_accepting": False, "patients": [{"spo2": 80}]}]
    assert process_triage_wards(wards, 10)["acuity_score"] == 0


def test_accepting_ward_with_normal_patient():
    wards = [{"is_accepting": True, "patients": [{"spo2": 95, "hr": 80}]}]
    assert process_triage_wards(wards, 10)["acuity_score"] == 10


def test_invalid_spo2():
    wards = [{"is_accepting": True, "patients": [{"spo2": 0, "hr": 70}]}]
    assert process_triage_wards(wards, 10)["acuity_score"] == 0


def test_invalid_heart_rate():
    wards = [{"is_accepting": True, "patients": [{"spo2": 95, "hr": 0}]}]
    assert process_triage_wards(wards, 10)["acuity_score"] == 0


def test_unconscious_general_patient():
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "patients": [{"unconscious": True}],
        }
    ]
    assert process_triage_wards(wards, 10)["acuity_score"] == 100


def test_unconscious_outpatient():
    wards = [
        {
            "is_accepting": True,
            "tier": "outpatient",
            "patients": [{"unconscious": True}],
        }
    ]
    assert process_triage_wards(wards, 10)["status"] == "NO_URGENT_CASES"


def test_low_oxygen_branch():
    wards = [{"is_accepting": True, "patients": [{"spo2": 89, "hr": 80}]}]
    assert process_triage_wards(wards, 10)["acuity_score"] == 60


def test_high_heart_rate_branch():
    wards = [{"is_accepting": True, "patients": [{"spo2": 95, "hr": 121}]}]
    assert process_triage_wards(wards, 10)["acuity_score"] == 60


def test_normal_vitals_branch():
    wards = [{"is_accepting": True, "patients": [{"spo2": 90, "hr": 120}]}]
    assert process_triage_wards(wards, 10)["acuity_score"] == 10


def test_icu_standby_true():
    wards = [{"is_accepting": True, "icu_standby": True, "patients": []}]
    assert process_triage_wards(wards, 10)["acuity_score"] == 25


def test_icu_standby_false():
    wards = [{"is_accepting": True, "icu_standby": False, "patients": []}]
    assert process_triage_wards(wards, 10)["acuity_score"] == 0


def test_more_than_four_flagged_patients():
    patients = [{"spo2": 0, "hr": 70} for _ in range(5)]
    wards = [{"is_accepting": True, "patients": patients}]
    assert process_triage_wards(wards, 10)["status"] == "WARD_ALERT"


def test_four_flagged_patients_not_alert():
    patients = [{"spo2": 0, "hr": 70} for _ in range(4)]
    wards = [{"is_accepting": True, "patients": patients}]
    assert process_triage_wards(wards, 10)["status"] == "NO_URGENT_CASES"


def test_no_sensor_data():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_single_low_pressure_reading():
    assert monitor_oxygen_manifolds([[3.0]]) == "PRESSURE_NORMAL"


def test_two_consecutive_low_readings():
    assert monitor_oxygen_manifolds([[3.0, 3.5]]) == "PRESSURE_FAILURE"


def test_normal_pressure_resets_streak():
    assert monitor_oxygen_manifolds([[3.0, 4.0, 3.0]]) == "PRESSURE_NORMAL"


def test_failure_in_later_manifold():
    assert monitor_oxygen_manifolds([[4.0], [3.0, 3.0]]) == "PRESSURE_FAILURE"
