"""
create_pdf.py

This script generates three realistic university PDF documents.

Generated PDFs:
1. Student_Handbook.pdf
2. Admission_Guide.pdf
3. Faculty_Handbook.pdf

These PDFs will be used throughout the Advanced Retrieval tutorial.
"""

import os
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    PageBreak
)

# ----------------------------------------------------------
# Create output directory
# ----------------------------------------------------------

OUTPUT_DIR = "data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()

title_style = styles["Title"]
heading_style = styles["Heading1"]
body_style = styles["BodyText"]


# ----------------------------------------------------------
# Generic PDF Creator
# ----------------------------------------------------------

def create_pdf(filename, pages):
    """
    Creates a PDF from a list of pages.

    Parameters
    ----------
    filename : str
        Output PDF filename.

    pages : list
        List of tuples
        [
            ("Heading", "Content"),
            ("Heading", "Content")
        ]
    """

    filepath = os.path.join(OUTPUT_DIR, filename)

    doc = SimpleDocTemplate(
        filepath,
        rightMargin=40,
        leftMargin=40,
        topMargin=50,
        bottomMargin=50
    )

    story = []

    # Cover Page
    story.append(Paragraph(filename.replace("_", " ").replace(".pdf", ""), title_style))
    story.append(PageBreak())

    # Add each page
    for heading, content in pages:

        story.append(Paragraph(heading, heading_style))
        story.append(Paragraph(content.replace("\n", "<br/>"), body_style))
        story.append(PageBreak())

    doc.build(story)

    print(f"✓ Created : {filepath}")


# ----------------------------------------------------------
# Student Handbook
# ----------------------------------------------------------

student_pages = [

(
"Welcome",
"""
Welcome to CHRIST University.

This handbook provides important academic information
for all students.

Students are expected to understand university policies
before the commencement of classes.

This handbook covers:

• Attendance Policy

• Examination Rules

• Library Services

• Hostel Regulations

• Student Discipline

• Student Welfare

Students should regularly visit the ERP portal for updates.
"""
),

(
"Attendance Policy",
"""
Students must maintain at least 85 percent attendance.

MBA students must maintain 90 percent attendance.

BBA students must maintain 80 percent attendance.

Medical leave is considered only after proper approval.

Students having attendance shortage may not be permitted
to appear for the End Semester Examination.

Attendance can be viewed through the ERP portal.

Parents may also receive attendance notifications.
"""
),

(
"Examination Rules",
"""
Continuous Internal Assessment contributes 50 marks.

End Semester Examination contributes 50 marks.

Minimum passing marks are 40 percent.

Malpractice is treated seriously.

Revaluation applications should be submitted within
seven working days.

Students should carry identity cards while appearing
for examinations.
"""
),

(
"Library Policy",
"""
Students can borrow six books.

Loan duration is fourteen days.

Late return attracts fines.

Digital Library is available 24 hours.

Research databases include:

IEEE

Springer

ScienceDirect

JSTOR

Students should maintain silence inside the library.
"""
),

(
"Hostel Rules",
"""
Visitors are allowed only during visiting hours.

Hostel gates close at 10 PM.

Cooking appliances are prohibited.

Students should maintain cleanliness.

Ragging is strictly prohibited.

Any damage to hostel property must be reported
immediately.
"""
),

(
"Student Discipline",
"""
Students should wear identity cards.

Mobile phones should remain silent during lectures.

Respect towards faculty members is mandatory.

Damage to university property attracts disciplinary action.

Repeated misconduct may result in suspension.

Students should maintain professional behaviour
both on campus and online.
"""
)
]

# ----------------------------------------------------------
# Admission Guide
# ----------------------------------------------------------

admission_pages = [

(
"Admission Overview",
"""
Admissions begin every January.

Applications are submitted online.

Candidates receive acknowledgement after submission.

Applicants should carefully verify all information
before submitting the application.

Admission notifications are communicated through
email and the university portal.
"""
),

(
"Required Documents",
"""
Applicants should upload:

Class X Marksheet

Class XII Marksheet

Transfer Certificate

Migration Certificate

Passport Size Photograph

Identity Proof

Category Certificate (if applicable)

Incomplete applications may be rejected.
"""
),

(
"Admission Process",
"""
Application Submission

↓

Document Verification

↓

Interview

↓

Fee Payment

↓

Registration

↓

Orientation

↓

Commencement of Classes
"""
),

(
"Scholarships",
"""
Merit Scholarship

Sports Scholarship

Research Scholarship

Financial Assistance

Scholarships are reviewed every academic year.

Continuation depends upon academic performance
and attendance.
"""
),

(
"Fee Payment",
"""
Fees can be paid online.

Installment facility is available.

Delayed payments attract penalties.

Students should preserve payment receipts.

Fee details are available on the ERP portal.
"""
),

(
"Cancellation and Refund",
"""
Admission cancellation requests should be submitted
through the Admission Office.

Refunds follow UGC regulations.

Refund processing usually requires
fifteen working days.

Original fee receipts should be attached
with cancellation requests.
"""
)
]

# ----------------------------------------------------------
# Faculty Handbook
# ----------------------------------------------------------

faculty_pages = [

(
"Faculty Responsibilities",
"""
Faculty members contribute through

Teaching

Research

Mentoring

Institutional Service

Industry Collaboration

Professional Ethics
"""
),

(
"Teaching Workload",
"""
Average teaching workload is
16 hours per week.

Faculty guide projects.

Faculty mentor students.

Faculty conduct laboratory sessions.

Additional responsibilities include
question paper preparation.
"""
),

(
"Research Policy",
"""
Faculty members are encouraged to

Publish research papers

Apply for funded projects

File patents

Attend conferences

Collaborate with industries

Guide PhD scholars
"""
),

(
"Leave Rules",
"""
Casual Leave

Medical Leave

Earned Leave

Maternity Leave

Leave applications require HOD approval.

Emergency leave should be informed immediately.
"""
),

(
"Performance Evaluation",
"""
Faculty performance is evaluated based on

Teaching

Research Publications

Student Feedback

Consultancy

Institutional Contribution

Professional Development
"""
),

(
"Examination Duties",
"""
Question Paper Setting

Invigilation

Answer Sheet Evaluation

Moderation

Result Submission

Confidentiality must be maintained at every stage.
"""
)
]

# ----------------------------------------------------------
# Generate PDFs
# ----------------------------------------------------------

if __name__ == "__main__":

    create_pdf(
        "Student_Handbook.pdf",
        student_pages
    )

    create_pdf(
        "Admission_Guide.pdf",
        admission_pages
    )

    create_pdf(
        "Faculty_Handbook.pdf",
        faculty_pages
    )

    print("\nAll PDFs generated successfully.")
