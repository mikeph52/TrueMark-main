import sys
import random
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QFileDialog, QMessageBox, QSpinBox, QHBoxLayout
)
from PySide6.QtCore import Qt

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import qr
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing

# -------------------------
#  OMR GENERATION FUNCTIONS
# -------------------------

def get_shuffled_options(df, n):
    choices = [
        (df.choice_correct[n], 'correct'),
        (df.choice_1[n], ''),
        (df.choice_2[n], ''),
        (df.choice_3[n], ''),
    ]
    random.shuffle(choices)
    return choices

def generate_omr_sheet(df, filename, set_label="A"):
    question_list = list(range(len(df)))
    random.shuffle(question_list)

    answer_key = []

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y_start = height - 80  # leave space for QR at top
    y = y_start

    # ---- QR CODE (ANSWER KEY) ----
    # For QR, we can generate it dynamically after shuffling questions
    encoded_answers_list = []

    for idx, n in enumerate(question_list):
        shuffled = get_shuffled_options(df, n)
        correct_letter = chr(65 + [i for i, (_, is_correct) in enumerate(shuffled) if is_correct == 'correct'][0])
        encoded_answers_list.append(f"Q{idx+1}={correct_letter}")

    encoded_answers = f"SET={set_label}|" + "|".join(encoded_answers_list)

    qr_code = qr.QrCodeWidget(encoded_answers)
    bounds = qr_code.getBounds()
    qr_width = bounds[2] - bounds[0]
    qr_height = bounds[3] - bounds[1]
    d = Drawing(50, 50, transform=[50/qr_width, 0, 0, 50/qr_height, 0, 0])
    d.add(qr_code)
    renderPDF.draw(d, c, width - 100, height - 70)  # top-right corner

    # ---- QUESTIONS ----
    for idx, n in enumerate(question_list):
        question = df.question[n]
        shuffled = get_shuffled_options(df, n)

        c.drawString(50, y, f"Q{idx+1}: {question}")

        correct_letter = None
        for i, (answer, is_correct) in enumerate(shuffled):
            pos_x = 70 + i * 100
            c.circle(pos_x, y - 15, 10)
            c.drawString(pos_x + 15, y - 20, chr(65 + i))
            if is_correct == 'correct':
                correct_letter = chr(65 + i)

        y -= 50
        if y < 120:
            c.showPage()
            # Re-draw QR code on new page
            renderPDF.draw(d, c, width - 100, height - 70)
            y = y_start

    c.save()

def generate_multiple_sets(df, num_sets=3):
    for i in range(num_sets):
        set_label = chr(65 + i)  # A, B, C...
        filename = f"omr_set_{set_label}.pdf"
        generate_omr_sheet(df, filename, set_label)

# -------------------------
#  GUI APPLICATION
# -------------------------

class OMRGeneratorGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.csv_path = None
        self.setWindowTitle("TrueMark 0.7.0 Alpha Testing by mikeph_")
        self.setMinimumSize(450, 250)

        layout = QVBoxLayout()

        self.label = QLabel("Select a CSV file:")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16px;")

        btn_choose = QPushButton("Select CSV File")
        btn_choose.setStyleSheet("font-size: 16px; padding: 8px;")
        btn_choose.clicked.connect(self.select_csv)

        # Number of sets input
        sets_layout = QHBoxLayout()
        sets_label = QLabel("Number of Sets:")
        sets_label.setStyleSheet("font-size: 14px;")
        self.sets_input = QSpinBox()
        self.sets_input.setMinimum(1)
        self.sets_input.setMaximum(10)
        self.sets_input.setValue(3)
        sets_layout.addWidget(sets_label)
        sets_layout.addWidget(self.sets_input)

        btn_generate = QPushButton("Generate Single OMR PDF")
        btn_generate.setStyleSheet("font-size: 16px; padding: 8px;")
        btn_generate.clicked.connect(self.generate_pdf)

        btn_generate_multi = QPushButton("Generate Multiple Sets")
        btn_generate_multi.setStyleSheet("font-size: 16px; padding: 8px;")
        btn_generate_multi.clicked.connect(self.generate_multiple)

        layout.addWidget(self.label)
        layout.addWidget(btn_choose)
        layout.addLayout(sets_layout)
        layout.addWidget(btn_generate)
        layout.addWidget(btn_generate_multi)

        self.setLayout(layout)

    def select_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open CSV File", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.csv_path = file_path
            self.label.setText(f"Selected: {file_path}")

    def generate_pdf(self):
        if not self.csv_path:
            QMessageBox.warning(self, "No File", "Please select a CSV file first.")
            return
        try:
            df = pd.read_csv(self.csv_path, sep=None, engine="python")
            generate_omr_sheet(df, filename="omr_set_A.pdf", set_label="A")
            QMessageBox.information(self, "Success", "OMR Sheet generated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate sheet:\n{e}")

    def generate_multiple(self):
        if not self.csv_path:
            QMessageBox.warning(self, "No File", "Please select a CSV file first.")
            return
        try:
            num_sets = self.sets_input.value()
            df = pd.read_csv(self.csv_path, sep=None, engine="python")
            generate_multiple_sets(df, num_sets=num_sets)
            QMessageBox.information(
                self, "Success", f"{num_sets} OMR sets generated successfully!"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

# -------------------------
#  Main Entry
# -------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OMRGeneratorGUI()
    window.show()
    sys.exit(app.exec())
