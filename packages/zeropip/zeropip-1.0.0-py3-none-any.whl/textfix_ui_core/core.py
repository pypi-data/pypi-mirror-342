
import difflib
import ipywidgets as widgets
from IPython.display import display, clear_output, Javascript, HTML
import uuid

try:
    from langdetect import detect
except ImportError:
    import os
    os.system("pip install langdetect")
    from langdetect import detect

def diff_highlight(original, corrected):
    diff = list(difflib.ndiff(original.split(), corrected.split()))
    result = []
    for word in diff:
        if word.startswith('- '):
            result.append(f"<del style='color:red'>{word[2:]}</del>")
        elif word.startswith('+ '):
            result.append(f"<ins style='color:green'>{word[2:]}</ins>")
        elif word.startswith('  '):
            result.append(word[2:])
    return ' '.join(result)

def run_ui(fn, title="Text UI", input_placeholder="입력하세요", button_label="실행", 
           output_description="결과:", show_description=True, copy_button_label="복사",
           highlight_diff=False, presets=None, template=None, enable_save=True,
           use_tabs=False, theme='light', accent='blue', show_history=True,
           multilingual=False):
    """
    텍스트 UI 구성기 v1.4
    - multilingual: 입력/출력 언어 선택 및 감지 기능 활성화
    """
    accent_style = f"{accent}" if accent in ['primary', 'success', 'info', 'danger', 'warning'] else 'primary'
    dark_mode_css = """
        <style>
        .widget-label { color: white !important; }
        .widget-textarea { background-color: #222 !important; color: #fff !important; }
        </style>
    """ if theme == 'dark' else ""

    input_box = widgets.Textarea(
        value="",
        placeholder=input_placeholder,
        description='입력:',
        layout=widgets.Layout(width='100%', height='100px')
    )

    input_lang = widgets.Dropdown(options=["감지", "ko", "en", "ja", "zh"], value="감지", description="입력언어:")
    output_lang = widgets.Dropdown(options=["ko", "en", "ja", "zh"], value="ko", description="출력언어:")

    output_label = widgets.Label(value=output_description)
    main_output_box = widgets.Textarea(
        value='',
        layout=widgets.Layout(width='100%', height='100px'),
        disabled=False
    )

    submit_button = widgets.Button(description=button_label, button_style=accent_style)
    copy_button = widgets.Button(description=copy_button_label, button_style='success')
    save_button = widgets.Button(description="저장", button_style='info') if enable_save else None

    preset_buttons = []
    if presets:
        for example in presets:
            btn = widgets.Button(description=example[:20], layout=widgets.Layout(width='auto'))
            btn.on_click(lambda b, ex=example: setattr(input_box, 'value', ex))
            preset_buttons.append(btn)

    history_items = []

    def render(body):
        clear_output(wait=True)
        if theme == 'dark':
            display(HTML(dark_mode_css))
        components = []
        if preset_buttons:
            components.append(widgets.HBox(preset_buttons))
        components.extend([input_box])
        if multilingual:
            components.append(widgets.HBox([input_lang, output_lang]))
        components.append(submit_button)
        if show_description:
            components.append(output_label)
        components.extend(body)
        if show_history and history_items:
            label = widgets.HTML("<b>최근 결과:</b>")
            components.append(label)
            components.extend(history_items[::-1])
        display(widgets.VBox(components))

    def on_submit_click(b):
        try:
            input_text = input_box.value

            # 언어 감지
            source_lang = input_lang.value
            if source_lang == "감지":
                source_lang = detect(input_text)

            target_lang = output_lang.value if multilingual else "ko"

            # 템플릿 적용
            if template:
                formatted_input = template.format(text=input_text)
            else:
                formatted_input = input_text

            result = fn(formatted_input, lang_from=source_lang, lang_to=target_lang)                 if multilingual else fn(formatted_input)

            result_text = ""
            if isinstance(result, dict):
                result_text = result.get("결과") or result.get("text") or ""
                main_output_box.value = result_text
                body = [main_output_box, copy_button]
                if enable_save:
                    body.append(save_button)
                for key, val in result.items():
                    if key.lower() in ["결과", "text"]:
                        continue
                    area = widgets.Textarea(
                        value=str(val),
                        description=str(key),
                        layout=widgets.Layout(width='100%', height='100px'),
                        disabled=False
                    )
                    body.append(area)
            else:
                result_text = result
                main_output_box.value = result_text
                body = [main_output_box, copy_button]
                if enable_save:
                    body.append(save_button)

            # history
            if show_history and result_text.strip():
                hist_area = widgets.Textarea(
                    value=result_text,
                    layout=widgets.Layout(width='100%', height='80px'),
                    disabled=True
                )
                hist_copy = widgets.Button(description="복사", button_style='warning', layout=widgets.Layout(width='80px'))
                def copy_hist(_):
                    js_code = f"navigator.clipboard.writeText({repr(result_text)})"
                    display(Javascript(js_code))
                hist_copy.on_click(copy_hist)
                hist_row = widgets.HBox([hist_area, hist_copy])
                history_items.append(hist_row)
                if len(history_items) > 5:
                    history_items.pop(0)

            render(body)

            if highlight_diff:
                html_result = diff_highlight(input_text, result_text)
                display(HTML(f"<b>변경된 부분 하이라이트:</b><br><div>{html_result}</div>"))

        except Exception as e:
            main_output_box.value = f"[오류] {str(e)}"
            render([main_output_box, copy_button])

    def on_copy_click(b):
        js_code = f"navigator.clipboard.writeText({repr(main_output_box.value)})"
        display(Javascript(js_code))

    def on_save_click(b):
        file_id = f"output_{uuid.uuid4().hex[:8]}.txt"
        with open(file_id, "w", encoding="utf-8") as f:
            f.write(main_output_box.value)
        display(HTML(f"<b>저장 완료:</b> <a href='{file_id}' download>{file_id}</a>"))

    submit_button.on_click(on_submit_click)
    copy_button.on_click(on_copy_click)
    if enable_save:
        save_button.on_click(on_save_click)

    render([main_output_box, copy_button] + ([save_button] if enable_save else []))
