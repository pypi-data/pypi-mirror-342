import json
import os
from pathlib import Path
from typing import Dict, List, Union, Optional
from .items import CustomItem
from .blocks import CustomBlock
from .recipes import Recipe
from .utils import validate_namespace, write_json

class Datapack:
    def __init__(
        self,
        name: str,
        description: str = "CraftScript生成的数据包",
        version: int = 15,
        namespace: str = None
    ):
        self.name = validate_namespace(name)
        self.description = description
        self.version = version
        self.namespace = validate_namespace(namespace) if namespace else self.name
        self.custom_items: Dict[str, CustomItem] = {}
        self.custom_blocks: Dict[str, CustomBlock] = {}
        self.recipes: List[Recipe] = []
        self.functions: Dict[str, List[str]] = {}
        self.advancements: Dict[str, Dict] = {}

    def add_item(self, item: CustomItem):
        self.custom_items[item.item_id] = item

    def add_block(self, block: CustomBlock):
        self.custom_blocks[block.block_id] = block

    def add_recipe(self, recipe: Recipe):
        self.recipes.append(recipe)

    def add_function(self, name: str, commands: List[str]):
        self.functions[name] = commands

    def add_advancement(self, name: str, advancement: Dict):
        self.advancements[name] = advancement

    def generate(self, output_dir: Union[str, Path] = "generated_datapacks"):
        """生成完整的原版数据包"""
        output_path = Path(output_dir) / self.name
        
        # 生成核心文件
        self._generate_pack_meta(output_path)
        self._generate_items(output_path)
        self._generate_blocks(output_path)
        self._generate_recipes(output_path)
        self._generate_functions(output_path)
        self._generate_advancements(output_path)
        
        # 生成必要的标签目录
        self._generate_tags(output_path)
        
        print(f"✅ 数据包 [{self.name}] 已生成到: {output_path.resolve()}")

    def generate_kubejs(self, output_dir: str = "kubejs"):
        """生成KubeJS 6脚本"""
        from .kubejs.generator import generate_kubejs
        generate_kubejs(self, output_dir)
        print(f"✅ KubeJS脚本已生成到: {Path(output_dir).resolve()}")

    def _generate_pack_meta(self, path: Path):
        """生成pack.mcmeta文件"""
        write_json(path / "pack.mcmeta", {
            "pack": {
                "pack_format": self.version,
                "description": self.description
            }
        })

    def _generate_items(self, path: Path):
        """生成物品JSON文件"""
        items_dir = path / "data" / self.namespace / "items"
        items_dir.mkdir(parents=True, exist_ok=True)
        for item_id, item in self.custom_items.items():
            write_json(items_dir / f"{item_id}.json", item.to_dict())

    def _generate_blocks(self, path: Path):
        """生成方块相关文件"""
        # 方块状态
        blockstates_dir = path / "data" / self.namespace / "blockstates"
        blockstates_dir.mkdir(parents=True, exist_ok=True)
        
        # 方块模型
        models_dir = path / "data" / self.namespace / "models" / "block"
        models_dir.mkdir(parents=True, exist_ok=True)
        
        # 战利品表
        loot_tables_dir = path / "data" / self.namespace / "loot_tables" / "blocks"
        loot_tables_dir.mkdir(parents=True, exist_ok=True)
        
        for block_id, block in self.custom_blocks.items():
            # 方块状态
            write_json(blockstates_dir / f"{block_id}.json", block.get_blockstate())
            
            # 方块模型
            write_json(models_dir / f"{block_id}.json", block.get_model())
            
            # 战利品表
            write_json(loot_tables_dir / f"{block_id}.json", block.get_loot_table())

    def _generate_recipes(self, path: Path):
        """生成配方文件"""
        recipes_dir = path / "data" / self.namespace / "recipes"
        recipes_dir.mkdir(parents=True, exist_ok=True)
        
        for idx, recipe in enumerate(self.recipes):
            write_json(recipes_dir / f"recipe_{idx}.json", recipe.to_dict())

    def _generate_functions(self, path: Path):
        """生成函数文件"""
        functions_dir = path / "data" / self.namespace / "functions"
        functions_dir.mkdir(parents=True, exist_ok=True)
        
        for func_name, commands in self.functions.items():
            with open(functions_dir / f"{func_name}.mcfunction", "w") as f:
                f.write("\n".join(commands))

    def _generate_advancements(self, path: Path):
        """生成进度文件"""
        advancements_dir = path / "data" / self.namespace / "advancements"
        advancements_dir.mkdir(parents=True, exist_ok=True)
        
        for adv_name, advancement in self.advancements.items():
            write_json(advancements_dir / f"{adv_name}.json", advancement)

    def _generate_tags(self, path: Path):
        """生成必要的标签目录"""
        tags_dir = path / "data" / "minecraft" / "tags" / "functions"
        tags_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成load.json标签
        write_json(tags_dir / "load.json", {
            "values": [f"{self.namespace}:load"]
        })
        
        # 生成tick.json标签
        write_json(tags_dir / "tick.json", {
            "values": [f"{self.namespace}:tick"]
        })