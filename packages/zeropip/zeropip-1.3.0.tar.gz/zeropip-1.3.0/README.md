# Zeropip

🧩 Lightweight UI framework for Colab / Jupyter notebooks.  
Just plug in a function and go.

## Installation

```bash
pip install zeropip
```

## Example

```python
from zeropip.ui.core import ZeropipUI

def my_tool(text, option):
    return {
        "결과": text[::-1],
        "정보": "문자열 반전 완료"
    }

ZeropipUI(on_submit=my_tool, description="🔁 텍스트 반전기")
```

## Features

- 입력 텍스트 박스
- 업로드/다운로드 지원
- 복사 기능
- 실행 버튼과 옵션 체크박스
- 캐시 초기화 버튼
