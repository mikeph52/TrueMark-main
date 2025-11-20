import pandas as pd
import random

# Load CSV
df = pd.read_csv("desktop_app/multiple_choice_exam_sample.csv")

def quiz():
    idx = random.randint(0, len(df) - 1)
    question = df.question[idx]
    answers = [df.choice_correct[idx],df.choice_1[idx],df.choice_2[idx],df.choice_3[idx]]

    # shuffle
    random.shuffle(answers)

    print("\n" + question)
    print("A.", answers[0])
    print("B.", answers[1])
    print("C.", answers[2])
    print("D.", answers[3])

    answer_input = input("Type the correct answer: ")

    if answer_input.strip() == df.choice_correct[idx]:
        print("You're correct!")
    else:
        print("You're wrong.")

# Run quiz
print("This is a good quiz:\n")
quiz()
