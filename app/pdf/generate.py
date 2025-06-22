import pdfkit
from jinja2 import Environment, FileSystemLoader
import os

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')

config = pdfkit.configuration(
    wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
)

def generate_invoice_pdf(invoice: dict, output_path="invoice.pdf") -> str:
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("invoice.html")

    html_content = template.render(invoice=invoice)
    pdfkit.from_string(html_content, output_path, configuration=config)
    
    return output_path
