from ..blocks import CustomBlock

def generate_block_script(block: CustomBlock) -> str:
    """生成方块注册脚本"""
    script = [
        f'    event.create("{block.block_id}")',
        f'        .material("{block.material}")',
        f'        .hardness({block.hardness})',
        f'        .resistance({block.resistance})'
    ]
    
    if block.display_name:
        script.insert(1, f'        .displayName("{block.display_name}")')
    
    return "\n".join(script) + ";"