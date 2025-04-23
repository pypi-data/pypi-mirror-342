import ipywidgets as widgets
from IPython.display import display, Javascript
import uuid

class ZeropipUI:
    def __init__(self, on_submit, description="", enable_copy=True, enable_file=True, enable_cache_reset=True, enable_options=True, enable_download=True):
        self.on_submit = on_submit
        self.description = description
        self.enable_copy = enable_copy
        self.enable_file = enable_file
        self.enable_cache_reset = enable_cache_reset
        self.enable_options = enable_options
        self.enable_download = enable_download

        self.file_cache = None
        self._render_ui()

    def _render_ui(self):
        if self.description:
            display(widgets.HTML(f"<b>{self.description}</b>"))

        self.input_box = widgets.Textarea(placeholder='텍스트를 입력하세요...', layout=widgets.Layout(width='100%', height='100px'))
        self.output_box = widgets.Textarea(layout=widgets.Layout(width='100%', height='150px'), disabled=False)
        self.info_box = widgets.HTML(value='<span style="color:gray;">실행 결과가 여기에 표시됩니다.</span>')
        self.upload_button = widgets.FileUpload(accept='.txt,.csv,.json', multiple=False)
        self.option_box = widgets.Checkbox(value=False, description='옵션 활성화')
        self.submit_button = widgets.Button(description="실행", button_style='success')
        self.copy_button = widgets.Button(description="복사", button_style='info')
        self.clear_cache_button = widgets.Button(description="캐시 삭제", button_style='warning')
        self.download_button = widgets.Button(description="다운로드", button_style='primary')

        self.submit_button.on_click(self._on_submit_click)
        self.copy_button.on_click(self._on_copy_click)
        self.clear_cache_button.on_click(self._on_clear_cache)
        self.download_button.on_click(self._on_download_click)
        self.upload_button.observe(self._on_upload, names='value')

        box_list = [self.input_box]
        if self.enable_file:
            box_list.append(self.upload_button)
        if self.enable_options:
            box_list.append(self.option_box)

        box_list.append(self.submit_button)
        box_list.append(self.output_box)
        box_list.append(self.info_box)

        if self.enable_copy:
            box_list.append(self.copy_button)
        if self.enable_cache_reset:
            box_list.append(self.clear_cache_button)
        if self.enable_download:
            box_list.append(self.download_button)

        display(widgets.VBox(box_list))

    def _on_submit_click(self, b):
        try:
            option_state = self.option_box.value if self.enable_options else False
            result = self.on_submit(self.input_box.value, option_state)
            self.output_box.value = result.get("결과", "")
            self.info_box.value = f"<span style='color:green;'>{result.get('정보', '처리 완료')}</span>"
        except Exception as e:
            self.output_box.value = ""
            self.info_box.value = f"<span style='color:red;'>[오류] {e}</span>"

    def _on_copy_click(self, b):
        js_code = "navigator.clipboard.writeText(`" + self.output_box.value + "`);"
        display(Javascript(js_code))
        self.info_box.value = "<span style='color:blue;'>복사되었습니다 ✅</span>"

    def _on_upload(self, change):
        for filename, fileinfo in self.upload_button.value.items():
            content = fileinfo['content'].decode('utf-8')
            self.input_box.value = content
            self.file_cache = (filename, content)
            self.info_box.value = f"<span style='color:gray;'>📂 {filename} 업로드됨</span>"

    def _on_clear_cache(self, b):
        self.input_box.value = ""
        self.output_box.value = ""
        self.info_box.value = "<span style='color:orange;'>캐시/입력 내용이 초기화되었습니다</span>"
        self.file_cache = None

    def _on_download_click(self, b):
        filename = f"zeropip_output_{uuid.uuid4().hex[:8]}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.output_box.value)

        download_js = f'''
        var link = document.createElement('a');
        link.href = 'files/{filename}';
        link.download = '{filename}';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        '''
        display(Javascript(download_js))
        self.info_box.value = f"<span style='color:purple;'>📥 결과가 파일로 다운로드되었습니다</span>"
