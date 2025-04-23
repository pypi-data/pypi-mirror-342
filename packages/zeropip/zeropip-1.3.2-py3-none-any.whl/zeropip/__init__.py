
import ipywidgets as widgets
from IPython.display import display, Javascript
import uuid

def create_ui(on_submit, description="", enable_copy=True, enable_file=True,
              enable_cache_reset=True, enable_options=True, enable_download=True):

    input_box = widgets.Textarea(placeholder='텍스트를 입력하세요...', layout=widgets.Layout(width='100%', height='100px'))
    output_box = widgets.Textarea(layout=widgets.Layout(width='100%', height='150px'), disabled=False)
    info_box = widgets.HTML(value='<span style="color:gray;">실행 결과가 여기에 표시됩니다.</span>')
    upload_button = widgets.FileUpload(accept='.txt,.csv,.json', multiple=False)
    option_box = widgets.Checkbox(value=False, description='옵션 활성화')
    submit_button = widgets.Button(description="실행", button_style='success')
    copy_button = widgets.Button(description="복사", button_style='info')
    clear_cache_button = widgets.Button(description="캐시 삭제", button_style='warning')
    download_button = widgets.Button(description="다운로드", button_style='primary')
    file_cache = [None]

    def _on_submit_click(_):
        try:
            option_state = option_box.value if enable_options else False
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

    def _on_upload(change):
        for filename, fileinfo in upload_button.value.items():
            content = fileinfo['content'].decode('utf-8')
            input_box.value = content
            file_cache[0] = (filename, content)
            info_box.value = f"<span style='color:gray;'>📂 {filename} 업로드됨</span>"

    def _on_clear_cache(_):
        input_box.value = ""
        output_box.value = ""
        file_cache[0] = None
        info_box.value = "<span style='color:orange;'>캐시/입력 내용이 초기화되었습니다</span>"

    def _on_download_click(_):
        filename = f"zeropip_output_{uuid.uuid4().hex[:8]}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(output_box.value)
        download_js = f"""
        var link = document.createElement('a');
        link.href = 'files/{filename}';
        link.download = '{filename}';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        """
        display(Javascript(download_js))
        info_box.value = f"<span style='color:purple;'>📥 결과가 파일로 다운로드되었습니다</span>"

    submit_button.on_click(_on_submit_click)
    copy_button.on_click(_on_copy_click)
    clear_cache_button.on_click(_on_clear_cache)
    download_button.on_click(_on_download_click)
    upload_button.observe(_on_upload, names='value')

    box_list = [input_box]
    if enable_file:
        box_list.append(upload_button)
    if enable_options:
        box_list.append(option_box)
    box_list.extend([submit_button, output_box, info_box])
    if enable_copy:
        box_list.append(copy_button)
    if enable_cache_reset:
        box_list.append(clear_cache_button)
    if enable_download:
        box_list.append(download_button)

    if description:
        display(widgets.HTML(f"<b>{description}</b>"))
    display(widgets.VBox(box_list))
