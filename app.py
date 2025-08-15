import gradio as gr

def greet(name):
    return f"Welcome, {name}! This is the AI Scroll Certification Chatroom."

demo = gr.Interface(fn=greet, inputs="text", outputs="text", title="AI Scroll Certification")

if __name__ == "__main__":
    demo.launch()

from adapters.chatgpt.client import call_chatgpt
import gradio as gr

def chat(input_text):
    return call_chatgpt(input_text)

gr.Interface(fn=chat, inputs="text", outputs="text").launch()
