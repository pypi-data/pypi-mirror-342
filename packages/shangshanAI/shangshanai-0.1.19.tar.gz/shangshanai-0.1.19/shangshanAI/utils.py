import os
import re
from pathlib import Path

def get_cache_dir() -> str:
    """获取默认缓存目录"""
    cache_dir = os.getenv("SHANGSHANAI_HOME", None)
    if cache_dir is None:
        cache_dir = os.path.join(str(Path.home()), ".shangshanAI")
    return cache_dir

def validate_model_id(model_id: str) -> bool:
    """验证模型ID格式"""
    pattern = r"^[a-zA-Z0-9-]+/[a-zA-Z0-9-_]+$"
    return bool(re.match(pattern, model_id)) 