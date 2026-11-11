import math
import pytest
from hypothesis import given, strategies as st
from processor import parse_vitals_summary, compute_patient_bmi, assign_ward_bed

# ===========================================================================
# 1. Broad Fuzz Tests for Unexpected / Malformed Inputs (Starter Requirements)
# ===========================================================================

@given(st.text() | st.none())
def test_parse_vitals_summary_no_crash(s):
    """
    Fuzz parse_vitals_summary with arbitrary text and None.
    Should either return a valid summary string or raise a clean ValueError/TypeError.
    Must never crash with unhandled AttributeError or IndexError.
    """
    try:
        result = parse_vitals_summary(s)
        assert isinstance(result, str)
        assert "Vitals: HR=" in result
        assert ("CRITICAL" in result) or ("STABLE" in result)
    except (ValueError, TypeError):
        pass


@given(st.text() | st.none())
def test_compute_patient_bmi_safe(s):
    """
    Fuzz compute_patient_bmi with arbitrary text and None.
    Should either return a rounded float BMI or raise a clean ValueError/TypeError.
    Must never crash with unhandled AttributeError, ZeroDivisionError, or unhandled exceptions.
    """
    try:
        result = compute_patient_bmi(s)
        assert isinstance(result, float)
        assert not math.isnan(result)
        assert not math.isinf(result)
        assert result > 0
    except (ValueError, TypeError):
        pass


@given(st.text() | st.none())
def test_assign_ward_bed_safe(s):
    """
    Fuzz assign_ward_bed with arbitrary text and None.
    Should either return a formatted ward assignment string or raise a clean ValueError/TypeError.
    Must never crash with unhandled AttributeError, KeyError, or IndexError.
    """
    try:
        result = assign_ward_bed(s)
        assert isinstance(result, str)
        assert "Bed #" in result
    except (ValueError, TypeError):
        pass


# ===========================================================================
# 2. Type Robustness Tests (Unexpected Data Types: ints, floats, lists, dicts)
# ===========================================================================

@given(st.one_of(st.integers(), st.floats(), st.booleans(), st.lists(st.integers()), st.dictionaries(st.text(), st.text())))
def test_unexpected_types_handling(val):
    """
    Ensure all three functions safely reject non-string input types with TypeError.
    """
    with pytest.raises(TypeError):
        parse_vitals_summary(val)

    with pytest.raises(TypeError):
        compute_patient_bmi(val)

    with pytest.raises(TypeError):
        assign_ward_bed(val)


# ===========================================================================
# 3. Domain-Specific Property & Boundary Tests for Hospital Triage
# ===========================================================================

@given(
    hr=st.floats(min_value=20.0, max_value=250.0, allow_nan=False, allow_infinity=False),
    spo2=st.floats(min_value=50.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    temp=st.floats(min_value=30.0, max_value=45.0, allow_nan=False, allow_infinity=False)
)
def test_parse_vitals_summary_properties(hr, spo2, temp):
    """
    Property test: Valid physiologic vitals must be parsed correctly and classified
    as CRITICAL if HR > 120 or SpO2 < 90 or Temp > 39.0, else STABLE.
    """
    vitals_csv = f"{hr},{spo2},{temp}"
    summary = parse_vitals_summary(vitals_csv)
    is_critical = (hr > 120.0) or (spo2 < 90.0) or (temp > 39.0)
    expected_status = "CRITICAL" if is_critical else "STABLE"
    assert expected_status in summary
    assert "Vitals: HR=" in summary


@given(
    weight=st.floats(min_value=1.0, max_value=400.0, allow_nan=False, allow_infinity=False),
    height=st.floats(min_value=0.5, max_value=2.8, allow_nan=False, allow_infinity=False)
)
def test_compute_patient_bmi_valid_calculation(weight, height):
    """
    Property test: Valid weight and height must produce BMI = round(weight / height^2, 2).
    """
    bmi_str = f"{weight}/{height}"
    expected_bmi = round(weight / (height ** 2), 2)
    assert compute_patient_bmi(bmi_str) == expected_bmi


@given(
    weight=st.floats(max_value=0.0, allow_nan=False, allow_infinity=False),
    height=st.floats(min_value=0.5, max_value=2.5, allow_nan=False, allow_infinity=False)
)
def test_compute_patient_bmi_zero_or_negative_weight(weight, height):
    """
    Edge case: Non-positive weight (zero or negative) must raise ValueError.
    """
    with pytest.raises(ValueError):
        compute_patient_bmi(f"{weight}/{height}")


@given(
    weight=st.floats(min_value=10.0, max_value=150.0, allow_nan=False, allow_infinity=False),
    height=st.floats(max_value=0.0, allow_nan=False, allow_infinity=False)
)
def test_compute_patient_bmi_zero_or_negative_height(weight, height):
    """
    Edge case: Non-positive height (zero or negative) must raise ValueError,
    preventing ZeroDivisionError and nonsensical metrics.
    """
    with pytest.raises(ValueError):
        compute_patient_bmi(f"{weight}/{height}")


@given(
    ward=st.sampled_from(["ER", "ICU", "GEN", "PED", "er", "icu", "gen", "ped"]),
    bed=st.integers(min_value=1, max_value=999)
)
def test_assign_ward_bed_valid_allocations(ward, bed):
    """
    Property test: Valid ward codes (case-insensitive) and positive bed numbers
    must correctly format the ward name and bed number.
    """
    code = f"{ward}-{bed}"
    result = assign_ward_bed(code)
    ward_names = {
        "ER": "Emergency Room",
        "ICU": "Intensive Care Unit",
        "GEN": "General Ward",
        "PED": "Pediatrics"
    }
    expected_name = ward_names[ward.upper()]
    assert f"{expected_name} Bed #{bed}" == result


@given(
    ward=st.text().filter(lambda w: w.strip().upper() not in ["ER", "ICU", "GEN", "PED"] and "-" not in w),
    bed=st.integers(min_value=1, max_value=100)
)
def test_assign_ward_bed_invalid_ward(ward, bed):
    """
    Boundary/Edge case: Unknown ward codes must raise ValueError rather than KeyError.
    """
    code = f"{ward}-{bed}"
    with pytest.raises(ValueError):
        assign_ward_bed(code)


@given(
    ward=st.sampled_from(["ER", "ICU", "GEN", "PED"]),
    bed=st.integers(max_value=0)
)
def test_assign_ward_bed_zero_or_negative_bed(ward, bed):
    """
    Edge case: Non-positive bed numbers (<= 0) must raise ValueError.
    """
    code = f"{ward}-{bed}"
    with pytest.raises(ValueError):
        assign_ward_bed(code)
