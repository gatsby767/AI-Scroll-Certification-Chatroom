import gradio as gr

def greet(name):
    return f"Welcome, {name}! This is the AI Scroll Certification Chatroom."

demo = gr.Interface(fn=greet, inputs="text", outputs="text", title="AI Scroll Certification")

if __name__ == "__main__":
    demo.launch()
