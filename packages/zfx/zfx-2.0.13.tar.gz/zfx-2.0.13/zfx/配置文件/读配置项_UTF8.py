import configparser


def 读配置项_UTF8(config文件路径, 节名称, 配置项名称, 默认值=None):
    """
    从配置文件中读取指定的配置项值。

    参数:
        - config文件路径 (str): 配置文件的路径。
        - 节名称 (str): 要读取的节的名称。
        - 配置项名称 (str): 要读取的配置项的名称。
        - 默认值: 如果配置项不存在时返回的默认值。默认为 None。

    返回:
        str: 读取到的配置项值，若配置项不存在则返回默认值。

    使用示例:
        读取配置('config.ini', 'database', 'host')
    """
    try:
        # 创建 ConfigParser 对象
        config = configparser.ConfigParser()

        # 读取配置文件，指定编码为 UTF-8
        config.read(config文件路径, encoding='utf-8')

        # 获取指定节和配置项的值
        if config.has_section(节名称):
            if config.has_option(节名称, 配置项名称):
                return config.get(节名称, 配置项名称)

        # 如果节或配置项不存在，返回默认值
        return 默认值

    except Exception:
        return 默认值