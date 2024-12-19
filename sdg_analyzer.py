import json
import os
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, END

# Function to load and parse JSON data
def load_json_files():
    sdg_data = {}
    for i in range(1, 18):
        filename = f"SDG{i:02}.json"
        filepath = os.path.join(os.getcwd(), filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                sdg_data[filename] = json.load(file)
    return sdg_data

# Function to analyze the text against SDG data
def analyze_text(user_input, sdg_data):
    aligned_sdgs = []
    reasoning = []

    for sdg, content in sdg_data.items():
        sdg_number = sdg.replace("SDG", "").replace(".json", "")
        match_found = False
        reason = []

        def check_fields(field_data):
            nonlocal match_found
            if isinstance(field_data, dict):
                for value in field_data.values():
                    check_fields(value)
            elif isinstance(field_data, list):
                for item in field_data:
                    check_fields(item)
            elif isinstance(field_data, str):
                if field_data.lower() in user_input.lower():
                    match_found = True
                    reason.append(field_data)

        check_fields(content)

        if match_found:
            aligned_sdgs.append(f"SDG{sdg_number}")
            reasoning.append(f"Aligned with SDG{sdg_number} because of matches: {', '.join(reason)}.")

    return aligned_sdgs, reasoning

# Function to handle the analysis
def perform_analysis():
    user_input = input_text.get("1.0", END).strip()

    sdg_data = load_json_files()
    aligned_sdgs, reasoning = analyze_text(user_input, sdg_data)

    result_text.delete("1.0", END)
    if aligned_sdgs:
        result_text.insert(END, f"Aligned SDGs: {', '.join(aligned_sdgs)}\n\n")
        result_text.insert(END, "Reasoning:\n")
        for line in reasoning:
            result_text.insert(END, f"- {line}\n")
    else:
        result_text.insert(END, "No alignment found.\n")

# GUI Setup
root = Tk()
root.title("SDG Text Analyzer")

Label(root, text="Enter your text below:").pack()

input_text = Text(root, height=10, width=60)
input_text.pack()

Button(root, text="Analyze", command=perform_analysis).pack()

Label(root, text="Analysis Result:").pack()

result_text = Text(root, height=15, width=60, wrap="word")
result_text.pack()

scrollbar = Scrollbar(root, command=result_text.yview)
result_text.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

root.mainloop()
