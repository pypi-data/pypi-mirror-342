import json
from pathlib import Path
from typing import Dict, List, Union
from .items import CustomItem
from .blocks import CustomBlock
from .recipes import Recipe
from .utils import validate_namespace, write_json

class Datapack:
    def __init__(self, name: str, description: str = "CraftScript生成的数据包", version: int = 15):
        self.name = validate_namespace(name)
        self.description = description
        self.version = version
        self.namespace = self.name
        self.custom_items: Dict[str, CustomItem] = {}
        self.recipes: List[Recipe] = []

    def add_item(self, item: CustomItem):
        self.custom_items[item.item_id] = item

    def add_recipe(self, recipe: Recipe):
        self.recipes.append(recipe)

    def generate(self, output_dir: Union[str, Path] = "generated_datapacks"):
        output_path = Path(output_dir) / self.name
        self._generate_pack_meta(output_path)
        self._generate_items(output_path)
        self._generate_recipes(output_path)

    def _generate_pack_meta(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)  # 关键修复
        write_json(path / "pack.mcmeta", {
            "pack": {
                "pack_format": self.version,
                "description": self.description
            }
        })

    def _generate_items(self, path: Path):
        items_dir = path / "data" / self.namespace / "items"
        items_dir.mkdir(parents=True, exist_ok=True)  # 关键修复
        for item_id, item in self.custom_items.items():
            write_json(items_dir / f"{item_id}.json", item.to_dict())

    def _generate_recipes(self, path: Path):
        recipes_dir = path / "data" / self.namespace / "recipes"
        recipes_dir.mkdir(parents=True, exist_ok=True)  # 关键修复
        for idx, recipe in enumerate(self.recipes):
            write_json(recipes_dir / f"recipe_{idx}.json", recipe.to_dict())

    def generate_kubejs(self, output_dir: str = "kubejs"):
        """生成 KubeJS 6 脚本"""
        from .kubejs.generator import generate_kubejs  # 确保导入生成器模块
        generate_kubejs(self, output_dir)
        print(f"✅ KubeJS脚本已生成到: {Path(output_dir).resolve()}")