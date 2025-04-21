# __version__ = "0.1.1"

# 暴露公共接口
from .ar4m import AR4M, AR4, AR4Packet

__all__ = ['AR4M', 'AR4', 'AR4Packet']

# from importlib import import_module
# from pathlib import Path

# _MODULES = [p.stem for p in Path(__file__).parent.glob("*.py") if p.stem != "__init__"]

# for module in _MODULES:
#     import_module(f".{module}", package="qlsdk")