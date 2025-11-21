import sys
import random
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


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


def generate_omr_sheet(df, filename="omr_sheet.pdf"):
    question_list = list(range(len(df)))
    random.shuffle(question_list)

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 50

    for idx, n in enumerate(question_list):
        question = df.question[n]
        shuffled = get_shuffled_options(df, n)

        c.drawString(50, y, f"Q{idx+1}: {question}")

        for i, (answer, is_correct) in enumerate(shuffled):
            pos_x = 70 + i * 100
            c.circle(pos_x, y - 15, 10)
            c.drawString(pos_x + 15, y - 20, chr(65 + i))

        y -= 50
        if y < 100:
            c.showPage()
            y = height - 50

    c.save()


# -------------------------
#  GUI APPLICATION
# -------------------------

class OMRGeneratorGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.csv_path = None
        self.setWindowTitle("TrueMark 0.5.0 alpha testing")
        self.setMinimumSize(400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Select a csv file:")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16px;")

        btn_choose = QPushButton("Select CSV File")
        btn_choose.setStyleSheet("font-size: 18px; padding: 10px;")
        btn_choose.clicked.connect(self.select_csv)

        btn_generate = QPushButton("Generate OMR PDF")
        btn_generate.setStyleSheet("font-size: 18px; padding: 10px;")
        btn_generate.clicked.connect(self.generate_pdf)

        layout.addWidget(self.label)
        layout.addWidget(btn_choose)
        layout.addWidget(btn_generate)

        self.setLayout(layout)

    # -------------------------
    #  Choose CSV
    # -------------------------
    def select_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open CSV File", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.csv_path = file_path
            self.label.setText(f"Selected: {file_path}")

    # -------------------------
    #  Generate OMR PDF
    # -------------------------
    def generate_pdf(self):
        if not self.csv_path:
            QMessageBox.warning(self, "No File", "Please select a CSV file first.")
            return

        try:
            df = pd.read_csv(self.csv_path, sep=None)
            generate_omr_sheet(df)
            QMessageBox.information(self, "Success", "OMR Sheet generated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate sheet:\n{e}")


# -------------------------
#  Main Entry
# -------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OMRGeneratorGUI()
    window.show()
    sys.exit(app.exec())
