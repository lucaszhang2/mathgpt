import tkinter as tk
from tkinter import scrolledtext
import wolframalpha
import requests

# Replace 'WOLFRAM_APP_ID' with your actual Wolfram Alpha App ID
WOLFRAM_APP_ID = 'WOLFRAM_APP_ID'
# Replace 'OPENAI_API_KEY' with your actual OpenAI API key
OPENAI_API_KEY = 'OPENAI_API_KEY'

# Wolfram Alpha client
client = wolframalpha.Client(WOLFRAM_APP_ID)

def get_wolfram_result(query):
    res = client.query(query)
    try:
        answer = next(res.results).text
    except StopIteration:
        answer = "No result found."
    return answer

def get_chatgpt_solution(problem, answer):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Here is a math problem: {problem}\nWolfram Alpha gives the following direct answer: {answer}\nCan you provide a step-by-step solution to this problem?"}
        ],
        "max_tokens": 500
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    
    if 'choices' in response_json:
        return response_json['choices'][0]['message']['content'].strip()
    else:
        return "Error: Unable to get response from ChatGPT."

def process_query():
    query = entry.get()
    wolfram_answer = get_wolfram_result(query)
    chatgpt_solution = get_chatgpt_solution(query, wolfram_answer)
    
    output_text.delete(1.0, tk.END)  # Clear previous output
    output_text.insert(tk.END, f"Step-by-Step Solution:\n{chatgpt_solution}\n")
    entry.delete(0, tk.END)

# Create main window
root = tk.Tk()
root.title("Math Problem Solver")

# Create entry widget for user query
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Create button to submit query
submit_button = tk.Button(root, text="Submit", command=process_query)
submit_button.pack(pady=5)

# Create scrolled text widget to display output
output_text = scrolledtext.ScrolledText(root, width=80, height=30)
output_text.pack(pady=10)

# Run the application
root.mainloop()
