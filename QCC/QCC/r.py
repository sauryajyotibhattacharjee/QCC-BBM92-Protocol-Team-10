import random
import string
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk
from tkinter import messagebox, simpledialog


# Class Definitions

class ReportGenerator:
    def __init__(self):
        self.data = []

    def add_data(self, message_type, message_content, encryption_status, qkd_status, intrusion_alerts):
        self.data.append({
            'Type': message_type,
            'Content': message_content,
            'Encryption': encryption_status,
            'QKD Status': qkd_status,
            'Intrusion Alerts': intrusion_alerts
        })

    def generate_pdf_report(self, filename, password):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Secure Communication Report", 0, 1, 'C')
        pdf.ln(10)

        # Table Header
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(30, 10, "Type", 1)
        pdf.cell(80, 10, "Content", 1)
        pdf.cell(40, 10, "Encryption", 1)
        pdf.cell(40, 10, "QKD Status", 1)
        pdf.cell(0, 10, "Intrusion Alerts", 1)
        pdf.ln()

        # Table Data
        pdf.set_font("Arial", '', 12)
        for item in self.data:
            pdf.cell(30, 10, item['Type'], 1)
            pdf.cell(80, 10, item['Content'], 1)
            pdf.cell(40, 10, item['Encryption'], 1)
            pdf.cell(40, 10, item['QKD Status'], 1)
            pdf.cell(0, 10, item['Intrusion Alerts'], 1)
            pdf.ln()

        # Save PDF
        pdf.output(filename)

        # Encrypt PDF with a password
        self.encrypt_pdf(filename, password)

    def encrypt_pdf(self, filename, password):
        # Open existing PDF
        reader = PdfReader(filename)
        writer = PdfWriter()

        # Add all pages to writer
        for page in reader.pages:
            writer.add_page(page)

        # Encrypt PDF
        writer.encrypt(password)

        # Save encrypted PDF
        with open(filename, "wb") as f:
            writer.write(f)

# GUI Application for Report Generation
class ReportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Communication Report Generator")
        self.report_generator = ReportGenerator()

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        # Message Type Entry
        tk.Label(self.root, text="Message Type").grid(row=0, column=0, padx=10, pady=10)
        self.message_type_entry = tk.Entry(self.root)
        self.message_type_entry.grid(row=0, column=1, padx=10, pady=10)

        # Message Content Entry
        tk.Label(self.root, text="Message Content").grid(row=1, column=0, padx=10, pady=10)
        self.message_content_entry = tk.Entry(self.root)
        self.message_content_entry.grid(row=1, column=1, padx=10, pady=10)

        # Encryption Status Entry
        tk.Label(self.root, text="Encryption Status").grid(row=2, column=0, padx=10, pady=10)
        self.encryption_status_entry = tk.Entry(self.root)
        self.encryption_status_entry.grid(row=2, column=1, padx=10, pady=10)

        # QKD Status Entry
        tk.Label(self.root, text="QKD Status").grid(row=3, column=0, padx=10, pady=10)
        self.qkd_status_entry = tk.Entry(self.root)
        self.qkd_status_entry.grid(row=3, column=1, padx=10, pady=10)

        # Intrusion Alerts Entry
        tk.Label(self.root, text="Intrusion Alerts").grid(row=4, column=0, padx=10, pady=10)
        self.intrusion_alerts_entry = tk.Entry(self.root)
        self.intrusion_alerts_entry.grid(row=4, column=1, padx=10, pady=10)

        # Add Data Button
        tk.Button(self.root, text="Add Data", command=self.add_data).grid(row=5, column=1, padx=10, pady=10)

        # Generate Report Button
        tk.Button(self.root, text="Generate Report", command=self.generate_report).grid(row=6, column=1, padx=10, pady=10)

    def add_data(self):
        message_type = self.message_type_entry.get()
        message_content = self.message_content_entry.get()
        encryption_status = self.encryption_status_entry.get()
        qkd_status = self.qkd_status_entry.get()
        intrusion_alerts = self.intrusion_alerts_entry.get()

        # Add data to report generator
        self.report_generator.add_data(message_type, message_content, encryption_status, qkd_status, intrusion_alerts)
        messagebox.showinfo("Success", "Data added to the report successfully!")

    def generate_report(self):
        # Get filename and password from the user
        filename = "Secure_Communication_Report.pdf"
        password = simpledialog.askstring("Input", "Enter a password to encrypt the report:", show='*')

        if password:
            # Generate PDF Report
            self.report_generator.generate_pdf_report(filename, password)
            messagebox.showinfo("Success", f"Report generated and saved as {filename}!")
        else:
            messagebox.showerror("Error", "Password is required to generate the report!")

# Main Application Loop
if __name__ == "__main__":
    root = tk.Tk()
    app = ReportApp(root)
    root.mainloop()
