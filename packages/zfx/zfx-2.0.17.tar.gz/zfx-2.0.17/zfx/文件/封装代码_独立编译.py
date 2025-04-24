import subprocess
import os
import sys
import tempfile


def 封装代码_独立编译(脚本路径, 隐藏导入模块=None):
    """
    将指定的 Python 脚本打包成独立 EXE 可执行文件，并输出到用户桌面。

    参数：
        - 脚本路径: 要打包的 Python 源码文件路径，例如 "D:\\项目\\主程序.py"。
        - 隐藏导入模块: 可选参数，列表形式，用于指定 PyInstaller 打包时需要手动加入的模块依赖。
            - 举例：["mysql.connector", "selenium", "zfx.mysql"]
            - 适用于：某些模块在运行时动态导入，PyInstaller 静态分析时无法识别，会导致运行报错。

    返回值：
        - 无返回值。打包成功后，EXE 文件将保存在桌面上。

    注意事项：
        1. 本函数使用 PyInstaller 将 Python 脚本封装为独立的 .exe 文件，适用于部署和分享。
        2. 打包依赖 PyInstaller 工具，请确保已通过 pip 安装。
        3. 默认打包为单文件模式（--onefile），工作目录与临时文件将自动清理。
        4. 如果脚本依赖的模块被封装在函数或自定义模块中，请使用 `隐藏导入模块` 参数显式声明。

    使用示例：
        - 脚本路径 = "D:\\项目\\任务执行器.py"
        - 隐藏依赖 = ["mysql.connector", "selenium"]
        - 封装代码_独立编译(脚本路径, 隐藏依赖)

    成功后将输出至用户桌面，例如：
        C:\\Users\\你的用户名\\Desktop\\任务执行器.exe
    """
    try:
        桌面路径 = os.path.join(os.path.expanduser("~"), 'Desktop')
        pyinstaller_path = os.path.join(os.path.dirname(sys.executable), 'Scripts', 'pyinstaller.exe')

        if not os.path.isfile(pyinstaller_path):
            raise FileNotFoundError("未找到 pyinstaller.exe，请确认已正确安装 PyInstaller。")

        with tempfile.TemporaryDirectory() as 临时目录:
            命令 = [
                pyinstaller_path,
                '--onefile',
                '--distpath', 桌面路径,
                '--workpath', 临时目录,
                '--specpath', 临时目录
            ]

            if 隐藏导入模块:
                for 模块名 in 隐藏导入模块:
                    命令.append(f'--hidden-import={模块名}')

            命令.append(脚本路径)

            subprocess.run(命令, check=True)
            print(f"✅ 打包成功：{os.path.basename(脚本路径)} 已输出至桌面。")

    except subprocess.CalledProcessError as e:
        print(f"❌ 打包出错（PyInstaller 执行失败）：{e}")
    except FileNotFoundError as e:
        print(f"❌ 错误：{e}")