import ipywidgets as widgets
from IPython.display import display, Javascript
import uuid

def create_ui(on_submit, description="", enable_copy=True, enable_file=False,
              enable_cache_reset=False, enable_options=False, enable_download=False):

    input_box = widgets.Textarea(placeholder='텍스트를 입력하세요...', layout=widgets.Layout(width='100%', height='300px'))
    output_box = widgets.Textarea(layout=widgets.Layout(width='100%', height='300px'), disabled=False)
    info_box = widgets.HTML(value='<span style="color:gray;">실행 결과가 여기에 표시됩니다.</span>')
    submit_button = widgets.Button(description="실행", button_style='success')
    copy_button = widgets.Button(description="복사", button_style='info')

    def _on_submit_click(_):
        try:
            option_state = False
            result = on_submit(input_box.value, option_state)
            output_box.value = result.get("결과", "")
            info_box.value = f"<span style='color:green;'>{result.get('정보', '처리 완료')}</span>"
        except Exception as e:
            output_box.value = ""
            info_box.value = f"<span style='color:red;'>[오류] {e}</span>"

    def _on_copy_click(_):
        js_code = f"""
        navigator.clipboard.writeText(`{output_box.value}`).catch(err => {{
            console.log("복사 실패", err);
        }});
        """
        display(Javascript(js_code))
        info_box.value = "<span style='color:blue;'>복사되었습니다 ✅</span>"

    submit_button.on_click(_on_submit_click)
    copy_button.on_click(_on_copy_click)

    box_list = [input_box, submit_button, output_box, info_box]
    if enable_copy:
        box_list.append(copy_button)

    if description:
        display(widgets.HTML(f"<b>{description}</b>"))
    display(widgets.VBox(box_list))