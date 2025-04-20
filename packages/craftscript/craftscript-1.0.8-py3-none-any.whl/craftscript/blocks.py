# coding: utf-8

from typing import Dict, Any
from .utils import validate_namespace, load_template

class CustomBlock:
    def __init__(
        self,
        block_id: str,
        texture: str,
        display_name: str = None,
        material: str = "stone",
        hardness: float = 1.0,
        resistance: float = 1.0
    ):
        self.block_id = validate_namespace(block_id)
        self.texture = texture
        self.display_name = display_name
        self.material = material
        self.hardness = hardness
        self.resistance = resistance

    def get_blockstate(self) -> Dict[str, Any]:
        """获取方块状态定义"""
        return load_template("block_state").copy()

    def get_model(self) -> Dict[str, Any]:
        """获取方块模型定义"""
        template = load_template("block_model")
        template["textures"]["all"] = f"block/{self.texture}"
        return template

    def get_loot_table(self) -> Dict[str, Any]:
        """获取战利品表定义"""
        return {
            "type": "minecraft:block",
            "pools": [{
                "rolls": 1,
                "entries": [{
                    "type": "minecraft:item",
                    "name": f"{self.block_id}"
                }],
                "conditions": [{
                    "condition": "minecraft:survives_explosion"
                }]
            }]
        }