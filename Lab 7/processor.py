"""
Hospital Triage Priority - Data Processor
Fixed and hardened implementation following Hypothesis fuzz testing.
"""

import math

VALID_WARDS = {
    "ER": "Emergency Room",
    "ICU": "Intensive Care Unit",
    "GEN": "General Ward",
    "PED": "Pediatrics"
}


def parse_vitals_summary(vitals_csv):
    """
    Parses a comma-separated string containing patient vitals: HR, SpO2, and Temp.
    Determines triage acuity status: CRITICAL if HR > 120, SpO2 < 90, or Temp > 39.0;
    otherwise STABLE.

    Raises:
        TypeError: If vitals_csv is not a string.
        ValueError: If vitals_csv does not contain exactly 3 comma-separated numeric values,
                    or if values are NaN, Infinite, or physiologically nonsensical.
    """
    if not isinstance(vitals_csv, str):
        raise TypeError(f"Expected vitals input to be a string, got {type(vitals_csv).__name__}")

    parts = vitals_csv.split(',')
    if len(parts) != 3:
        raise ValueError(f"Expected 3 comma-separated values (HR,SpO2,Temp), got {len(parts)} part(s)")

    try:
        hr = float(parts[0].strip())
        spo2 = float(parts[1].strip())
        temp = float(parts[2].strip())
    except ValueError as e:
        raise ValueError(f"Could not parse vitals as numeric values: {e}") from e

    if math.isnan(hr) or math.isnan(spo2) or math.isnan(temp):
        raise ValueError("Vitals cannot be NaN")
    if math.isinf(hr) or math.isinf(spo2) or math.isinf(temp):
        raise ValueError("Vitals cannot be Infinite")

    if hr <= 0 or spo2 <= 0 or spo2 > 100 or temp <= 0:
        raise ValueError(f"Invalid physiological vitals: HR={hr}, SpO2={spo2}, Temp={temp}")

    critical = hr > 120.0 or spo2 < 90.0 or temp > 39.0
    return f"Vitals: HR={hr}, SpO2={spo2}% - {'CRITICAL' if critical else 'STABLE'}"


def compute_patient_bmi(bmi_string):
    """
    Computes BMI given a string in format 'weight/height' (kg / m).

    Raises:
        TypeError: If bmi_string is not a string.
        ValueError: If bmi_string does not contain exactly one '/', or if weight/height
                    are non-numeric, NaN, Infinite, or <= 0.
    """
    if not isinstance(bmi_string, str):
        raise TypeError(f"Expected BMI input to be a string, got {type(bmi_string).__name__}")

    parts = bmi_string.split('/')
    if len(parts) != 2:
        raise ValueError(f"Expected format 'weight/height', got '{bmi_string}'")

    try:
        weight = float(parts[0].strip())
        height = float(parts[1].strip())
    except ValueError as e:
        raise ValueError(f"Could not parse weight and height as numbers: {e}") from e

    if math.isnan(weight) or math.isnan(height):
        raise ValueError("Weight and height cannot be NaN")
    if math.isinf(weight) or math.isinf(height):
        raise ValueError("Weight and height cannot be Infinite")

    if weight <= 0:
        raise ValueError(f"Weight must be strictly positive (>0), got {weight}")
    if height <= 0:
        raise ValueError(f"Height must be strictly positive (>0), got {height}")

    bmi = weight / (height ** 2)
    return round(bmi, 2)


def assign_ward_bed(allocation_code):
    """
    Allocates and returns ward bed descriptor given an allocation code (e.g. 'ICU-05').

    Valid ward codes: ER, ICU, GEN, PED.
    Bed number must be a positive integer (> 0).

    Raises:
        TypeError: If allocation_code is not a string.
        ValueError: If format is invalid, ward is unrecognized, or bed number is invalid/non-positive.
    """
    if not isinstance(allocation_code, str):
        raise TypeError(f"Expected allocation code to be a string, got {type(allocation_code).__name__}")

    cleaned = allocation_code.strip()
    parts = cleaned.split('-')
    if len(parts) != 2:
        raise ValueError(f"Expected format '<WARD>-<BED_NUMBER>', got '{allocation_code}'")

    ward_str, bed_str = parts[0].strip(), parts[1].strip()
    ward_code = ward_str.upper()

    if ward_code not in VALID_WARDS:
        valid_list = ", ".join(VALID_WARDS.keys())
        raise ValueError(f"Unknown ward code '{ward_str}'. Valid codes are: {valid_list}")

    try:
        bed_num = int(bed_str)
    except ValueError as e:
        raise ValueError(f"Bed number must be a valid integer, got '{bed_str}'") from e

    if bed_num <= 0:
        raise ValueError(f"Bed number must be greater than zero (>0), got {bed_num}")

    return f"{VALID_WARDS[ward_code]} Bed #{bed_num}"


def main():
    print("==== Running parse_vitals_summary ====")
    try:
        v_input = input("Enter vitals (HR,SpO2,Temp): ")
        print("Summary:", parse_vitals_summary(v_input))
    except (ValueError, TypeError) as e:
        print(f"Input Error: {e}")

    print("\n==== Running compute_patient_bmi ====")
    try:
        b_input = input("Enter weight/height (e.g. 70/1.75): ")
        print("BMI:", compute_patient_bmi(b_input))
    except (ValueError, TypeError) as e:
        print(f"Input Error: {e}")

    print("\n==== Running assign_ward_bed ====")
    try:
        w_input = input("Enter allocation (e.g. ICU-05): ")
        print("Assignment:", assign_ward_bed(w_input))
    except (ValueError, TypeError) as e:
        print(f"Input Error: {e}")


if __name__ == "__main__":
    main()
