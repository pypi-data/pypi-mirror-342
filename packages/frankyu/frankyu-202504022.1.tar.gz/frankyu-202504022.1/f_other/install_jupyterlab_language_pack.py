import os
# 导入 os 模块，提供与操作系统交互的功能

print(20250419)

import shutil
# 导入 shutil 模块，提供高级文件操作功能

import subprocess
# 导入 subprocess 模块，用于运行外部命令

from typing import Optional, Tuple
# 从 typing 模块导入 Optional 和 Tuple 类型提示

from packaging import version as version_parser
# 从 packaging 模块导入 version 并重命名为 version_parser


def get_pip_location(default_pip_path='C:\\anaconda3\\Scripts\\pip.EXE', prefer_default_pip=0) -> Optional[str]:
    # 定义函数 get_pip_location，用于获取 pip 可执行文件的位置
    """
    获取 pip 可执行文件的位置。

    思路:
        首先检查是否优先使用用户提供的默认 pip 路径，并且该路径是否真实存在。
        如果不是，则尝试导入自定义的 `f_other.system_info` 模块并调用其获取 pip 位置的函数。
        如果导入失败，则使用 `shutil.which("pip")` 在系统环境变量中查找 pip。
        最后，如果上述方法都失败，则判断默认 pip 路径是否存在，如果存在则返回默认路径，否则返回 None。

    Args:
        default_pip_path (str): 用户提供的默认 pip 可执行文件路径。例如: "C:\\anaconda3\\Scripts\\pip.exe"。
        prefer_default_pip (bool): 一个布尔值，指示是否优先使用 `default_pip_path`。如果为 True，则优先使用 `default_pip_path`。

    Returns:
        Optional[str]: pip 可执行文件的完整路径。如果找不到 pip，则返回 None。
    """
    if prefer_default_pip and os.path.exists(default_pip_path):
        # 如果 prefer_default_pip 为 True，表示优先使用用户指定的默认 pip 路径，
        # 并且使用 os.path.exists() 检查该路径在文件系统中是否真实存在。
        return default_pip_path
        # 如果条件满足，则直接返回用户提供的默认 pip 路径。
    try:
        # 尝试导入名为 `f_other.system_info` 的自定义模块。
        # 这个模块可能包含一些特定于用户的获取系统信息的功能，包括 pip 的安装位置。
        import f_other.system_info as sys_info
        # 将导入的模块命名为 `sys_info` 以方便后续调用。
        return sys_info.get_pip_location()
        # 调用 `sys_info` 模块中的 `get_pip_location()` 函数，该函数应该返回 pip 的安装路径。
    except ImportError:
        # 如果导入 `f_other.system_info` 模块失败（例如该模块不存在），
        # 则会抛出 `ImportError` 异常，这里使用 `except` 语句捕获这个异常。
        pass
        # 使用 `pass` 表示忽略这个异常，继续执行后续的代码。这表明如果自定义方法失败，则尝试其他方法。
    # 使用 `shutil.which("pip")` 在系统的环境变量中查找名为 "pip" 的可执行文件。
    # `shutil.which()` 会返回找到的第一个匹配项的完整路径，如果找不到则返回 None。
    # 然后，使用 `or` 运算符连接 `shutil.which("pip")` 的结果和另一个条件判断。
    # 另一个条件判断是 `(default_pip_path if os.path.exists(default_pip_path) else None)`。
    # 这个条件判断首先使用 `os.path.exists(default_pip_path)` 检查默认 pip 路径是否存在。
    # 如果存在，则返回 `default_pip_path`，否则返回 None。
    # 整个 `return` 语句的逻辑是：首先尝试使用 `shutil.which("pip")` 查找，
    # 如果找不到，则检查默认路径是否存在并返回，如果默认路径也不存在，则最终返回 None。
    return shutil.which("pip") or (default_pip_path if os.path.exists(default_pip_path) else None)


import subprocess
import locale
from typing import Tuple

def execute_command(command=["ipconfig"]) -> Tuple[int, str, str]:
    """
    在 shell 中执行指定的命令，并返回其退出代码、标准输出和标准错误。
    优先尝试UTF-8解码，失败后回退到系统默认编码。

    Args:
        command (list): 要执行的命令列表，默认为 ["ipconfig"]

    Returns:
        Tuple[int, str, str]: (退出代码, 标准输出, 标准错误)
    """
    print(f"运行的命令: {' '.join(command)}")
    
    try:
        # 第一阶段：先以bytes形式捕获输出
        result = subprocess.run(
            command,
            capture_output=True,
            text=False,  # 获取bytes而非str
            check=False
        )
        
        # 解码函数（尝试UTF-8，失败则使用系统编码）
        def decode_with_fallback(byte_data):
            if not byte_data:
                return ""
            try:
                return byte_data.decode('utf-8').strip()
            except UnicodeDecodeError:
                sys_encoding = locale.getpreferredencoding()
                return byte_data.decode(sys_encoding, errors='replace').strip()
        
        # 处理输出
        stdout = decode_with_fallback(result.stdout)
        stderr = decode_with_fallback(result.stderr)
        
        print(f"命令输出 (stdout):\n{stdout}")
        print(f"命令错误 (stderr):\n{stderr}" if stderr else "命令错误 (stderr): 无")
        
        return result.returncode, stdout, stderr
        
    except Exception as e:
        print(f"执行命令时发生异常: {str(e)}")
        return -1, "", str(e)




def check_package_version(package_name=" jupyterlab-language-pack-zh-CN", mirror_url= None,pip_location=r"C:\anaconda3\Scripts\pip.exe"):
    # 定义函数 check_package_version，用于检查已安装或最新的包版本
    """
    检查指定包是否已安装，并返回其已安装的版本。可以选择性地使用镜像 URL 来检查最新的版本 (但当前逻辑只返回已安装版本)。

    思路:
        首先检查提供的包名是否为空，如果为空则直接返回 None。
        然后构建执行 `pip show <package_name>` 命令。
        如果提供了镜像 URL，则将其添加到命令参数中。
        执行命令并捕获输出。
        如果命令执行成功（退出代码为 0），则解析标准输出，查找以 "version:" 开头的行，并提取版本号。

    Args:
        pip_location (str): pip 可执行文件的路径。
        package_name (str): 要检查版本的目标包名。
        mirror_url (Optional[str], optional): 可选的 pip 镜像 URL。Defaults to None。
                                              注意：当前逻辑未使用此参数来检查最新版本，仅用于 `pip show` 命令。

    Returns:
        Optional[str]: 如果找到包且成功获取到版本信息，则返回已安装的版本号 (str)。
                       如果包未安装或获取版本信息失败，则返回 None。
    """
    if not package_name.strip():
        # 使用 `.strip()` 方法去除包名首尾的空白字符，如果结果为空字符串，
        # 说明用户没有提供有效的包名，此时直接返回 None。
        return None  # 防止包名为空

    command = [pip_location, "show", package_name]
    # 构建要执行的 pip 命令列表。
    # `pip_location` 是 pip 可执行文件的路径。
    # "show" 是 pip 的子命令，用于显示有关已安装包的信息。
    # `package_name` 是要查询的包的名称。

    if mirror_url:
        # 检查是否提供了 `mirror_url` 参数。
        # 如果提供了，说明用户可能希望从特定的镜像源获取包信息。
        pass
        #command.extend(["-i", mirror_url])
        # 使用 `extend()` 方法将 "-i" 参数和 `mirror_url` 添加到 `command` 列表中。
        # "-i" 是 pip 的选项，用于指定要使用的镜像源。

    exit_code, stdout, _ = execute_command(command)
    # 调用之前定义的 `execute_command()` 函数来执行构建好的 pip 命令。
    # `execute_command()` 返回一个包含退出代码、标准输出和标准错误信息的元组。
    # 这里我们只关心退出代码 (`exit_code`) 和标准输出 (`stdout`)，标准错误信息用 `_` 占位符表示忽略。

    if exit_code == 0:
        # 检查命令的退出代码是否为 0。
        # 在大多数情况下，退出代码为 0 表示命令执行成功。
        for line in stdout.splitlines():
            # 使用 `splitlines()` 方法将标准输出字符串分割成一个包含多行的列表，
            # 然后遍历这个列表中的每一行。
            if line.lower().startswith("version:"):
                # 对于每一行，使用 `.lower()` 方法将其转换为小写，
                # 然后使用 `startswith("version:")` 方法检查该行是否以 "version:" 开头。
                # 这通常是 pip show 命令输出中包含包版本信息的行的格式。
                return line.split(":", 1)[1].strip()
                # 如果找到以 "version:" 开头的行，则使用 `split(":", 1)` 方法将该行以 ":" 分割成两部分，
                # 第一个部分是 "version:"，第二个部分是版本号。这里的 `1` 参数表示只分割一次。
                # 然后，我们取分割后的第二个部分 (`[1]`)，并使用 `.strip()` 方法去除版本号首尾的空白字符，
                # 最后将提取到的版本号返回。

    return None
    # 如果循环结束后没有找到以 "version:" 开头的行，或者命令的退出代码不是 0，
    # 说明包可能未安装，或者获取版本信息失败，此时返回 None。


def uninstall_package(package_name="xlwings",pip_location=r"C:\anaconda3\Scripts\pip.exe" ) -> str:
    # 定义函数 uninstall_package，用于卸载指定的 Python 包
    """
    使用 pip 卸载指定的 Python 包，并返回卸载结果的字符串信息。

    思路:
        首先检查提供的包名是否为空。
        然后调用 `check_package_version` 函数检查该包是否已安装。
        如果未安装，则返回相应的提示信息。
        如果已安装，则构建执行 `pip uninstall -y <package_name>` 命令。
        执行命令并捕获输出。
        根据命令的退出代码判断卸载是否成功，并返回相应的成功或失败信息。

    Args:
        pip_location (str): pip 可执行文件的路径。
        package_name (str): 要卸载的包名。

    Returns:
        str: 卸载操作的结果信息。可能包含成功卸载的消息或者失败的错误信息。
    """
    if not package_name.strip():
        # 检查包名去除首尾空格后是否为空。如果为空，说明没有提供有效的包名，
        # 返回一个错误消息，提示用户包名不能为空。
        return "卸载失败：包名不能为空。"  # 防止包名为空

    # 检查已安装版本
    installed_version = check_package_version(pip_location, package_name)
    # 调用 `check_package_version` 函数，传入 pip 的位置和要卸载的包名，
    # 以获取该包的已安装版本。如果包未安装，`check_package_version` 将返回 None。

    if not installed_version:
        # 如果 `installed_version` 为 None，表示要卸载的包未安装。
        return f"包 {package_name} 未安装，无需卸载。"
        # 返回一个消息，告知用户该包未安装，因此无需进行卸载操作。

    # 执行卸载命令
    command = [pip_location, "uninstall", "-y", package_name]
    # 构建要执行的 pip 卸载命令列表。
    # `pip_location` 是 pip 可执行文件的路径。
    # "uninstall" 是 pip 的子命令，用于卸载包。
    # "-y" 是 pip 的选项，表示在卸载前自动确认，无需用户手动输入 "yes"。
    # `package_name` 是要卸载的包的名称。

    exit_code, _, stderr = execute_command(command)
    # 调用 `execute_command` 函数执行构建好的卸载命令。
    # 该函数返回命令的退出代码、标准输出和标准错误。
    # 我们只关心退出代码 (`exit_code`) 和标准错误 (`stderr`)，标准输出用 `_` 占位符忽略。

    if exit_code == 0:
        # 检查命令的退出代码是否为 0。
        # 在大多数情况下，退出代码为 0 表示命令执行成功，即包已成功卸载。
        return f"卸载成功：包名 {package_name}, 版本 {installed_version}"
        # 返回一个成功消息，包含卸载的包名和其卸载前的版本号。

    return f"卸载失败。错误信息:\n{stderr}"
    # 如果命令的退出代码不是 0，表示卸载失败。
    # 返回一个失败消息，并附带命令的标准错误输出，以便用户了解卸载失败的原因。


def install_package_with_version_check(
    package_name="jupyterlab-language-pack-zh-CN",
    default_pip_path: str = r"C:\anaconda3\Scripts\pip.exe",
    mirror_url=r"https://pypi.tuna.tsinghua.edu.cn/simple",
    prefer_default_pip: bool = True
) -> str:
    # 定义函数 install_package_with_version_check，用于安装指定的 Python 包并检查版本变化
    """
    安装指定的 Python 包，并在安装前后检查其版本，最后返回包含安装前后版本信息的字符串。

    思路:
        首先检查提供的包名是否为空。
        使用 `get_pip_location` 函数获取 pip 可执行文件的路径。
        如果找不到 pip，则返回错误信息。
        调用 `check_package_version` 函数获取安装前的包版本。
        构建执行 `pip install <package_name>` 命令，如果提供了镜像 URL，则将其添加到命令中。
        执行安装命令并捕获输出。
        再次调用 `check_package_version` 函数获取安装后的包版本。
        返回包含安装前和安装后版本信息的字符串。

    Args:
        package_name (str): 要安装或升级的包名。
        default_pip_path (str, optional): 默认的 pip 可执行文件路径。
                                           
        mirror_url (Optional[str], optional): 可选的 pip 镜像 URL。Defaults to None。
        prefer_default_pip (bool, optional): 是否优先使用默认 pip 路径。Defaults to True。

    Returns:
        str: 包含安装前后版本信息的字符串。格式为 "已安装版本: <旧版本>, 安装后版本: <新版本>"。
             如果包名为空或找不到 pip，则返回相应的错误信息。
    """
    if not package_name.strip():
        # 检查包名去除首尾空格后是否为空。如果为空，说明没有提供有效的包名，
        # 返回一个错误消息，提示用户包名不能为空。
        return "操作失败：包名不能为空。"  # 防止包名为空

    pip_location = get_pip_location(default_pip_path, prefer_default_pip)
    # 调用 `get_pip_location` 函数获取 pip 可执行文件的路径。
    # 该函数会根据 `default_pip_path` 和 `prefer_default_pip` 的值来确定 pip 的位置。

    if not pip_location:
        # 如果 `get_pip_location` 函数返回 None，表示没有找到 pip 可执行文件。
        return "找不到 pip 可执行文件，无法操作包。"
        # 返回一个错误消息，告知用户找不到 pip，无法进行后续的包管理操作。

    # 获取已安装版本和最新版本
    installed_version = check_package_version( package_name,None,pip_location)
    # 调用 `check_package_version` 函数获取要安装的包的当前已安装版本。
    # 如果该包尚未安装，则 `installed_version` 将为 None。

    print(f"已安装版本: {installed_version if installed_version else '未安装'}")
    # 使用 f-string 打印已安装的版本信息。
    # 如果 `installed_version` 为 None，则打印 "未安装"。

    # 安装或升级包
    command = [pip_location, "install", package_name]
    # 构建要执行的 pip 安装命令列表。
    # `pip_location` 是 pip 可执行文件的路径。
    # "install" 是 pip 的子命令，用于安装或升级包。
    # `package_name` 是要安装的包的名称。

    if mirror_url:
        # 检查是否提供了 `mirror_url` 参数。
        # 如果提供了，说明用户希望从特定的镜像源安装或升级包。
        #pass
    
        command.extend(["-i", mirror_url])
        # 使用 `extend()` 方法将 "-i" 参数和 `mirror_url` 添加到 `command` 列表中。
        # "-i" 是 pip 的选项，用于指定要使用的镜像源，可以加速包的下载。

    execute_command(command)
    # 调用之前定义的 `execute_command()` 函数来执行构建好的 pip 安装命令。
    # 该函数会执行命令并打印命令的输出和错误信息。

    # 检查安装后的版本
    new_version = check_package_version(pip_location, package_name)
    # 再次调用 `check_package_version` 函数，获取安装或升级后的包的版本。

    return f"已安装版本: {installed_version}, 安装后版本: {new_version}"
    # 使用 f-string 返回包含安装前 (`installed_version`) 和安装后 (`new_version`) 版本信息的字符串。


if __name__ == "__main__":
    # 如果当前脚本作为主程序运行（而不是被其他模块导入）
    # 测试包名
    package_name = "frankyu"
    # 设置一个用于测试的包名

    default_pip_path = r"C:\anaconda3\Scripts\pip.exe"
    # 设置默认的 pip 可执行文件路径，通常是 Anaconda 安装目录下的 Scripts 文件夹中

    # 获取 pip 路径
    pip_location = get_pip_location(default_pip_path, prefer_default_pip=True)
    # 调用 `get_pip_location` 函数获取 pip 的实际路径，这里设置优先使用默认路径

    # 测试卸载功能
    if pip_location:
        # 如果 `get_pip_location` 函数成功找到了 pip 的路径
        uninstall_result = uninstall_package(pip_location, package_name)
        # 调用 `uninstall_package` 函数尝试卸载之前设置的测试包
        print(uninstall_result)
        # 打印卸载操作的结果信息
    else:
        # 如果 `get_pip_location` 函数未能找到 pip 的路径
        print("找不到 pip 可执行文件，无法卸载包。")
        # 打印提示信息，告知用户找不到 pip，因此无法执行卸载操作