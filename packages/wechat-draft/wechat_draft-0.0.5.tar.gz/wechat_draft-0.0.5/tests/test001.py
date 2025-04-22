import logging


def setup_logger(log_level: str = 'INFO'):
    """
    设置日志记录器
    :param log_level: 日志记录器日志级别
    :return: 
    """
    # 创建日志记录器
    log = logging.getLogger('wechat_draft')
    log.setLevel(log_level.upper())  # 设置日志级别

    # 创建控制台输出流
    console_handler = logging.StreamHandler()

    # 设置日志输出格式
    formatter = logging.Formatter('%(asctime)s - [%(name)s %(filename)s:%(lineno)d] - %(levelname)s: %(message)s')
    console_handler.setFormatter(formatter)

    # 将处理器添加到记录器中
    log.addHandler(console_handler)
    return log


log = setup_logger('debug')

log.debug('This is a debug message.')
log.info('This is a debug message.')
log.warning('This is a debug message.')