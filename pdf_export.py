from fpdf import FPDF
import io

def generate_pdf(code: str, suggestions: str) -> io.BytesIO:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    
    pdf.set_text_color(40, 40, 100)
    pdf.cell(0, 10, "Codalyze AI Code Review", ln=True, align='C')
    pdf.ln(5)

    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(0, 10, "Submitted Code:", ln=True)
    pdf.set_font("Courier", size=10)
    pdf.multi_cell(0, 6, code)
    pdf.ln(5)

    
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(0, 10, "AI Feedback:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, suggestions)

    
    pdf_output = io.BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1') 
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output
