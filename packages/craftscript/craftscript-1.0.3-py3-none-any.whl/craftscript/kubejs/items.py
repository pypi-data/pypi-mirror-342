from typing import Dict
from ..items import CustomItem

def generate_item_script(item: CustomItem) -> str:
    """生成单个物品的KubeJS注册代码"""
    script_lines = [
        f'    event.create("{item.item_id}")',
        f'        .displayName("{item.display_name}")',
        f'        .texture("item/{item.texture}")'
    ]
    
    if item.max_stack != 64:
        script_lines.append(f'        .maxStackSize({item.max_stack})')
    
    if item.lore:
        lore_str = ", ".join([f'"{line}"' for line in item.lore])
        script_lines.append(f'        .lore([{lore_str}])')
    
    if item.custom_model_data:
        script_lines.append(f'        .customModelData({item.custom_model_data})')
    
    return "\n".join(script_lines) + ";"