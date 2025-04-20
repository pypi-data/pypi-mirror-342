from typing import Dict, List, Optional, Any
from .utils import validate_namespace

class Recipe:
    """配方基类"""
    def __init__(self, recipe_type: str, result: Dict, namespace: str):
        self.recipe_type = recipe_type
        self.result = result
        self.namespace = namespace
        self.conditions: List[Dict] = []
        self.group: Optional[str] = None

    def add_condition(self, condition: Dict):
        self.conditions.append(condition)
        return self

    def to_dict(self) -> Dict:
        return {
            "type": self.recipe_type,
            "result": self.result,
            "conditions": self.conditions,
            "group": self.group
        }

class ShapedRecipe(Recipe):
    """有序合成配方"""
    def __init__(
        self,
        result: Dict,
        pattern: List[str],
        key: Dict[str, Dict],
        namespace: str,
        group: Optional[str] = None
    ):
        super().__init__("minecraft:crafting_shaped", result, namespace)
        self.pattern = pattern
        self.key = key
        self.group = group

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            "pattern": self.pattern,
            "key": self.key
        })
        return data

class ShapelessRecipe(Recipe):  # 添加这个类
    """无序合成配方"""
    def __init__(
        self,
        result: Dict,
        ingredients: List[Dict],
        namespace: str,
        group: Optional[str] = None
    ):
        super().__init__("minecraft:crafting_shapeless", result, namespace)
        self.ingredients = ingredients
        self.group = group

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data["ingredients"] = self.ingredients
        return data

class SmeltingRecipe(Recipe):  # 新增熔炉配方类
    """熔炉烧炼配方"""
    def __init__(
        self,
        result: Dict,
        ingredient: Dict,
        namespace: str,
        experience: float = 0.1,
        cooking_time: int = 200
    ):
        super().__init__("minecraft:smelting", result, namespace)
        self.ingredient = ingredient
        self.experience = experience
        self.cooking_time = cooking_time

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data.update({
            "ingredient": self.ingredient,
            "experience": self.experience,
            "cookingtime": self.cooking_time
        })
        return data
    

__all__ = [
    'Recipe',
    'ShapedRecipe',
    'ShapelessRecipe',
    'SmeltingRecipe'
]