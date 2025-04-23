
# Zeropip

🧩 Lightweight UI framework for Colab / Jupyter notebooks.  
Just plug in a function and go.

## Installation

```
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
