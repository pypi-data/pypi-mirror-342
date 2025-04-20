import unittest
import json
from craftscript.recipes import (
    ShapedRecipe,
    ShapelessRecipe,
    SmeltingRecipe,
    BlastingRecipe,
    SmithingRecipe
)

class TestRecipes(unittest.TestCase):
    def test_shaped_recipe(self):
        """测试有序合成配方生成"""
        recipe = ShapedRecipe(
            result={"item": "test:ruby", "count": 1},
            pattern=["AAA", " A ", "AAA"],
            key={"A": {"item": "minecraft:amethyst_shard"}},
            namespace="test",
            group="gem_recipes"
        )
        
        # 验证基础结构
        data = recipe.to_dict()
        self.assertEqual(data["type"], "minecraft:crafting_shaped")
        self.assertEqual(data["pattern"], ["AAA", " A ", "AAA"])
        self.assertEqual(data["key"]["A"]["item"], "minecraft:amethyst_shard")
        self.assertEqual(data["result"]["item"], "test:ruby")
        self.assertEqual(data.get("group"), "gem_recipes")

    def test_shapeless_recipe(self):
        """测试无序合成配方生成"""
        recipe = ShapelessRecipe(
            result={"item": "test:diamond_dust", "count": 4},
            ingredients=[
                {"item": "minecraft:diamond"},
                {"item": "minecraft:gunpowder"}
            ],
            namespace="test"
        )
        
        data = recipe.to_dict()
        self.assertEqual(data["type"], "minecraft:crafting_shapeless")
        self.assertEqual(len(data["ingredients"]), 2)
        self.assertEqual(data["ingredients"][1]["item"], "minecraft:gunpowder")

    def test_smelting_recipe(self):
        """测试熔炉配方生成"""
        recipe = SmeltingRecipe(
            result={"item": "test:smelted_iron"},
            ingredient={"item": "minecraft:raw_iron"},
            namespace="test",
            experience=0.7,
            cooking_time=200
        ).add_condition({"type": "minecraft:item_exists", "item": "minecraft:raw_iron"})
        
        data = recipe.to_dict()
        self.assertEqual(data["type"], "minecraft:smelting")
        self.assertEqual(data["ingredient"]["item"], "minecraft:raw_iron")
        self.assertEqual(data["experience"], 0.7)
        self.assertEqual(data["cookingtime"], 200)
        self.assertEqual(len(data["conditions"]), 1)

    def test_blast_recipe(self):
        """测试高炉配方继承关系"""
        recipe = BlastingRecipe(
            result={"item": "test:blast_glass"},
            ingredient={"item": "minecraft:sand"},
            namespace="test"
        )
        
        data = recipe.to_dict()
        self.assertEqual(data["type"], "minecraft:blasting")
        self.assertEqual(data["cookingtime"], 100)  # 验证默认值覆盖

    def test_invalid_pattern(self):
        """测试非法合成表格式"""
        with self.assertRaises(ValueError):
            ShapedRecipe(
                result={"item": "test:invalid"},
                pattern=["AAAA"],  # 超过3个字符
                key={"A": {"item": "test:material"}},
                namespace="test"
            )
        
        with self.assertRaises(ValueError):
            ShapedRecipe(
                result={"item": "test:invalid"},
                pattern=["A", "B", "C", "D"],  # 超过3行
                key={"A": {"item": "test:material"}},
                namespace="test"
            )

    def test_smithing_recipe(self):
        """测试锻造配方生成"""
        recipe = SmithingRecipe(
            result={"item": "test:netherite_hammer"},
            base={"item": "minecraft:diamond_sword"},
            addition={"item": "minecraft:netherite_ingot"},
            namespace="test"
        )
        
        data = recipe.to_dict()
        self.assertEqual(data["base"]["item"], "minecraft:diamond_sword")
        self.assertEqual(data["addition"]["item"], "minecraft:netherite_ingot")
        self.assertEqual(data["type"], "minecraft:smithing")

    def test_recipe_conditions(self):
        """测试配方条件添加"""
        recipe = ShapedRecipe(
            result={"item": "test:locked_item"},
            pattern=["A"],
            key={"A": {"item": "minecraft:stick"}},
            namespace="test"
        ).add_condition({
            "type": "minecraft:recipe_unlocked",
            "items": ["minecraft:redstone"]
        })
        
        data = recipe.to_dict()
        self.assertEqual(len(data["conditions"]), 1)
        self.assertEqual(data["conditions"][0]["type"], "minecraft:recipe_unlocked")

if __name__ == "__main__":
    unittest.main()