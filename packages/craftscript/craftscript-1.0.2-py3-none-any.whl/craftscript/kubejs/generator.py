import json
from pathlib import Path
from typing import Dict, List
from ..datapack import Datapack
from .items import generate_item_script
from .blocks import generate_block_script
from .recipes import (
    generate_shaped_recipe,
    generate_shapeless_recipe,
    generate_smelting_recipe
)

def generate_kubejs(datapack: Datapack, output_dir: str = "kubejs"):
    """生成全套KubeJS脚本"""
    output_path = Path(output_dir)
    _generate_startup_scripts(datapack, output_path)
    _generate_server_scripts(datapack, output_path)

def _generate_startup_scripts(datapack: Datapack, base_path: Path):
    """生成启动阶段脚本"""
    startup_dir = base_path / "startup_scripts"
    startup_dir.mkdir(exist_ok=True)
    
    # 生成物品注册脚本
    items_js = [
        "// Auto-generated item registrations",
        "StartupEvents.registry('item', event => {"
    ]
    for item in datapack.custom_items.values():
        items_js.append(generate_item_script(item))
    items_js.append("});\n")
    
    # 生成方块注册脚本
    blocks_js = [
        "// Auto-generated block registrations",
        "StartupEvents.registry('block', event => {"
    ]
    for block in datapack.custom_blocks.values():
        blocks_js.append(generate_block_script(block))
    blocks_js.append("});")
    
    (startup_dir / "registration.js").write_text("\n".join(items_js + blocks_js))

def _generate_server_scripts(datapack: Datapack, base_path: Path):
    """生成服务端脚本"""
    server_dir = base_path / "server_scripts"
    server_dir.mkdir(exist_ok=True)
    
    recipes_js = [
        "// Auto-generated recipes",
        "ServerEvents.recipes(event => {"
    ]
    
    for recipe in datapack.recipes:
        if recipe.recipe_type == "minecraft:crafting_shaped":
            recipes_js.append(generate_shaped_recipe(recipe))
        elif recipe.recipe_type == "minecraft:crafting_shapeless":
            recipes_js.append(generate_shapeless_recipe(recipe))
        elif recipe.recipe_type == "minecraft:smelting":
            recipes_js.append(generate_smelting_recipe(recipe))
    
    recipes_js.append("});")
    (server_dir / "recipes.js").write_text("\n".join(recipes_js))