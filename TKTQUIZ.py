import sqlite3
from tkinter import *
from tkinter import messagebox


def setup_database():
    conn = sqlite3.connect('quiz.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY,
                    question TEXT,
                    option1 TEXT,
                    option2 TEXT,
                    option3 TEXT,
                    option4 TEXT,
                    correct_option INTEGER)''')
    conn.commit()
    
   
    sample_questions = [
        ("What is the capital of France?", "Berlin", "Madrid", "Paris", "Rome", 3),
        ("What is 2 + 2?", "3", "4", "5", "6", 2),
        ("Which programming language is used for AI?", "Python", "Java", "C++", "Ruby", 1)
    ]
    cur.executemany('''INSERT OR IGNORE INTO questions 
                        (question, option1, option2, option3, option4, correct_option) 
                        VALUES (?, ?, ?, ?, ?, ?)''', sample_questions)
    conn.commit()
    conn.close()


def fetch_question(qid):
    conn = sqlite3.connect('quiz.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions WHERE id = ?", (qid,))
    question = cur.fetchone()
    conn.close()
    return question


def submit_answer():
    global current_question_id, score
    selected = selected_option.get()
    
    if selected == 0:
        messagebox.showwarning("No Selection", "Please select an option!")
        return
    
    correct_option = current_question[6]
    if selected == correct_option:
        score += 1
    
    current_question_id += 1
    load_question()


def load_question():
    global current_question
    current_question = fetch_question(current_question_id)
    
    if current_question:
        question_label.config(text=current_question[1])
        option1_rbtn.config(text=current_question[2], value=1)
        option2_rbtn.config(text=current_question[3], value=2)
        option3_rbtn.config(text=current_question[4], value=3)
        option4_rbtn.config(text=current_question[5], value=4)
        selected_option.set(0)
    else:
        messagebox.showinfo("Quiz Complete", f"Quiz over! Your score: {score}")
        root.quit()


root = Tk()
root.title("Quiz Application")

current_question_id = 1
current_question = None
score = 0


question_label = Label(root, text="", font=("Arial", 14), wraplength=400)
question_label.pack(pady=20)

selected_option = IntVar()

option1_rbtn = Radiobutton(root, text="", variable=selected_option, value=1, font=("Arial", 12))
option1_rbtn.pack(anchor=W, padx=20)
option2_rbtn = Radiobutton(root, text="", variable=selected_option, value=2, font=("Arial", 12))
option2_rbtn.pack(anchor=W, padx=20)
option3_rbtn = Radiobutton(root, text="", variable=selected_option, value=3, font=("Arial", 12))
option3_rbtn.pack(anchor=W, padx=20)
option4_rbtn = Radiobutton(root, text="", variable=selected_option, value=4, font=("Arial", 12))
option4_rbtn.pack(anchor=W, padx=20)

submit_button = Button(root, text="Submit", command=submit_answer, font=("Arial", 12))
submit_button.pack(pady=20)


setup_database()
load_question()

root.mainloop()
