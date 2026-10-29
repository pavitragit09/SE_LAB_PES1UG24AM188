import pytest

from hospital_triage_priority import (
    process_triage_wards,
    monitor_oxygen_manifolds,
)


def test_invalid_wards():
    with pytest.raises(ValueError):
        process_triage_wards("invalid", 10)


def test_negative_default_acuity():
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_empty_wards():
    result = process_triage_wards([], 10)
    assert result == {
        "acuity_score": 0,
        "status": "NO_URGENT_CASES",
    }


def test_non_accepting_ward_is_skipped():
    wards = [
        {
            "is_accepting": False,
            "patients": [{"spo2": 70, "hr": 150}],
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_normal_patient():
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [
                {"spo2": 98, "hr": 72, "unconscious": False}
            ],
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 10
    assert result["status"] == "TRIAGE_STABLE"


def test_low_spo2_patient():
    wards = [
        {
            "is_accepting": True,
            "patients": [{"spo2": 85, "hr": 80}],
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 60


def test_high_heart_rate_patient():
    wards = [
        {
            "is_accepting": True,
            "patients": [{"spo2": 95, "hr": 130}],
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 60


def test_unconscious_patient_in_general_ward():
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "patients": [{"spo2": 98, "hr": 70, "unconscious": True}],
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 100
    assert result["status"] == "TRIAGE_STABLE"


def test_unconscious_patient_in_outpatient_ward():
    wards = [
        {
            "is_accepting": True,
            "tier": "outpatient",
            "patients": [{"spo2": 98, "hr": 70, "unconscious": True}],
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_invalid_patient_readings_are_flagged():
    wards = [
        {
            "is_accepting": True,
            "patients": [
                {"spo2": 0, "hr": 70},
                {"spo2": 98, "hr": 0},
            ],
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_more_than_four_flagged_entries():
    wards = [
        {
            "is_accepting": True,
            "patients": [{"spo2": 0, "hr": 70} for _ in range(5)],
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["status"] == "WARD_ALERT"
    assert result["acuity_score"] == 0


def test_icu_standby_adds_acuity():
    wards = [
        {
            "is_accepting": True,
            "icu_standby": True,
            "patients": [{"spo2": 98, "hr": 70}],
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 35
    assert result["status"] == "TRIAGE_STABLE"


def test_default_patient_values():
    wards = [{"is_accepting": True, "patients": [{}]}]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 10


def test_empty_sensor_streams():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_empty_manifold():
    assert monitor_oxygen_manifolds([[]]) == "PRESSURE_NORMAL"


def test_two_consecutive_low_pressure_readings():
    assert monitor_oxygen_manifolds([[3.5, 3.0]]) == "PRESSURE_FAILURE"


def test_normal_reading_resets_low_pressure_streak():
    assert (
        monitor_oxygen_manifolds([[3.5, 4.0, 3.5, 4.2]])
        == "PRESSURE_NORMAL"
    )


def test_low_pressure_across_separate_manifolds():
    assert (
        monitor_oxygen_manifolds([[3.0], [3.0]])
        == "PRESSURE_NORMAL"
    )