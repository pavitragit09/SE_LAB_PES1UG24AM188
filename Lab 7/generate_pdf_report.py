import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
    Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header line (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "SE Lab 7 Report | Fuzz Testing with Hypothesis - Hospital Triage Priority")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Footer
        footer_text = f"Student: Pavitra Jain (PES1UG24AM188) | Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, footer_text)
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()


def build_pdf(filename="Lab 7/Lab7_FuzzTesting_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2B6CB0"),
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#2C5282"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#805AD5"),
        spaceAfter=4
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Italic'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#4A5568"),
        alignment=1, # Centered
        spaceBefore=4,
        spaceAfter=10
    )

    story = []

    # Title & Header
    story.append(Paragraph("LAB 7 REPORT: FUZZ TESTING WITH HYPOTHESIS", title_style))
    story.append(Paragraph("Software Engineering Laboratory | Assigned Project: Hospital Triage Priority", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#3182CE"), spaceAfter=12))

    # Student Details Box
    details_data = [
        [Paragraph("<b>Student Name:</b>", body_style), Paragraph("Pavitra Jain", body_style),
         Paragraph("<b>Course:</b>", body_style), Paragraph("Software Engineering Lab (UE24CS242AA2)", body_style)],
        [Paragraph("<b>SRN:</b>", body_style), Paragraph("PES1UG24AM188", body_style),
         Paragraph("<b>Assignment:</b>", body_style), Paragraph("Lab 7 — Fuzz Testing", body_style)],
        [Paragraph("<b>Assigned Project:</b>", body_style), Paragraph("Hospital Triage Priority (07)", body_style),
         Paragraph("<b>Date:</b>", body_style), Paragraph("November 2026", body_style)]
    ]
    details_table = Table(details_data, colWidths=[95, 155, 85, 169])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BEE3F8")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 10))

    # 1. Objective & Overview
    story.append(Paragraph("1. Lab Objective & Overview", h1_style))
    story.append(Paragraph(
        "The objective of this laboratory is to implement rigorous property-based fuzz testing on the "
        "<b>Hospital Triage Priority</b> data processor (<code>processor.py</code>) using the Python "
        "<code>hypothesis</code> library and <code>pytest</code>. The assignment targets three critical triage data processing routines: "
        "<b>patient vitals summary parsing</b>, <b>body mass index (BMI) calculation</b>, and <b>ward bed allocation</b>.",
        body_style
    ))
    story.append(Paragraph(
        "Fuzz testing subjects each function to high volumes of automatically generated normal, edge, boundary, "
        "and highly malformed inputs (including None, empty strings, negative numbers, extreme values, zero division conditions, "
        "and unexpected object types) to expose unhandled crashes, contract violations, and missing defensive validations.",
        body_style
    ))

    # 2. What is Fuzz Testing?
    story.append(Paragraph("2. Understanding Fuzz Testing & Property-Based Testing", h1_style))
    story.append(Paragraph(
        "<b>Fuzz Testing (Fuzzing)</b> is an automated software testing methodology that inputs semi-random, malformed, "
        "or boundary-pushing data into computer programs to detect crashes, memory leaks, unhandled exceptions, and logic bugs.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Hypothesis Property-Based Testing:</b> Unlike traditional example-based unit tests where developers write fixed "
        "input-output pairs, Hypothesis allows developers to define general <i>invariants</i> and <i>properties</i> that must hold "
        "true across an infinite domain of valid or invalid inputs. When an assertion fails or an unexpected exception occurs, "
        "Hypothesis employs intelligent <b>test case shrinking</b> to isolate the minimal, reproducible counterexample that triggers the failure.",
        body_style
    ))

    # 3. Tools and Libraries
    story.append(Paragraph("3. Tools and Libraries Used", h1_style))
    tools_data = [
        [Paragraph("<b>Tool / Library</b>", body_style), Paragraph("<b>Version</b>", body_style), Paragraph("<b>Role / Purpose in Lab 7</b>", body_style)],
        [Paragraph("Python", body_style), Paragraph("3.13.5", body_style), Paragraph("Core runtime environment for hospital triage priority execution.", body_style)],
        [Paragraph("Hypothesis", body_style), Paragraph("6.170.15", body_style), Paragraph("Property-based testing engine supplying strategies (<code>st.text()</code>, <code>st.floats()</code>, <code>st.integers()</code>, shrinking).", body_style)],
        [Paragraph("Pytest", body_style), Paragraph("9.1.1", body_style), Paragraph("Test execution framework, assertion evaluation, and detailed reporting.", body_style)],
        [Paragraph("Pillow & ReportLab", body_style), Paragraph("12.2 / 5.1", body_style), Paragraph("High-fidelity screenshot rendering and automated professional PDF report generation.", body_style)],
    ]
    tools_table = Table(tools_data, colWidths=[100, 70, 334])
    tools_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F7FAFC"), colors.white]),
    ]))
    story.append(tools_table)
    story.append(Spacer(1, 10))

    # 4. Bugs Identified
    story.append(Paragraph("4. Bugs Identified via Fuzz Testing", h1_style))
    story.append(Paragraph(
        "Fuzz testing the initial starter code revealed critical vulnerabilities across all three triage functions:",
        body_style
    ))
    story.append(Paragraph("• <b>Vitals Parsing (<code>parse_vitals_summary</code>):</b> Crashed with <code>AttributeError</code> when passed <code>None</code> or non-string types; raised unhandled <code>IndexError</code> when inputs contained fewer than three comma-separated elements (e.g., empty string <code>\"\"</code> or <code>\"80,98\"</code>); lacked bounds checking for physiological impossibility (negative heart rate or SpO2 > 100%).", bullet_style))
    story.append(Paragraph("• <b>BMI Computation (<code>compute_patient_bmi</code>):</b> Crashed with <code>AttributeError</code> on <code>None</code>; raised unhandled <code>ZeroDivisionError</code> when height was <code>0.0</code>; accepted negative heights and weights without validation; crashed with unhandled <code>ValueError</code> on missing or multiple <code>'/'</code> delimiters.", bullet_style))
    story.append(Paragraph("• <b>Ward Bed Allocation (<code>assign_ward_bed</code>):</b> Crashed with <code>AttributeError</code> on <code>None</code>; raised unhandled <code>KeyError</code> when unknown ward codes (e.g. <code>\"SURGERY\"</code>, <code>\"\"</code>) were passed; accepted invalid and non-positive bed numbers (<code>bed <= 0</code>).", bullet_style))
    story.append(Spacer(1, 10))

    # 5. Fixes Implemented
    story.append(Paragraph("5. Fixes and Defenses Implemented", h1_style))
    story.append(Paragraph("• <b>Strict Type Enforcement:</b> Added explicit type verification across all three functions to ensure only string instances are processed, safely raising informative <code>TypeError</code> exceptions for non-string inputs.", bullet_style))
    story.append(Paragraph("• <b>Robust Delimiter & Partition Validation:</b> Validated split counts (exactly 3 parts for vitals, exactly 2 parts for BMI and ward code), raising <code>ValueError</code> with diagnostic messages on structural mismatches.", bullet_style))
    story.append(Paragraph("• <b>Boundary, Positivity & Zero-Division Guards:</b> Required height and weight to be strictly positive numbers (<code>> 0</code>), directly preventing <code>ZeroDivisionError</code>; validated that bed numbers are integers strictly greater than 0; enforced positive vitals ranges and <code>SpO2 <= 100%</code>.", bullet_style))
    story.append(Paragraph("• <b>Dictionary Whitelist Verification:</b> Replaced direct dictionary indexing with safe key validation against authorized ward codes (<code>ER</code>, <code>ICU</code>, <code>GEN</code>, <code>PED</code>), converting unrecognized codes into descriptive <code>ValueError</code> exceptions.", bullet_style))
    story.append(Paragraph("• <b>Special Float Guards:</b> Explicitly guarded against IEEE-754 <code>NaN</code> and <code>Infinity</code> values to prevent arithmetic poisoning in triage classification.", bullet_style))

    # Page Break for Execution Stages & Screenshots
    story.append(PageBreak())

    # 6. Four Stages of Execution
    story.append(Paragraph("6. Four Stages of Execution (Screenshots & Verification)", h1_style))
    story.append(Paragraph(
        "Below are the verified execution stages showing the original application behavior, the failing Hypothesis fuzz tests, "
        "the fixed application execution with robust input handling, and the passing test suite.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Stage 1
    story.append(Paragraph("Stage 1: Original Buggy Application Execution", h2_style))
    if os.path.exists("Lab 7/screenshots/01_original_execution.png"):
        img1 = RLImage("Lab 7/screenshots/01_original_execution.png", width=490, height=210)
        story.append(img1)
    story.append(Paragraph("<i>Figure 1: Original processor.py execution demonstrating normal output alongside unhandled IndexError crash when vitals input is incomplete.</i>", caption_style))
    story.append(Spacer(1, 6))

    # Stage 2
    story.append(Paragraph("Stage 2: Hypothesis Tests Failing Against Buggy Code", h2_style))
    if os.path.exists("Lab 7/screenshots/02_failing_tests.png"):
        img2 = RLImage("Lab 7/screenshots/02_failing_tests.png", width=490, height=210)
        story.append(img2)
    story.append(Paragraph("<i>Figure 2: Pytest and Hypothesis exposing 8 test failures with minimal counterexamples (None inputs, zero height, invalid ward keys).</i>", caption_style))
    story.append(Spacer(1, 6))

    # Page Break for Stage 3 & 4
    story.append(PageBreak())

    # Stage 3
    story.append(Paragraph("Stage 3: Fixed Application Execution & Safe Validation", h2_style))
    if os.path.exists("Lab 7/screenshots/03_fixed_execution.png"):
        img3 = RLImage("Lab 7/screenshots/03_fixed_execution.png", width=490, height=210)
        story.append(img3)
    story.append(Paragraph("<i>Figure 3: Fixed processor.py executing valid inputs correctly and safely reporting errors on malformed vitals, zero height, and unknown wards.</i>", caption_style))
    story.append(Spacer(1, 6))

    # Stage 4
    story.append(Paragraph("Stage 4: Hypothesis Tests Passing Against Fixed Code", h2_style))
    if os.path.exists("Lab 7/screenshots/04_passing_tests.png"):
        img4 = RLImage("Lab 7/screenshots/04_passing_tests.png", width=490, height=210)
        story.append(img4)
    story.append(Paragraph("<i>Figure 4: Complete test suite passing against the fixed implementation (11 passed in 9.00s) with zero unexpected exceptions.</i>", caption_style))
    story.append(Spacer(1, 10))

    # 7. Test Results Comparison Table
    story.append(Paragraph("7. Comprehensive Test Results Comparison", h1_style))
    test_table_data = [
        [Paragraph("<b>Test Function</b>", body_style), Paragraph("<b>Input Strategy / Focus</b>", body_style), Paragraph("<b>Before Fix</b>", body_style), Paragraph("<b>After Fix</b>", body_style)],
        [Paragraph("<code>test_parse_vitals_summary_no_crash</code>", body_style), Paragraph("<code>st.text() | st.none()</code>", body_style), Paragraph("<font color='red'>FAILED (AttributeError)</font>", body_style), Paragraph("<font color='green'><b>PASSED</b></font>", body_style)],
        [Paragraph("<code>test_compute_patient_bmi_safe</code>", body_style), Paragraph("<code>st.text() | st.none()</code>", body_style), Paragraph("<font color='red'>FAILED (AttributeError)</font>", body_style), Paragraph("<font color='green'><b>PASSED</b></font>", body_style)],
        [Paragraph("<code>test_assign_ward_bed_safe</code>", body_style), Paragraph("<code>st.text() | st.none()</code>", body_style), Paragraph("<font color='red'>FAILED (AttributeError)</font>", body_style), Paragraph("<font color='green'><b>PASSED</b></font>", body_style)],
        [Paragraph("<code>test_unexpected_types_handling</code>", body_style), Paragraph("ints, floats, lists, dicts", body_style), Paragraph("<font color='red'>FAILED (AttributeError)</font>", body_style), Paragraph("<font color='green'><b>PASSED</b></font>", body_style)],
        [Paragraph("<code>test_parse_vitals_summary_properties</code>", body_style), Paragraph("HR, SpO2, Temp ranges", body_style), Paragraph("<font color='green'>PASSED</font>", body_style), Paragraph("<font color='green'><b>PASSED</b></font>", body_style)],
        [Paragraph("<code>test_compute_patient_bmi_valid_calc</code>", body_style), Paragraph("Positive weights and heights", body_style), Paragraph("<font color='green'>PASSED</font>", body_style), Paragraph("<font color='green'><b>PASSED</b></font>", body_style)],
        [Paragraph("<code>test_compute_patient_bmi_neg_weight</code>", body_style), Paragraph("<code>weight <= 0.0</code>", body_style), Paragraph("<font color='red'>FAILED (No ValueError)</font>", body_style), Paragraph("<font color='green'><b>PASSED</b></font>", body_style)],
        [Paragraph("<code>test_compute_patient_bmi_zero_neg_height</code>", body_style), Paragraph("<code>height <= 0.0</code>", body_style), Paragraph("<font color='red'>FAILED (ZeroDivision)</font>", body_style), Paragraph("<font color='green'><b>PASSED</b></font>", body_style)],
        [Paragraph("<code>test_assign_ward_bed_valid_allocations</code>", body_style), Paragraph("Valid ward codes, bed > 0", body_style), Paragraph("<font color='green'>PASSED</font>", body_style), Paragraph("<font color='green'><b>PASSED</b></font>", body_style)],
        [Paragraph("<code>test_assign_ward_bed_invalid_ward</code>", body_style), Paragraph("Unrecognized ward codes", body_style), Paragraph("<font color='red'>FAILED (KeyError)</font>", body_style), Paragraph("<font color='green'><b>PASSED</b></font>", body_style)],
        [Paragraph("<code>test_assign_ward_bed_zero_or_negative_bed</code>", body_style), Paragraph("<code>bed <= 0</code>", body_style), Paragraph("<font color='red'>FAILED (No ValueError)</font>", body_style), Paragraph("<font color='green'><b>PASSED</b></font>", body_style)],
    ]
    summary_table = Table(test_table_data, colWidths=[155, 125, 115, 109])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F7FAFC"), colors.white]),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 10))

    # 8. Conclusion
    story.append(Paragraph("8. Conclusion & Key Takeaways", h1_style))
    story.append(Paragraph(
        "Through Hypothesis property-based fuzz testing, eight severe edge-case vulnerabilities and failure modes were systematically uncovered "
        "and isolated into minimal counterexamples. By implementing defensive input validation, type safety checks, boundary enforcement, "
        "and structured error handling, the Hospital Triage Priority module was successfully transformed into a reliable, crash-resistant system. "
        "All 11 property and fuzz tests pass consistently, establishing robust assurance for clinical triage data processing.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Report generated successfully:", filename)

if __name__ == '__main__':
    build_pdf()
