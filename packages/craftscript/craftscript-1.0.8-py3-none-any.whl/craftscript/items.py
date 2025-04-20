# coding: utf-8

from typing import Dict, List, Optional
from pathlib import Path
from .utils import load_template, validate_namespace
import json

class CustomItem:
    def __init__(
        self,
        item_id: str,
        display_name: str,
        texture: str,
        max_stack: int = 64,
        lore: Optional[List[str]] = None,
        custom_model_data: int = None
    ):
        self.item_id = validate_namespace(item_id)
        self.display_name = display_name
        self.texture = texture
        self.max_stack = max_stack
        self.lore = lore or []
        self.custom_model_data = custom_model_data

    def to_dict(self) -> Dict:
        template = load_template("item_model")
        template["textures"]["layer0"] = f"item/{self.texture}"
        if self.display_name or self.lore:
            template["display"] = {}
            if self.display_name:
                template["display"]["Name"] = json.dumps(self.display_name)
            if self.lore:
                template["display"]["Lore"] = [json.dumps(line) for line in self.lore]
        return template

    def to_kubejs(self) -> str:
        from .kubejs.items import generate_item_js
        return generate_item_js(self)