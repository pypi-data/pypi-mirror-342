from typing import Dict, List, Optional, Any
from .utils import validate_namespace

class Recipe:
    def __init__(
        self,
        recipe_type: str,
        result: Dict[str, Any],
        namespace: str,
        group: Optional[str] = None
    ):
        self.recipe_type = validate_namespace(recipe_type)
        self.result = result
        self.namespace = validate_namespace(namespace)
        self.group = group
        self.conditions: List[Dict] = []

    def add_condition(self, condition: Dict):
        self.conditions.append(condition)
        return self

    def to_dict(self) -> Dict[str, Any]:
        base = {
            "type": self.recipe_type,
            "result": self.result
        }
        if self.group:
            base["group"] = self.group
        if self.conditions:
            base["conditions"] = self.conditions
        return base

class ShapedRecipe(Recipe):
    def __init__(
        self,
        result: Dict[str, Any],
        pattern: List[str],
        key: Dict[str, Dict[str, str]],
        namespace: str,
        group: Optional[str] = None
    ):
        super().__init__("crafting_shaped", result, namespace, group)
        self.pattern = pattern
        self.key = key

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "pattern": self.pattern,
            "key": self.key
        })
        return data