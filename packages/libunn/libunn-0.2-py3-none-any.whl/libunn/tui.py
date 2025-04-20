import sys
import uuid
def yesno(question, quitProgram=False):
    options = "[y/n]"
    if quitProgram == True:
        options = "[y/n/q] "
    while True:
        res = input(f"{question} {options}: ").strip().lower()
        if res == 'y':
            return True
        elif res == 'n':
            return False
        elif res == 'q' and quitProgram:
            exit(0)
        else:
            print("Invalid option, try again.")

def pick(questions, quitProgram=False):
    qs = {i+1: question for i, question in enumerate(questions)}
    num_options = len(qs)

    if quitProgram:
        num_options += 1
        qs[num_options] = "Quit"

    for num, question in qs.items():
        print(f"{num}. {question}")
    
    while True:
        try:
            res = int(input(f"Your choice [1-{num_options}]: "))
            if res == num_options and quitProgram:
                sys.exit(0)
            elif res in qs:
                return qs[res] 
            else:
                print("Invalid option, try again.")
        except ValueError:
            print("Please enter a valid number.")

