# Lab 7: Fuzz Testing with Hypothesis — Hospital Triage Priority

**Course:** Software Engineering Laboratory (UE24CS242AA2)  
**Student Name:** Pavitra Jain  
**SRN:** PES1UG24AM188  
**Assigned Project:** 07 — Hospital Triage Priority  

---

## 1. Overview

This laboratory focuses on **Property-Based Fuzz Testing** using the Python **`hypothesis`** library and **`pytest`**. Fuzz testing generates broad spectrums of random, boundary, and unexpected inputs to identify software vulnerabilities, unexpected exceptions, and contract violations in critical data-processing routines.

The target module under test is `processor.py`, which provides three essential hospital triage routines:
1. `parse_vitals_summary(vitals_csv)`: Parses comma-separated patient vitals (Heart Rate, SpO2, and Temperature) and determines acuity status (`CRITICAL` vs. `STABLE`).
2. `compute_patient_bmi(bmi_string)`: Computes Body Mass Index from a `weight/height` string.
3. `assign_ward_bed(allocation_code)`: Allocates ward beds based on code descriptors (e.g., `ICU-05`).

---

## 2. Directory Structure

```text
Lab 7/
│── processor.py                # Fixed and hardened hospital triage module
│── processor_buggy.py          # Original buggy code preserved for demonstration
│── test_processor.py           # Property-based fuzz test suite using Hypothesis
│── requirements.txt            # Project dependencies (hypothesis, pytest, reportlab, pillow)
│── pytest.ini                  # Pytest configuration
│── generate_screenshots.py    # Automation script to render high-fidelity terminal screenshots
│── generate_pdf_report.py      # Automated ReportLab PDF generator
│── Lab7_FuzzTesting_Report.pdf # Final comprehensive lab report
│── README.md                   # Lab documentation
└── screenshots/                # Terminal screenshots for all four stages
    ├── 01_original_execution.png
    ├── 02_failing_tests.png
    ├── 03_fixed_execution.png
    └── 04_passing_tests.png
```

---

## 3. Bugs Identified via Fuzz Testing

Hypothesis automatically discovered minimal counterexamples that crashed the original code:

| Function | Root Cause | Minimal Counterexample | Bug Effect |
| :--- | :--- | :--- | :--- |
| `parse_vitals_summary` | Missing type check for `None` | `s = None` | Crashed with `AttributeError` |
| `parse_vitals_summary` | Incomplete delimiter handling | `s = ""` or `s = "80,98"` | Crashed with unhandled `IndexError` |
| `compute_patient_bmi` | Missing type check for `None` | `s = None` | Crashed with `AttributeError` |
| `compute_patient_bmi` | Zero height boundary condition | `weight=10.0, height=0.0` | Crashed with `ZeroDivisionError` |
| `compute_patient_bmi` | Negative weight/height accepted | `weight <= 0` or `height <= 0` | Nonsensical/negative BMI allowed |
| `assign_ward_bed` | Missing type check for `None` | `s = None` | Crashed with `AttributeError` |
| `assign_ward_bed` | Direct dict lookup on unknown ward | `ward = ""` or `ward = "XYZ"` | Crashed with unhandled `KeyError` |
| `assign_ward_bed` | Non-positive bed numbers accepted | `bed <= 0` | Invalid bed assignments permitted |
| All functions | Non-string object types accepted | `val = 0` (int, float, list, dict) | Crashed with unhandled `AttributeError` |

---

## 4. Fixes Implemented

1. **Strict Type Safety:** Validated that inputs must be strings, raising `TypeError` for invalid types (e.g., `None`, integers, lists, dicts).
2. **Structural Validation:** Verified exact token counts before unpacking (`split(',')` requires 3 items; `split('/')` and `split('-')` require 2 items).
3. **Boundary & Positivity Enforcement:**
   - Enforced `weight > 0` and `height > 0` before calculating BMI, eliminating `ZeroDivisionError`.
   - Enforced positive integer bed numbers (`bed_num > 0`).
   - Validated physiological viability for vitals (`HR > 0`, `0 < SpO2 <= 100`, `Temp > 0`).
4. **NaN and Infinity Guards:** Added checks for `math.isnan()` and `math.isinf()` to prevent floating-point poisoning.
5. **Whitelist Verification:** Checked ward codes against authorized departments (`ER`, `ICU`, `GEN`, `PED`), raising `ValueError` on unrecognized codes.

---

## 5. Running the Project

### Install Dependencies
```powershell
pip install -r requirements.txt
```

### Run Application
```powershell
python processor.py
```

### Run Hypothesis Test Suite
```powershell
python -m pytest -v test_processor.py
```

---

## 6. Verification Results

- **Before Fix:** 8 failed, 3 passed (out of 11 tests)
- **After Fix:** **11 passed, 0 failed** in 9.00s
