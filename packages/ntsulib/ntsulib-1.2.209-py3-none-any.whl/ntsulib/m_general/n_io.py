import shutil
import os
import enum
import inspect
import pathlib

__all__ = ["Auto_Mode",
           "getProjectPath",
           "getTempDir",
           "is_nuitka_packaged",
           "is_pyinstaller_packaged",
           "print_file_tree",
           "copy_file_to",
           "isEntryPoint",
           "get_real_exe_dir"]

import sys


class Auto_Mode(enum.Enum):
    disable = 0  # 禁用自动查找，仅按层级查找 会获取当前使用的py文件所在的位置
    normal = 1  # 普通模式：仅检测常规Python项目标记
    high = 2  # 高敏感模式：额外检测.venv/.idea等特殊标记
    highest = 3  # 最高敏感模式：合并normal和high的所有标记

def isEntryPoint():
    # 获取主脚本的真实路径（处理符号链接等情况）
    main_script = os.path.realpath(sys.argv[0])

    # 获取当前模块的 __file__（如果是被导入的模块）
    caller_frame = inspect.currentframe().f_back
    caller_globals = caller_frame.f_globals

    # 检查当前模块是否是 __main__ 并且文件路径匹配
    if caller_globals.get('__name__') == '__main__':
        if '__file__' in caller_globals:
            caller_file = os.path.realpath(caller_globals['__file__'])
            if caller_file == main_script:
                return True

    # 如果不是 __main__ 或者文件不匹配，则不是入口点
    return False

def get_real_exe_dir() -> str:
    """
    获取 .exe 文件的真实目录（兼容 Nuitka 深度打包）
    适用于所有情况，即使 m_sys.executable 被重定向

    返回:
        str: 规范化后的绝对路径（如 "C:\\Program Files\\MyApp"）
    """
    # 1. 尝试从 m_sys.argv[0] 获取线索（Nuitka 可能会修改它）
    exe_path = sys.argv[0]

    # 2. 如果是相对路径，尝试结合当前工作目录
    if not os.path.isabs(exe_path):
        exe_path = os.path.join(os.getcwd(), exe_path)

    # 3. 解析可能的符号链接/短路径（如 ONEFIL~1）
    exe_path = os.path.realpath(exe_path)

    # 4. 如果是临时目录（如 AppData\Local\Temp），尝试向上查找
    temp_dir = os.path.join(os.environ.get("TEMP", ""), "")
    if exe_path.startswith(temp_dir):
        # 回溯到第一个非临时目录的父级
        parent = pathlib.Path(exe_path).parent
        while str(parent).startswith(temp_dir):
            parent = parent.parent
        exe_path = str(parent)

    # 5. 最终验证
    if not os.path.exists(exe_path):
        raise RuntimeError(f"无法定位 .exe 真实路径: {exe_path}")

    return os.path.normpath(exe_path)

def getTempDir(relative_path=""):
    """
    获取资源目录路径,是缓存路径

    参数:
        relative_path: 相对于基础目录的子路径（支持正斜杠/反斜杠）
    """
    try:
        # 统一路径分隔符为系统标准
        relative_path = relative_path.replace("/", os.sep).replace("\\", os.sep)

        # 1. 处理打包环境
        if is_pyinstaller_packaged():
            base_path = sys._MEIPASS

        elif is_nuitka_packaged():
            # 通过 __file__ 定位临时目录
            main_module = sys.modules.get('__main__')
            if main_module and hasattr(main_module, '__file__'):
                base_path = os.path.dirname(os.path.abspath(main_module.__file__))
                # 验证临时目录特征
                if not ("ONEFIL" in base_path.upper() or "Temp" in base_path):
                    base_path = get_real_exe_dir()
            else:
                base_path = get_real_exe_dir()

        # 2. 普通 Python 环境
        else:
            # 直接使用 getProjectPath 的结果
            base_path = getProjectPath()

        # 拼接路径并规范化
        full_path = os.path.normpath(os.path.join(base_path, relative_path))
        return full_path

    except Exception as e:
        raise RuntimeError(f"资源路径解析失败: {e}") from e

def print_file_tree(path):
    """打印文件树结构"""
    print(f"临时目录: {path}\n")
    for root, dirs, files in os.walk(path):
        level = root.replace(str(path), "").count(os.sep)
        indent = "    " * level
        print(f"{indent}{os.path.basename(root)}/")

        sub_indent = "    " * (level + 1)
        for file in files:
            print(f"{sub_indent}{file}")

def is_nuitka_packaged() -> bool:
    """检测是否为Nuitka打包环境"""
    return "__compiled__" in globals()

def is_pyinstaller_packaged() -> bool:
    """检测是否为PyInstaller打包环境"""
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


def copy_file_to(
        becopyed_file_path: str,
        new_file_path: str,
        cover: bool = False,
        file_name: str = None,
):
    """
    Copy a file with enforced forward slashes (`/`) for cross-platform compatibility.

    Args:
        becopyed_file_path: Source path (directory or file, must use `/`)
        new_file_path: Destination path (directory or file, must use `/`)
        cover: Overwrite if destination exists
        file_name: Filename if paths are directories
    """
    # Ensure paths use forward slashes (replace any backslashes)
    becopyed_file_path = becopyed_file_path.replace("\\", "/")
    new_file_path = new_file_path.replace("\\", "/")
    # Case 1: `file_name` is provided (paths are directories)
    if file_name is not None:
        # Build full paths (still using `/`)
        src_path = f"{becopyed_file_path}/{file_name}"
        dst_path = f"{new_file_path}/{file_name}"
        # Verify source is a directory (after enforcing `/`)
        if not os.path.isdir(becopyed_file_path):
            raise ValueError(f"Source must be a directory when file_name is provided: {becopyed_file_path}")
        # Create destination directory if missing
        os.makedirs(new_file_path, exist_ok=True)

    # Case 2: `file_name` is None (paths are full file paths)
    else:
        src_path = becopyed_file_path
        dst_path = new_file_path
        # Verify paths are files (not directories)
        if os.path.isdir(src_path):
            raise ValueError(f"Source must be a file when file_name is None: {src_path}")
        if os.path.isdir(dst_path):
            raise ValueError(f"Destination must be a file when file_name is None: {dst_path}")
    # Check if source file exists
    if not os.path.isfile(src_path):
        raise FileNotFoundError(f"Source file not found: {src_path}")
    # Skip if destination exists and cover=False
    if os.path.exists(dst_path):
        if not cover:
            return
        if os.path.isdir(dst_path):
            raise ValueError(f"Destination is a directory (expected file): {dst_path}")
    # Ensure parent directory exists
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    # Copy the file (works cross-platform)
    shutil.copy2(src_path, dst_path)


# 目前支持nuitka, pyinstaller, py工程的路径获取
def getProjectPath(layer: int = 0, auto: Auto_Mode = Auto_Mode.highest) -> str:
    """
    获取项目路径（统一打包环境行为）

    参数:
        layer: 向上回溯的目录层数（0=不回溯）
        auto: 自动检测模式（打包环境下强制禁用）

    返回:
        str: 规范化后的绝对路径
        - 开发环境: 工程根目录
        - 打包环境: .exe所在目录（考虑层级回溯）

    异常:
        ValueError: 如果layer是负数
        RuntimeError: 如果路径解析失败
    """
    if layer < 0:
        raise ValueError("layer参数不能为负数")

    # ==============================================
    # 打包环境处理
    # ==============================================
    if is_pyinstaller_packaged() or is_nuitka_packaged():
        layer += 1 # 去除文件名
        base_path = get_real_exe_dir()

        # 处理层级回溯
        for _ in range(layer):
            parent = os.path.dirname(base_path)
            if parent == base_path:  # 到达根目录
                break
            base_path = parent

        return os.path.normpath(base_path)

    # ==============================================
    # 开发环境处理（Python工程文件模式）
    # ==============================================
    main_module = sys.modules.get('__main__')
    if not hasattr(main_module, '__file__'):
        raise RuntimeError("无法确定主模块路径")

    current_path = os.path.dirname(os.path.abspath(main_module.__file__))

    # 禁用自动检测模式
    if auto == Auto_Mode.disable:
        project_path = current_path
    else:
        # 项目标记检测函数
        def is_project_dir(path: str) -> bool:
            """检查给定路径是否是项目根目录"""
            normal_markers = ['pyproject.toml', '.git', 'requirements.txt']
            high_markers = ['.idea', '.venv', '.vscode']

            markers = []
            if auto.value >= Auto_Mode.normal.value:
                markers += normal_markers
            if auto.value >= Auto_Mode.high.value:
                markers += high_markers

            for marker in markers:
                target = os.path.join(path, marker)
                if os.path.exists(target):
                    if marker.startswith('.'):
                        parent_marker = os.path.join(os.path.dirname(path), marker)
                        if os.path.exists(parent_marker):
                            continue
                    return True
            return False

        # 向上查找项目根目录
        project_path = current_path
        while True:
            if is_project_dir(project_path):
                break
            parent = os.path.dirname(project_path)
            if parent == project_path:
                break
            project_path = parent

    # 处理层级回溯
    for _ in range(layer):
        parent = os.path.dirname(project_path)
        if parent == project_path:
            break
        project_path = parent

    return os.path.normpath(project_path)

def is_executable() -> bool:
    return not sys.executable.endswith('python.exe')

def is_dir_exists(path: str) -> bool:
    return os.path.isdir(path)

def is_file_exists(path: str) -> bool:
    return os.path.isfile(path)
