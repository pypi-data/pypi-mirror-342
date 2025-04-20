# coding: utf-8

def generate_item_js(item) -> str:
    """生成单个物品的KubeJS注册代码"""
    code = [
        f'    event.create("{item.item_id}")',
        f'        .displayName("{item.display_name}")',
        f'        .texture("item/{item.texture}")'
    ]
    
    if item.max_stack != 64:
        code.append(f'        .maxStackSize({item.max_stack})')
    
    if item.lore:
        lore = ", ".join([f'"{line}"' for line in item.lore])
        code.append(f'        .lore([{lore}])')
    
    return "\n".join(code) + ";"

__all__ = ["generate_item_js"]