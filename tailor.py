import os
from fpdf import FPDF

BASE_RESUME = """SEETHA RAMADEVI TELAGAMSETTI
Data Analyst / Power BI Data Modeler | 3+ Years Experience
Hyderabad | seethatelagamsetti@gmail.com | +91-8639237718

PROFESSIONAL SUMMARY:
Detail-oriented Data Analyst / Modeler with 3+ years of experience designing complex Power BI data models, building ETL/ELT pipelines, and delivering scalable business intelligence. Expert in DAX, Power Query (M), star/snowflake schemas, SQL query optimisation, Python (data profiling, EDA, automation), and data governance frameworks. Proven ability to translate complex business and finance requirements into clear, scalable data structures and KPI dashboards.

CORE SKILLS:
Power BI & Data Modeling: data model design, DAX (measures, time intelligence, KPIs), Power Query (M), relationships, star/snowflake schemas, dimensional modelling, KPI dashboards
SQL: joins, aggregations, window functions (ROW_NUMBER, RANK, LEAD/LAG), CTEs, performance tuning, query optimisation, data validation
Python: Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn - data profiling, EDA, automation, statistical analysis
Data Engineering: ETL/ELT workflows, data pipelines, data cleaning & transformation, data lineage, reference data management
Data Governance: data stewardship, metadata management, data lifecycle management, reference data integrity
Azure: Azure SQL Database, Azure Data Lake (foundational knowledge)
Tools: MySQL, Jupyter Notebook, VS Code, Git, Excel (Pivot Tables, VLOOKUP, Advanced Formulas)

PROFESSIONAL EXPERIENCE:
Data Analyst / TPM Engineer | Dr. Reddy's Laboratories, Hyderabad | Nov 2023 - Jan 2026
- Designed and maintained complex Power BI data models (star schema, DAX measures, Power Query transformations) - improved KPI reporting efficiency by 30%
- Built ETL/ELT workflows for data cleansing, transformation, and loading; enforced data lineage, reference data integrity, and governance protocols
- Translated complex business and finance requirements into scalable dimensional data models supporting management decision-making and SLA tracking
- Wrote and optimised complex SQL queries on 10K+ record datasets - reduced query execution time by 30% through indexing and restructuring
- Automated data workflows using Python (Pandas, NumPy) for data profiling, quality checks - reduced analyst cycle time significantly
- Designed KPI frameworks tracking OEE, failure rates, cost metrics, and maintenance SLAs for cross-functional stakeholders
- Implemented data governance: metadata management, data stewardship, lifecycle management
- Conducted predictive analytics and RCA/FMEA - reduced equipment downtime by 15-25%, improved reliability by 20%+

Mechanical Design Engineer | Wynderz, Hyderabad | May 2023 - Nov 2023
- Analysed production data; produced business operations reports for management review
- Reduced rework by 20% through data-backed process improvements; tracked KPIs (yield, throughput, on-time delivery)
- Validated data inputs and ensured data lineage consistency across reporting systems

KEY PROJECTS:
Sales Performance & Financial Analytics Dashboard | Power BI | DAX | Dimensional Modeling
- Star schema data model in Power BI; analysed $57M revenue, 4M units, 10K+ shipments; DAX measures for $32.9M profit, 57% margin, drill-down trend analysis
- Power Query (M) transformations for data integration across multiple sources; reference data reconciliation; improved insight accessibility by 30%

IPL Analytics Dashboard | Python | SQL | Power BI | DAX
- End-to-end Power BI data model with DAX measures and Power Query for 100K+ records; full data lineage tracking
- Statistical forecasting; automated data refresh workflows - reduced manual reporting effort by 40%

SQL Analytics & Query Optimisation | MySQL | Performance Tuning
- Optimised complex SQL queries - reduced execution time 30%; implemented data validation and lineage tracing

Python Data Profiling & EDA | Pandas | NumPy | Seaborn | Matplotlib
- Full-cycle data profiling, quality checks, cleaning, transformation, and visualisation on real-world datasets

EDUCATION:
Integrated B.Tech - Mechanical Engineering | IIIT Nuzvid (RGUKT), Andhra Pradesh

CERTIFICATIONS:
- Data Analytics Certification
- TPM Accelerator Program - Dr. Reddy's Laboratories
- CGMP Certification - Pharmaceutical Industry Compliance
- (Pursuing) Microsoft Certified: Power BI Data Analyst Associate
"""


def tailor_resume_text(job: dict) -> str:
    """Use Claude API to tailor the resume for a specific job."""
    from config import CLAUDE_API_KEY, CLAUDE_MODEL
    import anthropic

    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

    prompt = (
        f"You are a professional resume writer. Tailor the resume below for this specific job.\n\n"
        f"JOB TITLE: {job['title']}\n"
        f"COMPANY: {job['company']}\n"
        f"LOCATION: {job['location']}\n"
        f"JOB DESCRIPTION: {job.get('description') or 'Not available - tailor based on title/company.'}\n\n"
        f"BASE RESUME:\n{BASE_RESUME}\n\n"
        f"Instructions:\n"
        f"- Rewrite the summary to directly match this role and company\n"
        f"- Reorder/emphasise the most relevant skills for this role\n"
        f"- Adjust bullet points to highlight most relevant experience\n"
        f"- Do NOT invent new experience - only use what is in the base resume\n"
        f"- Keep the same sections and structure\n"
        f"- Output ONLY the tailored resume text, no commentary\n"
    )

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1800,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def _clean(t: str) -> str:
    return (t.replace("—", "-").replace("–", "-")
             .replace("’", "'").replace("‘", "'")
             .replace("“", '"').replace("”", '"'))


def generate_pdf(resume_text: str, job_title: str, company: str) -> str:
    """Render tailored resume text as a formatted PDF."""
    DARK_BLUE = (15, 60, 110)

    pdf = FPDF(format="A4")
    pdf.set_margins(18, 16, 18)
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.add_page()

    lines = resume_text.split("\n")

    for i, raw in enumerate(lines):
        line = _clean(raw.strip())

        if not line:
            pdf.ln(2)
            continue

        if i == 0:                              # Name
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_text_color(*DARK_BLUE)
            pdf.cell(0, 8, line, align="C", new_x="LMARGIN", new_y="NEXT")

        elif i == 1:                            # Subtitle
            pdf.set_font("Helvetica", "I", 9.5)
            pdf.set_text_color(60, 60, 60)
            pdf.cell(0, 5, line, align="C", new_x="LMARGIN", new_y="NEXT")

        elif i == 2:                            # Contact
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(0, 5, line, align="C", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)

        elif line.endswith(":") and len(line) < 40 and line == line.upper():
            # Section header
            pdf.set_fill_color(*DARK_BLUE)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.cell(0, 6, f"  {line.rstrip(':')}", fill=True,
                     new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(20, 20, 20)
            pdf.ln(1)

        elif line.startswith("- ") or line.startswith("* "):
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(20, 20, 20)
            pdf.set_x(pdf.l_margin + 4)
            pdf.cell(4, 4.8, "-")
            pdf.multi_cell(0, 4.8, line[2:], new_x="LMARGIN", new_y="NEXT")
            pdf.ln(0.3)

        elif " | " in line and len(line) < 90:  # job/project title line
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_text_color(*DARK_BLUE)
            pdf.multi_cell(0, 5.5, line, new_x="LMARGIN", new_y="NEXT")

        else:
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(20, 20, 20)
            pdf.multi_cell(0, 4.8, line, new_x="LMARGIN", new_y="NEXT")

    safe = lambda s: "".join(c for c in s if c.isalnum() or c in " _-")[:30].strip()
    filename = f"Seetha_{safe(job_title)}_{safe(company)}.pdf".replace(" ", "_")
    pdf.output(filename)
    return filename
