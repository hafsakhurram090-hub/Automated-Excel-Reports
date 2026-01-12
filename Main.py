import pandas as pd

# Read CSV
df = pd.read_csv("data/sales_data.csv")

# Clean data
df["Sales"].fillna(0, inplace=True)
df["Quantity"].fillna(0, inplace=True)

# Convert Date
df["Date"] = pd.to_datetime(df["Date"])

# Save cleaned data
df.to_excel("output/cleaned_data.xlsx", index=False)


summary = {
    "Total Sales": df["Sales"].sum(),
    "Total Quantity Sold": df["Quantity"].sum(),
    "Top Product": df.groupby("Product")["Sales"].sum().idxmax(),
    "Top Region": df.groupby("Region")["Sales"].sum().idxmax()
}

summary_df = pd.DataFrame(list(summary.items()), columns=["Metric", "Value"])

summary_df.to_excel("output/summary_report.xlsx", index=False)


import matplotlib.pyplot as plt

sales_by_product = df.groupby("Product")["Sales"].sum()

sales_by_product.plot(
    kind="bar",
    color=(128/255, 128/255, 200/255),
    title=""
)
plt.ylabel("Total Sales")
plt.xlabel("Product")


plt.tight_layout()
plt.savefig("output/sales_chart.png")
plt.close()

# from fpdf import FPDF

# pdf = FPDF()
# pdf.add_page()
# pdf.set_font("Arial", size=12)

# pdf.cell(200, 10, "Sales Summary Report", ln=True)

# for key, value in summary.items():
#     pdf.cell(200, 10, f"{key}: {value}", ln=True)

# pdf.output("output/summary_report.pdf")

from fpdf import FPDF

class ReportPDF(FPDF):
    def header(self):
        self.set_fill_color(128, 128, 200)  # purple header
        self.rect(0, 0, 210, 25, 'F')

        self.set_font("Arial", "B", 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, "Sales Summary Report", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", size=9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, "Generated using Python Automation", align="C")


pdf = ReportPDF()
pdf.add_page()

# Reset text color
pdf.set_text_color(0, 0, 0)

# Section title
pdf.set_font("Arial", "B", 13)
pdf.cell(0, 10, "Key Metrics", ln=True)
pdf.ln(2)

# Accent line
pdf.set_draw_color(40, 116, 166)
pdf.line(10, pdf.get_y(), 200, pdf.get_y())
pdf.ln(5)

# Metrics content
pdf.set_font("Arial", size=11)

for key, value in summary.items():
    pdf.cell(70, 10, key, border=0)
    pdf.cell(0, 10, str(value), ln=True)

# Add chart if exists
try:
    pdf.ln(10)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "Sales Visualization", ln=True)

    pdf.image("output/sales_chart.png", x=25, w=160)
except:
    pass

pdf.output("output/summary_report.pdf")



