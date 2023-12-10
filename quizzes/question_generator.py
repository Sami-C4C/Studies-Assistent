import sqlite3
import openai

# Set up your API key and model
api_key = "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"

MODEL = "gpt-3.5-turbo"


# Function to interact with GPT-3 for generating quizzes
def generate_quiz(theme, num_questions, num_options):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful quiz generator."},
            {"role": "user",
             "content": f"Erstelle mir ein Quiz über das Thema {theme}, mit {num_questions} Fragen. Jede Frage hat {num_options} Antwortmoeglichkeiten."},
        ],
        temperature=0,
    )
    return response.choices[0].message.content


# Capture user input
user_input_theme = input("Das Thema: ")
user_input_questions = input("Die Anzahl von Fragen: ")
user_input_options = input("Die Anzahl von Antwortmoeglichkeiten: ")

# Generate quiz based on user input
quiz_content = generate_quiz(user_input_theme, user_input_questions, user_input_options)

# Connect to SQLite database
conn = sqlite3.connect('quiz_database.db')
c = conn.cursor()

# Create a table for quizzes if it doesn't exist
c.execute(
    '''CREATE TABLE IF NOT EXISTS quizzes (id INTEGER PRIMARY KEY AUTOINCREMENT, theme TEXT, question TEXT, options TEXT, correct_answer TEXT)''')

# Insert the generated quiz into the database
c.execute('''INSERT INTO quizzes (theme, question, options, correct_answer) VALUES (?, ?, ?, ?)''',
          (user_input_theme, quiz_content, "options go here", "correct answer goes here"))

# Commit changes and close the connection
conn.commit()
conn.close()
