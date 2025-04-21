# 开发人员： Xiaoqiang
# 微信公众号:  XiaoqiangClub
# 开发时间： 2025-04-19
# 文件名称： wechat_draft/utils/constants.py
# 项目描述： 常量定义文件
# 开发工具： PyCharm
import os
import platform
from .logger import LoggerBase

# 版本号
VERSION = '0.0.1'
# 作者
AUTHOR = 'Xiaoqiang'
# 邮箱
EMAIL = 'xiaoqiangclub@hotmail.com'
# 项目描述
DESCRIPTION = '新建微信公众号文章草稿'

# 当前运行的系统
CURRENT_SYSTEM = platform.system()

# 项目根目录
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 创建data目录
DATA_PATH = os.path.join(ROOT_PATH, 'data')
os.makedirs(DATA_PATH, exist_ok=True)

# 创建临时目录 temp
TEMP_PATH = os.path.join(ROOT_PATH, 'temp')
os.makedirs(TEMP_PATH, exist_ok=True)

# 日志保存路径
LOG_PATH = os.path.join(ROOT_PATH, 'logs')
os.makedirs(LOG_PATH, exist_ok=True)
LOG_FILE = os.path.join(LOG_PATH, 'wechat_draft.log')

logger = LoggerBase('wechat_draft', console_log_level='DEBUG', file_log_level='WARNING', log_file=LOG_FILE)
log = logger.logger
