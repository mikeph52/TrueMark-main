import pandas as pd
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Load CSV
df = pd.read_csv("desktop_app/data/exam_sample_2.csv")
question_list = list(range(len(df)))
random.shuffle(question_list)

# Shuffle answers, store mapping
def get_shuffled_options(n):
    choices = [
        (df.choice_correct[n], 'correct'),
        (df.choice_1[n], ''),
        (df.choice_2[n], ''),
        (df.choice_3[n], ''),
    ]
    random.shuffle(choices)
    return choices

def generate_omr_sheet(df, question_list, filename="omr_sheet2.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 50

    for idx, n in enumerate(question_list):
        question = df.question[n]
        shuffled = get_shuffled_options(n)
        c.drawString(50, y, f"Q{idx+1}: {question}")
        for i, (answer, is_correct) in enumerate(shuffled):
            pos_x = 70 + i*100
            c.circle(pos_x, y-15, 10)
            c.drawString(pos_x+15, y-20, chr(65+i))  # A/B/C/D
            # Optionally, output the answer text
            # c.drawString(pos_x + 30, y-20, answer)
        y -= 50
        if y < 100:
            c.showPage()
            y = height - 50
    c.save()

generate_omr_sheet(df, question_list)
