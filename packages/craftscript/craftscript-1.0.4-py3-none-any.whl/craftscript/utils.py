import json
from pathlib import Path
from typing import Dict, Any

def validate_namespace(namespace: str) -> str:
    """验证命名空间格式 (小写字母/数字/下划线)"""
    if not namespace.replace("_", "").isalnum():
        raise ValueError(f"非法命名空间: {namespace}")
    return namespace.lower()

def write_json(file_path: Path, data: Dict, indent: int = 2):
    """写入JSON文件"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)

def load_template(template_name: str) -> Dict:
    """加载JSON模板"""
    template_path = Path(__file__).parent / "templates" / f"{template_name}.json"
    with open(template_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_item_model(texture: str) -> Dict:
    """生成标准物品模型"""
    return {
        "parent": "item/generated",
        "textures": {
            "layer0": f"item/{texture}"
        }
    }