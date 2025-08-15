from adapters.chatgpt.client import call_chatgpt
import gradio as gr

def chat(input_text):
    return call_chatgpt(input_text)

demo = gr.Interface(fn=chat, inputs="text", outputs="text", title="AI Scroll Certification")

if __name__ == "__main__":
    demo.launch()

