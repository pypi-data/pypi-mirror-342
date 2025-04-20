import unittest
from craftscript.items import CustomItem

class TestCustomItem(unittest.TestCase):
    def test_item_creation(self):
        item = CustomItem(
            item_id="test_item",
            display_name="测试物品",
            texture="test_texture"
        )
        self.assertEqual(item.item_id, "test_item")
        self.assertEqual(item.texture, "test_texture")