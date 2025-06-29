from celery import shared_task
from app.core.config import settings
from email.message import EmailMessage
from app.pdf.generate import generate_invoice_pdf
import smtplib

@shared_task(name="app.tasks.email.send_invoice_email", bind=True, auto_retry=True, retry_kwargs={'max_retries': 3, 'countdown': 5})
def send_invoice_email(self, recipient_email: str, invoice: dict):
    msg = EmailMessage()
    msg['Subject'] = f'Invoice #{invoice["id"]}'
    msg['From'] = settings.EMAIL_USERNAME
    msg['To'] = recipient_email
    msg.set_content(f'Please find attached your invoice #{invoice["id"]}.')

    file_path = generate_invoice_pdf(invoice)

    with open(file_path, 'rb') as f:
        file_data = f.read()
        file_name = f'invoice_{invoice["id"]}.pdf'
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)
        
    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
            server.send_message(msg)
            print("Email sent successfully!")   
    except Exception as e:
        print(f"Error sending email: {e}")
        raise RuntimeError(f"Failed to send email: {e}") from e
