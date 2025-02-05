import random
import string
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import winsound  # Windows sound library
import os  # For file path operations
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Class Definitions for Report Generation
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
# Class Definitions for Secure Communication
class AuthenticationServer:
    def __init__(self):
        self.authorized_units = {}

    def authenticate(self, unit_id, password):
        return self.authorized_units.get(unit_id) == password

    def authorize_qkd(self, unit_id):
        return unit_id in self.authorized_units


class QKDNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.shared_key = None

    def initiate_qkd(self, other_node):
        self.shared_key = self.generate_quantum_key()
        other_node.receive_key(self.shared_key)

    def generate_quantum_key(self):
        key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        return key

    def receive_key(self, key):
        self.shared_key = key


class EncryptionDecryptionModule:
    def __init__(self, qkd_node):
        self.qkd_node = qkd_node

    def encrypt_data(self, plaintext):
        encrypted_data = ''.join(
            chr(ord(char) ^ ord(self.qkd_node.shared_key[i % len(self.qkd_node.shared_key)])) for i, char in
            enumerate(plaintext))
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        decrypted_data = ''.join(
            chr(ord(char) ^ ord(self.qkd_node.shared_key[i % len(self.qkd_node.shared_key)])) for i, char in
            enumerate(encrypted_data))
        return decrypted_data


# Threat Analyzer to track authentication attempts
class ThreatAnalyzer:
    def __init__(self):
        self.unit_a_attempts = {'success': 0, 'failure': 0}
        self.unit_b_attempts = {'success': 0, 'failure': 0}

    def log_attempt(self, unit, success):
        if unit == 'UnitA':
            if success:
                self.unit_a_attempts['success'] += 1
            else:
                self.unit_a_attempts['failure'] += 1
        elif unit == 'UnitB':
            if success:
                self.unit_b_attempts['success'] += 1
            else:
                self.unit_b_attempts['failure'] += 1

    def display_graph(self):
        # Create the bar chart
        fig, ax = plt.subplots(figsize=(6, 4))
        attempts = ['Success', 'Failure']
        unit_a_values = [self.unit_a_attempts['success'], self.unit_a_attempts['failure']]
        unit_b_values = [self.unit_b_attempts['success'], self.unit_b_attempts['failure']]

        ax.bar(attempts, unit_a_values, label='Unit A', color='blue', width=0.4, align='center')
        ax.bar(attempts, unit_b_values, label='Unit B', color='red', width=0.4, align='edge')
        ax.set_ylabel('Number of Attempts')
        ax.set_title('Authentication Attempts for Unit A and B')
        ax.legend()

        return fig


# Combined GUI Application
class SecureCommunicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Military Secure Communication System")

        # Load and set background image
        self.bg_image = Image.open("im.png")  # Update with your image path
        self.bg_image = self.bg_image.resize(
            (self.root.winfo_screenwidth(), self.root.winfo_screenheight()), 
            Image.Resampling.LANCZOS
        )
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        self.report_generator = ReportGenerator()
        self.threat_analyzer = ThreatAnalyzer()  # Initialize Threat Analyzer

        # Components setup for Secure Communication
        self.auth_server = AuthenticationServer()
        self.auth_server.authorized_units = {'UnitA': 'password123', 'UnitB': 'password456'}

        self.unit_a_qkd_node = QKDNode('QKD Node A')
        self.unit_b_qkd_node = QKDNode('QKD Node B')

        self.unit_a_enc_dec = EncryptionDecryptionModule(self.unit_a_qkd_node)
        self.unit_b_enc_dec = EncryptionDecryptionModule(self.unit_b_qkd_node)

        # Setup UI
        self.setup_ui()
        self.update_graph()  # Display initial graph

    def setup_ui(self):
        # Unit A Authentication
        tk.Label(self.root, text="Unit A Authentication", bg='#4B5320', fg='white').grid(row=0, column=0, padx=10, pady=10)
        self.unit_a_password = tk.Entry(self.root, show='*')
        self.unit_a_password.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Authenticate Unit A", command=self.authenticate_unit_a).grid(row=0, column=2, padx=10, pady=10)

        # Unit B Authentication
        tk.Label(self.root, text="Unit B Authentication", bg='#4B5320', fg='white').grid(row=1, column=0, padx=10, pady=10)
        self.unit_b_password = tk.Entry(self.root, show='*')
        self.unit_b_password.grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Authenticate Unit B", command=self.authenticate_unit_b).grid(row=1, column=2, padx=10, pady=10)

        # QKD Initiation
        tk.Button(self.root, text="Initiate QKD", command=self.initiate_qkd).grid(row=2, column=1, padx=10, pady=10)

        # Encryption and Decryption Controls
        tk.Label(self.root, text="Enter Plaintext", bg='#4B5320', fg='white').grid(row=3, column=0, padx=10, pady=10)
        self.plaintext_entry = tk.Entry(self.root)
        self.plaintext_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Encrypt", command=self.encrypt_data).grid(row=4, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Decrypt", command=self.decrypt_data).grid(row=4, column=2, padx=10, pady=10)

        self.encrypted_label = tk.Label(self.root, text="Encrypted Data: ", bg='#4B5320', fg='white')
        self.encrypted_label.grid(row=5, column=1, padx=10, pady=10)

        self.decrypted_label = tk.Label(self.root, text="Decrypted Data: ", bg='#4B5320', fg='white')
        self.decrypted_label.grid(row=6, column=1, padx=10, pady=10)

        # Report Generation Controls
        tk.Label(self.root, text="Message Type", bg='#4B5320', fg='white').grid(row=7, column=0, padx=10, pady=10)
        self.message_type_entry = tk.Entry(self.root)
        self.message_type_entry.grid(row=7, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Message Content", bg='#4B5320', fg='white').grid(row=8, column=0, padx=10, pady=10)
        self.message_content_entry = tk.Entry(self.root)
        self.message_content_entry.grid(row=8, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Encryption Status", bg='#4B5320', fg='white').grid(row=9, column=0, padx=10, pady=10)
        self.encryption_status_entry = tk.Entry(self.root)
        self.encryption_status_entry.grid(row=9, column=1, padx=10, pady=10)

        tk.Label(self.root, text="QKD Status", bg='#4B5320', fg='white').grid(row=10, column=0, padx=10, pady=10)
        self.qkd_status_entry = tk.Entry(self.root)
        self.qkd_status_entry.grid(row=10, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Intrusion Alerts", bg='#4B5320', fg='white').grid(row=11, column=0, padx=10, pady=10)
        self.intrusion_alerts_entry = tk.Entry(self.root)
        self.intrusion_alerts_entry.grid(row=11, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Generate Report", command=self.generate_report).grid(row=12, column=1, padx=10, pady=10)

    def authenticate_unit_a(self):
        password = self.unit_a_password.get()
        if self.auth_server.authenticate('UnitA', password):
            self.threat_analyzer.log_attempt('UnitA', True)
            messagebox.showinfo("Authentication", "Unit A Authenticated Successfully")
        else:
            self.threat_analyzer.log_attempt('UnitA', False)
            self.play_fire_alarm()
            messagebox.showerror("Authentication", "Authentication Failed for Unit A.")
        self.update_graph()

    def authenticate_unit_b(self):
        password = self.unit_b_password.get()
        if self.auth_server.authenticate('UnitB', password):
            self.threat_analyzer.log_attempt('UnitB', True)
            messagebox.showinfo("Authentication", "Unit B Authenticated Successfully")
        else:
            self.threat_analyzer.log_attempt('UnitB', False)
            self.play_fire_alarm()
            messagebox.showerror("Authentication", "Authentication Failed for Unit B.")
        self.update_graph()

    def play_fire_alarm(self):
        # Run alarm sound in a separate thread
        def alarm_thread():
            alarm_path = "alarm.wav"  # Update with the correct path if needed
            if os.path.exists(alarm_path):
                winsound.PlaySound(alarm_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                messagebox.showerror("Error", "Emergency alarm sound file not found!")
        
        threading.Thread(target=alarm_thread, daemon=True).start()

    def initiate_qkd(self):
        self.unit_a_qkd_node.initiate_qkd(self.unit_b_qkd_node)
        messagebox.showinfo("QKD Initiation", "QKD Initiated Between Unit A and Unit B")

    def encrypt_data(self):
        plaintext = self.plaintext_entry.get()
        encrypted_data = self.unit_a_enc_dec.encrypt_data(plaintext)
        self.encrypted_label.config(text=f"Encrypted Data: {encrypted_data}")

    def decrypt_data(self):
        encrypted_data = self.encrypted_label.cget("text").replace("Encrypted Data: ", "")
        decrypted_data = self.unit_a_enc_dec.decrypt_data(encrypted_data)
        self.decrypted_label.config(text=f"Decrypted Data: {decrypted_data}")

    def generate_report(self):
        message_type = self.message_type_entry.get()
        message_content = self.message_content_entry.get()
        encryption_status = self.encryption_status_entry.get()
        qkd_status = self.qkd_status_entry.get()
        intrusion_alerts = self.intrusion_alerts_entry.get()

        self.report_generator.add_data(
            message_type,
            message_content,
            encryption_status,
            qkd_status,
            intrusion_alerts
        )

        # Ask for password to encrypt PDF
        password = simpledialog.askstring("PDF Password", "Enter password to encrypt the PDF report:")
        if password:
            self.report_generator.generate_pdf_report("report.pdf", password)
            messagebox.showinfo("Report Generation", "Report generated and encrypted successfully!")

    def update_graph(self):
        # Display updated threat analysis graph
        fig = self.threat_analyzer.display_graph()
        if hasattr(self, 'graph_canvas'):
            self.graph_canvas.get_tk_widget().destroy()  # Remove old graph
        self.graph_canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().grid(row=13, columnspan=3, padx=10, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = SecureCommunicationApp(root)
    root.mainloop()
