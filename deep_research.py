"""
deep_research
Launches a gradio UI using their new Blocks API
"""
import os
import threading
import time

import gradio as gr
from dotenv import load_dotenv

from research_manager import ResearchManager


load_dotenv(override=True)

async def run(query: str):
    """
    It creates a simple asynchronous streaming interface that 
    forwards chunks of research results from ResearchManager.run(query) 
    to the caller.
    """
    async for chunk in ResearchManager().run(query):
        yield chunk


demo = gr.Blocks()

with demo:
    gr.Markdown("# Deep Research")
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    run_button = gr.Button("Run", variant="primary")
    report = gr.Markdown(label="Report")
    exit_button = gr.Button("Exit", variant="stop")
    
    run_button.click(fn=run, inputs=query_textbox, outputs=report)
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)

    def exit_app():
        """
        Stoopid gradio doesn't have an exit function, so we have to write one :(
        """
        def _close():
            """
            Small delay first!
            """
            time.sleep(0.4)
            demo.close()

        threading.Thread(target=_close, daemon=True).start()
        return (
            "✅ Shutting down… you can close this tab.",
            gr.update(interactive=False),
            gr.update(interactive=False),
        )

    exit_button.click(
        fn=exit_app, 
        inputs=None, 
        outputs=[report, run_button, query_textbox],
    )

demo.launch(inbrowser=True)
