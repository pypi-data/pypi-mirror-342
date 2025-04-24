import subprocess
import os
import sys
import tempfile


def 封装代码_普通编译(脚本路径, 隐藏导入模块=None):
    """
    将指定的 Python 脚本打包成标准结构的 EXE 可执行文件，输出到用户桌面（非单文件模式）。

    参数：
        - 脚本路径 (str): 要打包的 Python 脚本路径，例如 "D:\\项目\\主程序.py"。
        - 隐藏导入模块 (list[str], 可选): PyInstaller 打包时需要显式加入的模块名列表，用于处理动态导入的依赖。
            - 示例: ["mysql.connector.plugins.mysql_native_password", "selenium"]

    返回值：
        - 无返回值。成功后，生成 exe 及依赖文件目录到桌面。

    注意事项：
        1. 使用 PyInstaller 非 --onefile 模式，适用于依赖多、需保留资源文件的项目。
        2. 输出结构为一个含 EXE 文件及其运行依赖的文件夹。
        3. 若依赖项在运行时动态导入，需通过 `隐藏导入模块` 参数显式声明。

    使用示例：
        - 脚本路径 = "D:\\项目\\程序.py"
        - 隐藏模块 = ["mysql.connector.plugins.mysql_native_password"]
        - 封装代码_普通编译(脚本路径, 隐藏模块)
    """
    try:
        桌面路径 = os.path.join(os.path.expanduser("~"), 'Desktop')
        pyinstaller_path = os.path.join(os.path.dirname(sys.executable), 'Scripts', 'pyinstaller.exe')

        if not os.path.exists(pyinstaller_path):
            raise FileNotFoundError(f"未找到 pyinstaller，请确保它已正确安装。路径：{pyinstaller_path}")

        with tempfile.TemporaryDirectory() as 临时目录:
            命令 = [
                pyinstaller_path,
                '--distpath', 桌面路径,
                '--workpath', 临时目录,
                '--specpath', 临时目录,
            ]

            if 隐藏导入模块:
                for 模块名 in 隐藏导入模块:
                    命令.append(f'--hidden-import={模块名}')

            命令.append(脚本路径)

            subprocess.run(命令, check=True)
            print(f"✅ 打包成功：{os.path.basename(脚本路径)}（普通结构）已输出至桌面。")

    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败（PyInstaller 执行异常）：{e}")
    except FileNotFoundError as e:
        print(f"❌ 错误：{e}")
