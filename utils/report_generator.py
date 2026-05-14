from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os


def generate_report(data, patient_id):

    # -----------------------------
    # FILE SETUP
    # -----------------------------
    if not os.path.exists("reports"):
        os.makedirs("reports")

    file_path = f"reports/{patient_id}.pdf"

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()

    # -----------------------------
    # STYLES
    # -----------------------------
    title_style = ParagraphStyle(
        name="TitleStyle",
        fontSize=16,
        textColor=colors.white,
        alignment=1,
    )

    header_right = ParagraphStyle(
        name="HeaderRight",
        fontSize=8,
        textColor=colors.white,
        alignment=2,
    )

    normal_style = ParagraphStyle(
        name="NormalStyle",
        fontSize=10,
    )

    impression_style = ParagraphStyle(
        name="ImpressionStyle",
        fontSize=11,
        leftIndent=5,
    )

    elements = []

    # -----------------------------
    # LOGO HANDLING (SAFE)
    # -----------------------------
    logo_path = os.path.join("assets", "logo.png")
    logo = None

    try:
        if os.path.exists(logo_path):
            logo_img = Image(
                logo_path,
                width=50,
                height=50,
            )

            logo = Table(
                [[logo_img]],
                colWidths=[55],
                rowHeights=[55],
            )

            logo.setStyle(
                TableStyle(
                    [
                        ("BOX", (0, 0), (-1, -1), 1, colors.white),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ]
                )
            )
        else:
            logo = Paragraph("LOGO", styles["Normal"])

    except Exception as e:
        print("Logo Error:", e)
        logo = Paragraph("LOGO", styles["Normal"])

    # -----------------------------
    # HEADER
    # -----------------------------
    header_data = [
        [
            logo,
            Paragraph(
                "<b>NASALANCE TEST REPORT</b>",
                title_style,
            ),
            Paragraph(
                (
                    "<b>NASALANCE DIAGNOSTIC CENTER</b><br/>"
                    "Speech & Resonance Unit<br/>"
                    "Bangalore, India<br/>"
                    "Ph: +91-XXXXXXX"
                ),
                header_right,
            ),
        ]
    ]

    header_table = Table(
        header_data,
        colWidths=[80, 260, 120],
        rowHeights=[60],
    )

    header_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.darkblue),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    elements.append(header_table)
    elements.append(Spacer(1, 15))

    # -----------------------------
    # INFO TABLE
    # -----------------------------
    info_table = Table(
        [
            [
                Paragraph(
                    f"<b>Patient Name:</b> {data['name']}",
                    normal_style,
                ),
                Paragraph(
                    (
                        f"<para alignment='right'>"
                        f"<b>Date:</b> {data['date']}"
                        f"</para>"
                    ),
                    normal_style,
                ),
            ],
            [
                Paragraph(
                    (
                        f"<b>Age / Sex:</b> "
                        f"{data['age']} / {data['gender']}"
                    ),
                    normal_style,
                ),
                Paragraph(
                    (
                        f"<para alignment='right'>"
                        f"<b>Clinician:</b> "
                        f"{data['clinician']}"
                        f"</para>"
                    ),
                    normal_style,
                ),
            ],
        ],
        colWidths=[230, 230],
    )

    info_table.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(info_table)

    # LINE
    line = Table([[""]], colWidths=[460])
    line.setStyle(
        TableStyle(
            [("LINEABOVE", (0, 0), (-1, -1), 1, colors.black)]
        )
    )

    elements.append(Spacer(1, 5))
    elements.append(line)
    elements.append(Spacer(1, 15))

    # -----------------------------
    # RESULT TABLE
    # -----------------------------
    result_data = [
        ["Parameter", "Value"],
        ["Mean Nasalance", data["mean"]],
        ["Minimum", data["min"]],
        ["Maximum", data["max"]],
        ["Z Score", data["z"]],
        ["Category", data["category"]],
        ["Severity", data["severity"]],
    ]

    result_table = Table(
        result_data,
        colWidths=[230, 230],
    )

    result_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]
        )
    )

    elements.append(result_table)
    elements.append(Spacer(1, 30))

    # -----------------------------
    # IMPRESSION
    # -----------------------------
    elements.append(
        Paragraph("<b><u>Impression:</u></b>", styles["Normal"])
    )

    elements.append(Spacer(1, 8))

    impression_table = Table(
        [[Paragraph(data["impression"], impression_style)]],
        colWidths=[460],
    )

    impression_table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1, colors.black),
                ("PADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )

    elements.append(impression_table)
    elements.append(Spacer(1, 60))

    # -----------------------------
    # SIGNATURE
    # -----------------------------
    sign_line = Table([[""]], colWidths=[150])
    sign_line.setStyle(
        TableStyle(
            [("LINEABOVE", (0, 0), (-1, -1), 1, colors.black)]
        )
    )
    sign_line.hAlign = "LEFT"

    elements.append(sign_line)
    elements.append(Spacer(1, 5))

    elements.append(
        Paragraph(
            f"Clinician: {data['clinician']}",
            styles["Normal"],
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "<i>This is a system-generated clinical report.</i>",
            styles["Normal"],
        )
    )

    doc.build(elements)

    return file_path