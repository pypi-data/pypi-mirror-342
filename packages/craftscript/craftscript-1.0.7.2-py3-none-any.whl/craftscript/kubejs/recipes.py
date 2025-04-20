from typing import Dict, List
from ..recipes import Recipe, ShapedRecipe, SmeltingRecipe

def generate_shaped_recipe(recipe: ShapedRecipe) -> str:
    """生成有序合成配方脚本"""
    pattern = ",\n        ".join([f'"{row}"' for row in recipe.pattern])
    keys = ",\n        ".join([f'{key}: "{value["item"]}"' for key, value in recipe.key.items()])
    
    return f"""
    event.recipes.minecraft.crafting_shaped(
        "{recipe.result["item"]}",
        [
            {pattern}
        ],
        {{
            {keys}
        }}
    )"""

def generate_shapeless_recipe(recipe: Recipe) -> str:
    """生成无序合成配方脚本"""
    ingredients = ", ".join([f'"{i["item"]}"' for i in recipe.ingredients])
    return f"""
    event.recipes.minecraft.crafting_shapeless(
        "{recipe.result["item"]}",
        [{ingredients}]
    )"""

def generate_smelting_recipe(recipe: SmeltingRecipe) -> str:
    """生成熔炉配方脚本"""
    return f"""
    event.recipes.minecraft.smelting(
        "{recipe.result["item"]}",
        "{recipe.ingredient["item"]}"
    )
        .xp({recipe.experience})
        .cookingTime({recipe.cooking_time})"""