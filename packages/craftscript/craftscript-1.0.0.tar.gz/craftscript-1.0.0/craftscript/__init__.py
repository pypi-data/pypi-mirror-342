"""
CraftScript - Minecraft 数据包与 KubeJS 脚本生成工具
"""

from .datapack import Datapack
from .items import CustomItem
from .blocks import CustomBlock
from .recipes import (
    ShapedRecipe, ShapelessRecipe,
    SmeltingRecipe, BlastingRecipe,
    SmokingRecipe, CampfireRecipe,
    StonecuttingRecipe, SmithingRecipe
)

__version__ = "1.0.0"
__all__ = [
    'Datapack', 'CustomItem', 'CustomBlock',
    'ShapedRecipe', 'ShapelessRecipe',
    'SmeltingRecipe', 'BlastingRecipe',
    'SmokingRecipe', 'CampfireRecipe',
    'StonecuttingRecipe', 'SmithingRecipe'
]