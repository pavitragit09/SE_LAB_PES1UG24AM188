# Lab 5: Static Code Analysis

**Name:** Pavitra Jain  
**SRN:** PES1UG24AM188  
**Assigned repository:** L5_07_campus_shuttle

## Objective

Analyze the campus shuttle Python program using Pylint, Bandit, and Flake8, fix identified issues, and verify the results.

## Issues Identified and Fixes

| Issue | Tool | Fix |
|---|---|---|
| Missing module docstring | Pylint | Added a module-level docstring |
| Mutable default argument | Pylint | Changed `logs=[]` to `logs=None` |
| Broad exception handling | Pylint | Removed the bare `except` and handled route conditions explicitly |
| Insecure pseudorandom generator warning | Bandit | Replaced `random.choice` with `secrets.choice` |
| Unspecified file encoding | Pylint | Specified UTF-8 encoding |
| Formatting violations | Flake8 | Corrected any violations reported by Flake8 |

*Update this table to reflect the actual findings in your before-and-after reports.*

## Verification

The before-and-after reports are included in this folder. Final results should be recorded after running all three analysis tools against the corrected program.

## Reflection

Static code analysis helps identify potential bugs, insecure coding patterns, and formatting problems without executing every possible program path. Pylint helps improve code quality, Bandit checks for common security issues, and Flake8 enforces Python style conventions. Using these tools together improves readability and maintainability and helps catch problems before submission.
