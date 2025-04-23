
# Zeropip

**Zero-loading, zero-server, zero-fuss. A lightning-fast text-based UI framework for Colab and Jupyter.**

## Features

- Run interactive NLP tools with just one function: `run_ui`
- No loading bar. No servers. No bloated dependencies.
- Smart UI with text input, submit, copy, save, and tabbed outputs
- Optional: history log, diff highlighting, language detection
- Supports `TextTool` structure for clean modular tools

## Example

```python
from zeropip import run_ui

def echo(text):
    return {"결과": text.upper()}

run_ui(echo)
```

## License

MIT
