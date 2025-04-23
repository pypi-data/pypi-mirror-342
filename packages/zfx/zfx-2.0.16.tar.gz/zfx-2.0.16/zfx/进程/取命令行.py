import psutil


def 取命令行(pid):
    """
    根据指定进程 ID 获取其启动时的命令行参数列表。

    参数:
        - pid (int): 要查询的进程 ID，例如 1234。

    返回值:
        - list:
            - 成功时返回该进程的命令行参数列表（含可执行路径和所有参数）。
            - 若进程不存在或访问失败，则返回空列表。

    注意事项:
        1. 需要目标进程在运行中，且当前用户有权限访问。
        2. 返回值示例：["C:\\Program Files\\Example\\app.exe", "--debug", "--port=8080"]

    使用示例:
        命令行参数 = 取命令行(1234)
        if 命令行参数:
            print("目标进程命令行:", 命令行参数)
        else:
            print("无法获取该进程的命令行参数")
    """
    try:
        process = psutil.Process(pid)
        return process.cmdline()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return []