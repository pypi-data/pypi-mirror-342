# 开发人员： Xiaoqiang
# 微信公众号:  XiaoqiangClub
# 开发时间： 2025-04-19
# 文件名称： wechat_draft/__init__.py
# 项目描述： __init__
# 开发工具： PyCharm
from .utils.constants import (VERSION, AUTHOR, DESCRIPTION, EMAIL, CURRENT_SYSTEM, LOG_PATH, LOG_FILE, log)
from .wechat_draft import WechatDraft

__title__ = "wechat_draft"
__version__ = VERSION
__author__ = AUTHOR
__description__ = DESCRIPTION

__all__ = [
    "__title__", "__version__", "__author__", "__description__",
    "VERSION", "AUTHOR", "DESCRIPTION", "EMAIL",
    "CURRENT_SYSTEM", "LOG_PATH", "LOG_FILE", "log",
    "WechatDraft"
]
