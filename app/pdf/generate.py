import pdfkit
from jinja2 import Environment, FileSystemLoader
import os

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')

config = pdfkit.configuration(
    wkhtmltopdf='/usr/bin/wkhtmltopdf'
)

def generate_invoice_pdf(invoice: dict) -> str:
    output_dir = os.path.join(os.getcwd(), "invoices")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"invoice_{invoice['id']}.pdf")

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("invoice.html")

    html_content = template.render(invoice=invoice)
    
    try:
        pdfkit.from_string(html_content, output_path, configuration=config)
        
    except Exception as e:
        print("Error generating PDF:", e)
        raise RuntimeError("Failed to generate PDF") from e
    
    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Path was not found: {output_path}")
    return output_path
