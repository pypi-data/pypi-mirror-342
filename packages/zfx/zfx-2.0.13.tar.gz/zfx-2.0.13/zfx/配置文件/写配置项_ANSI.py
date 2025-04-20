import configparser


def 写配置项_ANSI(config文件路径, 节名称, 配置项名称, 值):
    """
    将指定的配置项值写入到以 ANSI 编码保存的配置文件中。

    参数:
        - config文件路径 (str): 配置文件的路径。
        - 节名称 (str): 要写入的节的名称。
        - 配置项名称 (str): 要写入的配置项的名称。
        - 值: 要写入的配置项的值。

    返回:
        bool: 写入成功返回 True，写入失败返回 False。

    使用示例:
        写入配置('config.ini', 'database', 'host', 'localhost')
    """
    try:
        # 创建 ConfigParser 对象
        config = configparser.ConfigParser()

        # 读取现有配置文件内容
        config.read(config文件路径, encoding='mbcs')

        # 如果节不存在，则创建
        if 节名称 not in config:
            config.add_section(节名称)

        # 写入配置项值
        config.set(节名称, 配置项名称, str(值))

        # 写入到文件，指定编码为 ANSI（使用 'mbcs'）
        with open(config文件路径, 'w', encoding='mbcs') as configfile:
            config.write(configfile)

        return True
    except Exception as e:
        print(f"写入配置文件时出错: {e}")
        return False


# 测试函数
配置文件_写配置项_ANSI(r"C:\Users\Administrator\Desktop\config.ini", 'database', 'host', 'localhost')
