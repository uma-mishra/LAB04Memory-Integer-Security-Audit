from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, PageBreak, Preformatted
)
from xml.sax.saxutils import escape
from pathlib import Path

BASE = Path.home() / "Lab4"
OUT = BASE / "report" / "Lab4_Security_Audit_Report.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="ReportTitle", parent=styles["Title"],
    alignment=TA_CENTER, fontSize=20, leading=25,
    textColor=colors.HexColor("#17365D"), spaceAfter=12
))
styles.add(ParagraphStyle(
    name="SmallCode", fontName="Courier",
    fontSize=6.5, leading=8, spaceAfter=1
))
styles.add(ParagraphStyle(
    name="Cell", parent=styles["BodyText"],
    fontSize=7, leading=9
))

doc = SimpleDocTemplate(
    str(OUT), pagesize=landscape(A4),
    rightMargin=13*mm, leftMargin=13*mm,
    topMargin=15*mm, bottomMargin=15*mm
)

story = []

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawString(13*mm, 8*mm, "Unit I - Memory and Integer Security Audit")
    canvas.drawRightString(landscape(A4)[0]-13*mm, 8*mm, f"Page {doc.page}")
    canvas.restoreState()

story.append(Paragraph("UNIT I PRACTICAL ASSIGNMENT", styles["ReportTitle"]))
story.append(Paragraph("Memory and Integer Security Audit", styles["Heading1"]))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "<b>Objective:</b> Audit the faculty-supplied C module, identify memory "
    "management and integer-handling defects, remediate the source, and "
    "verify the corrected implementation using security tools.",
    styles["BodyText"]
))
story.append(Spacer(1, 12))
story.append(Paragraph("1. Defect Table", styles["Heading1"]))

md = (BASE / "report" / "defect_table.md").read_text()
rows = []
for line in md.splitlines():
    if line.startswith("|") and not line.startswith("|---"):
        cells = [x.strip() for x in line.strip("|").split("|")]
        if cells and cells[0] == "No.":
            continue
        if cells and cells[0].isdigit():
            rows.append([Paragraph(escape(x), styles["Cell"]) for x in cells])

header = ["No.", "Exact Location", "Defect Type", "Security Impact", "Remediation"]
data = [[Paragraph(f"<b>{escape(x)}</b>", styles["Cell"]) for x in header]] + rows

table = Table(data, colWidths=[12*mm, 43*mm, 48*mm, 66*mm, 85*mm], repeatRows=1)
table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#17365D")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("GRID", (0,0), (-1,-1), 0.35, colors.grey),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#EAF0F6")]),
    ("LEFTPADDING", (0,0), (-1,-1), 4),
    ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
story.append(table)

story.append(PageBreak())
story.append(Paragraph("2. Remediated Source Code", styles["Heading1"]))
story.append(Paragraph(
    "The following is the corrected implementation committed in "
    "remediated/student.c.",
    styles["BodyText"]
))
source = (BASE / "remediated" / "student.c").read_text()
for line in source.splitlines():
    story.append(Preformatted(escape(line), styles["SmallCode"]))

story.append(PageBreak())
story.append(Paragraph("3. Security Tool Verification", styles["Heading1"]))

for filename, heading in [
    ("valgrind_results.txt", "Valgrind Memcheck"),
    ("asan_results.txt", "AddressSanitizer and UBSan"),
    ("cppcheck_results.txt", "Cppcheck")
]:
    story.append(Paragraph(heading, styles["Heading2"]))
    content = (BASE / "evidence" / filename).read_text(errors="replace")
    for line in content.splitlines():
        story.append(Preformatted(escape(line), styles["SmallCode"]))
    story.append(Spacer(1, 8))

story.append(PageBreak())
story.append(Paragraph("4. Compiler Warning Comparison", styles["Heading1"]))

for filename, heading in [
    ("warnings_before.txt", "Before remediation"),
    ("warnings_after.txt", "After remediation")
]:
    story.append(Paragraph(heading, styles["Heading2"]))
    content = (BASE / "evidence" / filename).read_text(errors="replace")
    if not content.strip():
        content = "No compiler warnings."
    for line in content.splitlines():
        story.append(Preformatted(escape(line), styles["SmallCode"]))

story.append(Spacer(1, 12))
story.append(Paragraph("Conclusion", styles["Heading1"]))
story.append(Paragraph(
    "The original module contained memory allocation errors, unsafe string "
    "handling, out-of-bounds access, integer overflow risks, double-free "
    "and use-after-free defects. The remediated implementation introduces "
    "checked allocations, correct initialization, safe resizing, range "
    "checking and correct cleanup. The attached evidence records the "
    "security-tool and compiler checks performed.",
    styles["BodyText"]
))

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("PDF created:", OUT)
print("Defect entries:", len(rows))
