import requests
import json
import tkinter as tk
from tkinter import scrolledtext

# Replace 'your-api-key' with your actual OpenAI API key
api_key = 'your-api-key'
api_url = 'https://api.openai.com/v1/chat/completions'
model = 'gpt-4'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

def chat_with_gpt(prompt, max_tokens=150):
    data = {
        'model': model,
        'messages': [{"role": "user", "content": prompt}],
        'max_tokens': max_tokens,
        'temperature': 0.7
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        if response.status_code == 429:
            return "Error: You have exceeded your quota. Please check your plan and billing details."
        else:
            return f"Error: {response.status_code} - {response.text}"
    response_json = response.json()
    if 'choices' not in response_json:
        return f"Error: {response_json}"
    return response_json['choices'][0]['message']['content'].strip()

def send_message():
    user_input = user_entry.get()
    chat_log.insert(tk.END, "You: " + user_input + "\n")
    response = chat_with_gpt(user_input)
    chat_log.insert(tk.END, "ChatGPT: " + response + "\n")
    user_entry.delete(0, tk.END)

# Create the main window
window = tk.Tk()
window.title("ChatGPT Interface")

# Create the chat log
chat_log = scrolledtext.ScrolledText(window, wrap=tk.WORD)
chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create the user input entry
user_entry = tk.Entry(window)
user_entry.pack(padx=10, pady=10, fill=tk.X)
user_entry.bind("<Return>", lambda event: send_message())

# Create the send button
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack(padx=10, pady=10)

# Start the main event loop
window.mainloop()
