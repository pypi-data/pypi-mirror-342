
import ipywidgets as widgets
from IPython.display import display

def run_ui(tool_func, highlight_diff=False):
    input_box = widgets.Textarea(placeholder='텍스트를 입력하세요...', layout=widgets.Layout(width='100%', height='100px'))
    output_box = widgets.Textarea(layout=widgets.Layout(width='100%', height='150px'))
    button = widgets.Button(description="실행")

    def on_click(b):
        result = tool_func(input_box.value)
        output_box.value = "\n".join(f"{k}: {v}" for k, v in result.items())

    button.on_click(on_click)
    display(input_box, button, output_box)
