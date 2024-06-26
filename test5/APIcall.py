import requests
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import pytesseract

# Configure OpenAI API key
API_KEY = "API key"
API_URL = "https://api.openai.com/v1/chat/completions"

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # path where you install tesseract

def call_chatgpt(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    }
    response = requests.post(API_URL, headers=headers, json=data)
    response_json = response.json()
    
    if "choices" in response_json:
        return response_json["choices"][0]["message"]["content"].strip()
    else:
        print("Error:", response_json)  # Print the entire response for debugging
        return "Error: Unable to get response from OpenAI API"

def ocr_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

class APIcall:
    def __init__(self, master):
        self.master = master
        self.steps = []
        self.current_step_index = 0
        self.create_widgets()

    def create_widgets(self):
        instruction_label = tk.Label(self.master, text="Please enter your problem below or upload an image of the problem")
        instruction_label.pack(pady=5)

        self.entry = tk.Entry(self.master, width=50)
        self.entry.pack(pady=10)

        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=5)

        left_button = tk.Button(button_frame, text="Hint", command=self.hint_action)
        left_button.pack(side=tk.LEFT, padx=5)

        middle_button = tk.Button(button_frame, text="Step-by-Step", command=self.step_action)
        middle_button.pack(side=tk.LEFT, padx=5)

        right_button = tk.Button(button_frame, text="Direct Answer", command=self.direct_answer_action)
        right_button.pack(side=tk.LEFT, padx=5)

        self.upload_button = tk.Button(self.master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=5)

        self.response_text = tk.Text(self.master, height=10, width=60)
        self.response_text.pack(pady=10)

        # Next Step button (initially hidden)
        self.next_step_button = tk.Button(button_frame, text="Next Step", command=self.next_step_action)
        self.next_step_button.pack(pady=5)
        self.next_step_button.pack_forget()  # Hide the button initially

    def hint_action(self):
        prompt = self.entry.get()
        hint_prompt = f"Provide a hint for the following problem: {prompt}"
        response = call_chatgpt(hint_prompt)
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(tk.END, response)

    def step_action(self):
        prompt = self.entry.get()
        step_by_step_prompt = f"Provide a step-by-step solution for the following problem: {prompt}"
        response = call_chatgpt(step_by_step_prompt)

        # Clear previous responses
        self.response_text.delete(1.0, tk.END)

        # Improved step parsing
        self.steps = self.parse_steps(response)
        self.current_step_index = 0

        if self.steps:
            self.show_next_step()
            self.next_step_button.pack(pady=5)  # Show the button
    
    def parse_steps(self, response):
        steps = []
        try:
            lines = response.split('\n')
            current_step = ""
            for line in lines:
                if line.strip().lower().startswith('step'):
                    if current_step:
                        steps.append(current_step.strip())
                    current_step = line.strip()
                else:
                    current_step += ' ' + line.strip()
            if current_step:
                steps.append(current_step.strip())
            return steps
        except Exception as e:
            print(f"Error parsing steps: {e}")
            return [response]  # Fallback to showing the entire response as one step

    def show_next_step(self):
        if self.current_step_index < len(self.steps):
            self.response_text.insert(tk.END, f"{self.steps[self.current_step_index]}\n")
            self.current_step_index += 1
        if self.current_step_index >= len(self.steps):
            self.next_step_button.pack_forget()  # Hide the button when all steps are shown
    
    def next_step_action(self):
        self.show_next_step()

    def direct_answer_action(self):
        prompt = self.entry.get()
        direct_answer_prompt = f"Provide a direct answer to the following problem: {prompt}"
        response = call_chatgpt(direct_answer_prompt)
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(tk.END, response)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            text = ocr_from_image(file_path)
            response = call_chatgpt(text)
            self.response_text.delete(1.0, tk.END)
            self.response_text.insert(tk.END, response)