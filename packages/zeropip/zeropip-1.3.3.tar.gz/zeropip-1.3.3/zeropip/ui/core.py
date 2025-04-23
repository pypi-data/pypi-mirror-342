from .base import ZeropipUI

def create_ui(on_submit, **kwargs):
    ui = ZeropipUI(on_submit, **kwargs)
    return ui
