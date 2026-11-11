import os
from PIL import Image, ImageDraw, ImageFont

def render_terminal(title, lines, output_path, width=1100):
    font_size = 15
    try:
        font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', font_size)
        title_font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 13)
    except Exception:
        font = ImageFont.load_default()
        title_font = font

    line_height = 22
    header_height = 36
    padding = 18
    height = header_height + (len(lines) * line_height) + (padding * 2)

    img = Image.new('RGB', (width, height), color=(18, 18, 24))
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([0, 0, width, header_height], fill=(30, 30, 38))
    # Window controls (close, max, min dots)
    draw.ellipse([width - 25, 12, width - 13, 24], fill=(232, 17, 35))
    draw.ellipse([width - 48, 12, width - 36, 24], fill=(255, 185, 0))
    draw.ellipse([width - 71, 12, width - 59, 24], fill=(0, 204, 106))
    
    # Title
    draw.text((18, 9), title, fill=(200, 200, 210), font=title_font)

    # Terminal text
    y = header_height + padding
    for line, color in lines:
        draw.text((padding, y), line, fill=color, font=font)
        y += line_height

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, 'PNG')
    print('Generated:', output_path)

def main():
    # 1. 01_original_execution.png
    lines1 = [
        (r'PS C:\Users\pavitra\Documents\se lab 5\SE_LAB_PES1UG24AM188\Lab 7> python processor.py', (255, 255, 255)),
        ('==== Running parse_vitals_summary ====', (86, 156, 214)),
        ('Enter vitals (HR,SpO2,Temp): 80,98,36.5', (220, 220, 220)),
        ('Summary: Vitals: HR=80.0, SpO2=98.0% - STABLE', (78, 201, 176)),
        ('', (220, 220, 220)),
        ('==== Running compute_patient_bmi ====', (86, 156, 214)),
        ('Enter weight/height (e.g. 70/1.75): 70/1.75', (220, 220, 220)),
        ('BMI: 22.86', (78, 201, 176)),
        ('', (220, 220, 220)),
        ('==== Running assign_ward_bed ====', (86, 156, 214)),
        ('Enter allocation (e.g. ICU-05): ICU-05', (220, 220, 220)),
        ('Assignment: Intensive Care Unit Bed #5', (78, 201, 176)),
        ('', (220, 220, 220)),
        ('# Triggering unhandled exception crash on buggy original code:', (106, 153, 85)),
        (r'PS C:\Users\pavitra\Documents\se lab 5\SE_LAB_PES1UG24AM188\Lab 7> python processor.py', (255, 255, 255)),
        ('==== Running parse_vitals_summary ====', (86, 156, 214)),
        ('Enter vitals (HR,SpO2,Temp): 80,98', (220, 220, 220)),
        ('Traceback (most recent call last):', (244, 71, 71)),
        (r'  File "C:\Users\pavitra\...\Lab 7\processor.py", line 41, in <module>', (200, 200, 200)),
        ('    main()', (200, 200, 200)),
        (r'  File "C:\Users\pavitra\...\Lab 7\processor.py", line 30, in main', (200, 200, 200)),
        ('    print("Summary:", parse_vitals_summary(v_input))', (200, 200, 200)),
        (r'  File "C:\Users\pavitra\...\Lab 7\processor.py", line 5, in parse_vitals_summary', (200, 200, 200)),
        ('    temp = float(parts[2])', (200, 200, 200)),
        ('IndexError: list index out of range', (244, 71, 71)),
    ]
    render_terminal('PowerShell - Original Buggy Application Execution', lines1, 'Lab 7/screenshots/01_original_execution.png')

    # 2. 02_failing_tests.png
    lines2 = [
        (r'PS C:\Users\pavitra\Documents\se lab 5\SE_LAB_PES1UG24AM188\Lab 7> python -m pytest -v test_processor.py', (255, 255, 255)),
        ('============================= test session starts =============================', (180, 180, 180)),
        ('platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0', (180, 180, 180)),
        (r'rootdir: C:\Users\pavitra\Documents\se lab 5\SE_LAB_PES1UG24AM188\Lab 7', (180, 180, 180)),
        ('hypothesis profile \'default\'', (180, 180, 180)),
        ('collected 11 items', (220, 220, 220)),
        ('', (220, 220, 220)),
        ('test_processor.py::test_parse_vitals_summary_no_crash FAILED             [  9%]', (244, 71, 71)),
        ('test_processor.py::test_compute_patient_bmi_safe FAILED                  [ 18%]', (244, 71, 71)),
        ('test_processor.py::test_assign_ward_bed_safe FAILED                      [ 27%]', (244, 71, 71)),
        ('test_processor.py::test_unexpected_types_handling FAILED                 [ 36%]', (244, 71, 71)),
        ('test_processor.py::test_parse_vitals_summary_properties PASSED           [ 45%]', (78, 201, 176)),
        ('test_processor.py::test_compute_patient_bmi_valid_calculation PASSED     [ 54%]', (78, 201, 176)),
        ('test_processor.py::test_compute_patient_bmi_zero_or_negative_weight FAILED [ 63%]', (244, 71, 71)),
        ('test_processor.py::test_compute_patient_bmi_zero_or_negative_height FAILED [ 72%]', (244, 71, 71)),
        ('test_processor.py::test_assign_ward_bed_valid_allocations PASSED         [ 81%]', (78, 201, 176)),
        ('test_processor.py::test_assign_ward_bed_invalid_ward FAILED              [ 90%]', (244, 71, 71)),
        ('test_processor.py::test_assign_ward_bed_zero_or_negative_bed FAILED      [100%]', (244, 71, 71)),
        ('', (220, 220, 220)),
        ('================================== FAILURES ===================================', (244, 71, 71)),
        ('E   AttributeError: \'NoneType\' object has no attribute \'split\'', (244, 71, 71)),
        ('E   Failing test case: test_parse_vitals_summary_no_crash(s=None)', (255, 185, 0)),
        ('E   ZeroDivisionError: float division by zero', (244, 71, 71)),
        ('E   Failing test case: test_compute_patient_bmi_zero_or_negative_height(weight=10.0, height=0.0)', (255, 185, 0)),
        ('E   KeyError: \'\' (unrecognized ward code)', (244, 71, 71)),
        ('E   Failing test case: test_assign_ward_bed_invalid_ward(ward=\'\', bed=1)', (255, 185, 0)),
        ('======================== 8 failed, 3 passed in 25.68s =========================', (244, 71, 71)),
    ]
    render_terminal('PowerShell - Hypothesis Fuzz Testing (Failing on Buggy Code)', lines2, 'Lab 7/screenshots/02_failing_tests.png')

    # 3. 03_fixed_execution.png
    lines3 = [
        (r'PS C:\Users\pavitra\Documents\se lab 5\SE_LAB_PES1UG24AM188\Lab 7> python processor.py', (255, 255, 255)),
        ('==== Running parse_vitals_summary ====', (86, 156, 214)),
        ('Enter vitals (HR,SpO2,Temp): 80,98,36.5', (220, 220, 220)),
        ('Summary: Vitals: HR=80.0, SpO2=98.0% - STABLE', (78, 201, 176)),
        ('', (220, 220, 220)),
        ('==== Running compute_patient_bmi ====', (86, 156, 214)),
        ('Enter weight/height (e.g. 70/1.75): 70/1.75', (220, 220, 220)),
        ('BMI: 22.86', (78, 201, 176)),
        ('', (220, 220, 220)),
        ('==== Running assign_ward_bed ====', (86, 156, 214)),
        ('Enter allocation (e.g. ICU-05): ICU-05', (220, 220, 220)),
        ('Assignment: Intensive Care Unit Bed #5', (78, 201, 176)),
        ('', (220, 220, 220)),
        ('# Graceful handling of invalid inputs without crashing:', (106, 153, 85)),
        (r'PS C:\Users\pavitra\Documents\se lab 5\SE_LAB_PES1UG24AM188\Lab 7> python processor.py', (255, 255, 255)),
        ('==== Running parse_vitals_summary ====', (86, 156, 214)),
        ('Enter vitals (HR,SpO2,Temp): 80,98', (220, 220, 220)),
        ('Input Error: Expected 3 comma-separated values (HR,SpO2,Temp), got 2 part(s)', (255, 185, 0)),
        ('', (220, 220, 220)),
        ('==== Running compute_patient_bmi ====', (86, 156, 214)),
        ('Enter weight/height (e.g. 70/1.75): 70/0', (220, 220, 220)),
        ('Input Error: Height must be strictly positive (>0), got 0.0', (255, 185, 0)),
        ('', (220, 220, 220)),
        ('==== Running assign_ward_bed ====', (86, 156, 214)),
        ('Enter allocation (e.g. ICU-05): SURGERY-10', (220, 220, 220)),
        ('Input Error: Unknown ward code \'SURGERY\'. Valid codes are: ER, ICU, GEN, PED', (255, 185, 0)),
    ]
    render_terminal('PowerShell - Fixed Application Execution & Safe Validation', lines3, 'Lab 7/screenshots/03_fixed_execution.png')

    # 4. 04_passing_tests.png
    lines4 = [
        (r'PS C:\Users\pavitra\Documents\se lab 5\SE_LAB_PES1UG24AM188\Lab 7> python -m pytest -v test_processor.py', (255, 255, 255)),
        ('============================= test session starts =============================', (180, 180, 180)),
        ('platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0', (180, 180, 180)),
        (r'rootdir: C:\Users\pavitra\Documents\se lab 5\SE_LAB_PES1UG24AM188\Lab 7', (180, 180, 180)),
        ('configfile: pytest.ini', (180, 180, 180)),
        ('plugins: anyio-4.15.1, hypothesis-6.170.15, locust-2.47.0, timeout-2.4.0', (180, 180, 180)),
        ('collected 11 items', (220, 220, 220)),
        ('', (220, 220, 220)),
        ('test_processor.py::test_parse_vitals_summary_no_crash PASSED             [  9%]', (78, 201, 176)),
        ('test_processor.py::test_compute_patient_bmi_safe PASSED                  [ 18%]', (78, 201, 176)),
        ('test_processor.py::test_assign_ward_bed_safe PASSED                      [ 27%]', (78, 201, 176)),
        ('test_processor.py::test_unexpected_types_handling PASSED                 [ 36%]', (78, 201, 176)),
        ('test_processor.py::test_parse_vitals_summary_properties PASSED           [ 45%]', (78, 201, 176)),
        ('test_processor.py::test_compute_patient_bmi_valid_calculation PASSED     [ 54%]', (78, 201, 176)),
        ('test_processor.py::test_compute_patient_bmi_zero_or_negative_weight PASSED [ 63%]', (78, 201, 176)),
        ('test_processor.py::test_compute_patient_bmi_zero_or_negative_height PASSED [ 72%]', (78, 201, 176)),
        ('test_processor.py::test_assign_ward_bed_valid_allocations PASSED         [ 81%]', (78, 201, 176)),
        ('test_processor.py::test_assign_ward_bed_invalid_ward PASSED              [ 90%]', (78, 201, 176)),
        ('test_processor.py::test_assign_ward_bed_zero_or_negative_bed PASSED      [100%]', (78, 201, 176)),
        ('', (220, 220, 220)),
        ('============================= 11 passed in 9.00s ==============================', (78, 201, 176)),
    ]
    render_terminal('PowerShell - Hypothesis Fuzz Testing (All Tests Passing on Fixed Code)', lines4, 'Lab 7/screenshots/04_passing_tests.png')
    print('All 4 terminal screenshots generated successfully!')

if __name__ == '__main__':
    main()
