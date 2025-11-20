import pandas as pd
import random

# Load CSV
df = pd.read_csv("desktop_app/data/exam_sample_2.csv")

question_list = list(range(len(df)))
random.shuffle(question_list)
#question_n = list(range(len(df))) string to int

def quiz(n):
    question = df.question[n]
    answers = [df.choice_correct[n],df.choice_1[n],df.choice_2[n],df.choice_3[n]]

    # shuffle
    random.shuffle(answers)

    print("\n" + question)
    print("A.", answers[0])
    print("B.", answers[1])
    print("C.", answers[2])
    print("D.", answers[3])

# Run quiz
def main():
    print("TrueMark proof of concept 0.3.0\n by mikeph_ 2025")

    for n in question_list:
        quiz(n)

    print("\nGood Luck!")

main()