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
import matplotlib.animation as animation
import numpy as np


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
        reader = PdfReader(filename)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)
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
        self.threat_direction = []  # Track threat directions for wave

    def log_attempt(self, unit, success):
        if unit == 'UnitA':
            if success:
                self.unit_a_attempts['success'] += 1
            else:
                self.unit_a_attempts['failure'] += 1
                self.threat_direction.append(1)
        elif unit == 'UnitB':
            if success:
                self.unit_b_attempts['success'] += 1
            else:
                self.unit_b_attempts['failure'] += 1
                self.threat_direction.append(-1)

    def display_graph(self):
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

    def create_live_threat_visualization(self):
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.set_xlim(0, 10)
        ax.set_ylim(-1, 1)
        ax.set_title("Live Threat Movement")
        self.line, = ax.plot([], [], lw=2)
        return fig

    def update_threat_movement(self):
        x = np.linspace(0, 10, 1000)
        y = np.sin(2 * np.pi * (x - 0.01 * time.time()))
        self.line.set_data(x, y)



# Combined GUI Application
class SecureCommunicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Military Secure Communication System")

        self.bg_image = Image.open("im.png")
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        self.report_generator = ReportGenerator()
        self.threat_analyzer = ThreatAnalyzer()

        self.auth_server = AuthenticationServer()
        self.auth_server.authorized_units = {'UnitA': 'password123', 'UnitB': 'password456'}

        self.unit_a_qkd_node = QKDNode('QKD Node A')
        self.unit_b_qkd_node = QKDNode('QKD Node B')

        self.unit_a_enc_dec = EncryptionDecryptionModule(self.unit_a_qkd_node)
        self.unit_b_enc_dec = EncryptionDecryptionModule(self.unit_b_qkd_node)

        self.setup_ui()
        self.update_graph()

    def setup_ui(self):
        tk.Label(self.root, text="Unit A Authentication", bg='#4B5320', fg='white').grid(row=0, column=0, padx=10, pady=10)
        self.unit_a_password = tk.Entry(self.root, show='*')
        self.unit_a_password.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Authenticate Unit A", command=self.authenticate_unit_a).grid(row=0, column=2, padx=10, pady=10)

        tk.Label(self.root, text="Unit B Authentication", bg='#4B5320', fg='white').grid(row=1, column=0, padx=10, pady=10)
        self.unit_b_password = tk.Entry(self.root, show='*')
        self.unit_b_password.grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Authenticate Unit B", command=self.authenticate_unit_b).grid(row=1, column=2, padx=10, pady=10)

        tk.Button(self.root, text="Initiate QKD", command=self.initiate_qkd).grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        tk.Button(self.root, text="Generate Report", command=self.generate_report).grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        
        self.canvas = FigureCanvasTkAgg(self.threat_analyzer.display_graph(), master=self.root)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=3)

        self.threat_canvas = FigureCanvasTkAgg(self.threat_analyzer.create_live_threat_visualization(self.canvas), master=self.root)
        self.threat_canvas.get_tk_widget().grid(row=5, column=0, columnspan=3)

    def update_graph(self):
        self.canvas.figure = self.threat_analyzer.display_graph()
        self.canvas.draw()

        self.threat_canvas.figure = self.threat_analyzer.create_live_threat_visualization(self.canvas)
        self.threat_canvas.draw()
    def play_fire_alarm(self):
        # Ensure the alarm.wav file is in the same directory or update with full path
        alarm_path = "alarm.wav"
        if os.path.exists(alarm_path):
            winsound.PlaySound(alarm_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            messagebox.showerror("Error", "Alarm sound file not found.")


    def authenticate_unit_a(self):
        password = self.unit_a_password.get()
        success = self.auth_server.authenticate('UnitA', password)
        self.threat_analyzer.log_attempt('UnitA', success)
        self.update_graph()
        if success:
            messagebox.showinfo("Success", "Unit A authenticated successfully!")
        else:
            messagebox.showerror("Failure", "Authentication failed for Unit A.")

    def authenticate_unit_b(self):
        password = self.unit_b_password.get()
        success = self.auth_server.authenticate('UnitB', password)
        self.threat_analyzer.log_attempt('UnitB', success)
        self.update_graph()
        if success:
            messagebox.showinfo("Success", "Unit B authenticated successfully!")
        else:
            messagebox.showerror("Failure", "Authentication failed for Unit B.")

    def initiate_qkd(self):
        self.unit_a_qkd_node.initiate_qkd(self.unit_b_qkd_node)
        messagebox.showinfo("QKD Status", "QKD has been initiated between Unit A and B.")

    def generate_report(self):
        filename = "report.pdf"
        password = simpledialog.askstring("Password", "Enter a password for the PDF:", show='*')
        if password:
            self.report_generator.generate_pdf_report(filename, password)
            messagebox.showinfo("Report Generated", f"PDF report saved as {filename}")

root = tk.Tk()
app = SecureCommunicationApp(root)
root.mainloop()
