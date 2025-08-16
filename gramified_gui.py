#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, ttk
from tkhtmlview import HTMLLabel
from duckduckgo_search import DDGS
import ollama
import os
from datetime import datetime
from threading import Thread
import time

# Constants
EXPORT_DIR = os.path.expanduser("~/gramified_chats")
os.makedirs(EXPORT_DIR, exist_ok=True)
AVAILABLE_MODELS = ["mistral", "llama3", "phi", "gemma", "qwen", "codellama"]
chat_log = []
chat_html = []

# GUI setup
root = tk.Tk()
root.title("Gramified Local Chat")
root.configure(bg="#1e1e1e")
root.attributes('-fullscreen', True)

def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)
root.bind("<Escape>", exit_fullscreen)

# Model selection
selected_model = tk.StringVar(value="mistral")
tk.Label(root, text="Select Model:", bg="#1e1e1e", fg="white", font=("Segoe UI", 10)).pack(padx=10, anchor="w")
model_dropdown = ttk.Combobox(root, textvariable=selected_model, values=AVAILABLE_MODELS, state="readonly")
model_dropdown.pack(padx=10, pady=(0, 5), anchor="w")

# Web search toggle
web_toggle = tk.BooleanVar()
web_checkbox = tk.Checkbutton(root, text="Live Web Mode", variable=web_toggle, bg="#1e1e1e", fg="white", selectcolor="#1e1e1e")
web_checkbox.pack(padx=10, pady=(0, 5), anchor="w")

# Diagnostic mode toggle
diagnostic_toggle = tk.BooleanVar()
diagnostic_checkbox = tk.Checkbutton(root, text="Diagnostic Mode (detailed export)", variable=diagnostic_toggle, bg="#1e1e1e", fg="white", selectcolor="#1e1e1e")
diagnostic_checkbox.pack(padx=10, pady=(0, 10), anchor="w")

# Chat area
chat_frame = tk.Frame(root, bg="#1e1e1e")
chat_frame.pack(padx=10, pady=(10, 0), fill=tk.BOTH, expand=True)
chat_area = HTMLLabel(chat_frame, html="", background="#1e1e1e", foreground="white", font=("Segoe UI", 11), width=150)
chat_area.pack(fill=tk.BOTH, expand=True)

# Input field
user_input = tk.Text(root, height=3, bg="#2c2c2c", fg="#cfcfcf", insertbackground="white", font=("Segoe UI", 11), borderwidth=0)
user_input.pack(padx=10, pady=(10, 0), fill=tk.X)

# Typing label
typing_label = tk.Label(root, text="", fg="#aaaaaa", bg="#1e1e1e", font=("Segoe UI", 10, "italic"))
typing_label.pack(padx=10, pady=(5, 0), anchor="w")

# Save chat
def save_chat(auto=False):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"chat_{timestamp}.txt"
    path = os.path.join(EXPORT_DIR, filename)

    if diagnostic_toggle.get():
        content = "\n\n".join(chat_log)
    else:
        content = "\n\n".join([entry for entry in chat_log if not entry.startswith("[Injected:")])

    try:
        with open(path, "w") as f:
            f.write(content)
        if not auto:
            messagebox.showinfo("Export Complete", f"Chat saved to:\n{path}")
    except Exception as e:
        if not auto:
            messagebox.showerror("Export Failed", str(e))

def on_quit():
    save_chat(auto=True)
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_quit)

def clear_chat():
    global chat_log, chat_html
    chat_log = []
    chat_html = []
    chat_area.set_html("")

# Typing animation
typing = True
def animate_typing():
    dots = ""
    while typing:
        for i in range(4):
            if not typing:
                break
            dots = "." * i
            typing_label.config(text=f"🤖 {selected_model.get().capitalize()} is typing{dots}")
            time.sleep(0.5)

# Web fetch
def fetch_web_results(query):
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            return "\n\n".join([r["body"] for r in results if "body" in r])
    except Exception as e:
        return f"[Web Search Error] {e}"

# Append chat
def append_chat(role, name, content):
    global chat_html
    timestamp = datetime.now().strftime("%H:%M")
    tag = "🧑" if role == "user" else "🤖"
    color = "#43d1af" if role == "user" else "#91b9f4"
    html_block = (
        f"<span style='color:{color};'><b>{tag} {name} [{timestamp}]</b></span><br>"
        f"<span style='color:{color};'>{content}</span><br><br>"
    )
    chat_html.append(html_block)
    chat_area.set_html("".join(chat_html))
    chat_area.yview_moveto(1.0)

# Response generator
def generate_response():
    raw_input = user_input.get("1.0", tk.END).strip()
    if not raw_input:
        return

    user_input.delete("1.0", tk.END)
    append_chat("user", "You", raw_input)

    def fetch_response():
        global typing
        typing = True
        Thread(target=animate_typing, daemon=True).start()

        try:
            model_name = selected_model.get()
            if model_name not in AVAILABLE_MODELS:
                raise Exception(f"Model '{model_name}' is not available.")

            if web_toggle.get():
                web_data = fetch_web_results(raw_input)
                prompt = f"Based on the following search results:\n{web_data}\n\nAnswer this:\n{raw_input}"
                chat_log.append(f"You [{datetime.now().strftime('%H:%M')}]: {raw_input}")
                chat_log.append(f"[Injected: Live Web Mode ON]\n{prompt}")
            else:
                prompt = raw_input
                chat_log.append(f"You [{datetime.now().strftime('%H:%M')}]: {raw_input}")

            response = ollama.Client(host="http://host.containers.internal:11434").chat(model=model_name, messages=[{"role": "user", "content": prompt}])
            reply = response["message"]["content"].replace("\n", "<br>")
        except Exception as e:
            reply = f"<span style='color:red;'>[ERROR] {e}</span>"

        typing = False
        typing_label.config(text="")
        append_chat("bot", model_name.capitalize(), reply)
        chat_log.append(f"{model_name.capitalize()} [{datetime.now().strftime('%H:%M')}]:\n{response['message']['content']}\n")

    Thread(target=fetch_response, daemon=True).start()

# Buttons
button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(fill=tk.X, padx=10, pady=10)

send_btn = tk.Button(button_frame, text="Send", command=generate_response, bg="#43d1af", fg="black", font=("Segoe UI", 11, "bold"))
send_btn.pack(side=tk.RIGHT, padx=(0, 5))

save_btn = tk.Button(button_frame, text="Save & Export Chat", command=save_chat, bg="#91b9f4", fg="black", font=("Segoe UI", 10))
save_btn.pack(side=tk.RIGHT, padx=(0, 5))

clear_btn = tk.Button(button_frame, text="Clear Chat", command=clear_chat, bg="#ff6666", fg="black", font=("Segoe UI", 10))
clear_btn.pack(side=tk.LEFT)

# Enter key binding
def enter_key(event):
    generate_response()
    return "break"
user_input.bind("<Return>", enter_key)

# Start app
root.mainloop()
