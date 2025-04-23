import os
import json
import time
import shutil
import atexit
import psutil
from datetime import datetime

# 定义全局变量
_temp_dir = None
# 检查是否为生产环境
_is_production = os.environ.get("ENVIRONMENT", "development") == "production"


def _get_log_dirs():
    """
    获取日志主目录和临时目录的路径

    :return: 元组 (主目录路径, 临时目录路径)
    """
    # 主目录路径
    root_dir = os.path.abspath(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )
    main_log_dir = os.path.join(root_dir, "printProLog")

    # 临时目录路径（使用进程ID确保多进程安全）
    temp_dir_name = f"temp_{os.getpid()}"
    temp_log_dir = os.path.join(main_log_dir, temp_dir_name)

    return main_log_dir, temp_log_dir


def _initialize_log_dirs():
    """
    初始化日志目录，如果发现旧的临时目录则进行清理
    """
    # 如果是生产环境，不执行任何操作
    if _is_production:
        return

    global _temp_dir

    main_log_dir, temp_log_dir = _get_log_dirs()
    _temp_dir = temp_log_dir

    # 创建主日志目录（如果不存在）
    if not os.path.exists(main_log_dir):
        os.makedirs(main_log_dir)

    # 检查是否存在旧的临时目录（可能是由于上次程序异常退出导致）
    temp_parent_dir = os.path.dirname(temp_log_dir)
    if os.path.exists(temp_parent_dir):
        for item in os.listdir(temp_parent_dir):
            # 只处理temp_开头的目录
            if item.startswith("temp_") and os.path.isdir(
                os.path.join(temp_parent_dir, item)
            ):
                try:
                    # 从目录名提取进程ID
                    pid_str = item.split('_')[1]
                    pid = int(pid_str)
                    
                    # 检查进程是否仍在运行
                    if not psutil.pid_exists(pid):
                        # 进程不存在，可以安全删除临时目录
                        old_temp_dir = os.path.join(temp_parent_dir, item)
                        shutil.rmtree(old_temp_dir)
                except (IndexError, ValueError):
                    # 目录名格式不正确，不处理
                    pass
                except Exception as e:
                    print(f"清理旧临时目录时出错: {str(e)}")

    # 创建新的临时目录
    if not os.path.exists(temp_log_dir):
        os.makedirs(temp_log_dir)


def printPro(
    content,
    filename="default.txt",
    clear_on_restart=True,
    show_timestamp=False,
    line_breaks=1,
    folder=None,
    forceWrite=True,
):
    """
    将内容写入到根目录的printProLog文件夹下的指定文件中，支持多种数据类型的输出。
    在生产环境中，此函数不执行任何操作。

    :param content: 要输出的内容，可以是任意类型（字符串、字典、列表等）
    :param filename: 输出文件名，支持各种扩展名如.txt、.json、.py等。如果没有提供后缀，将自动添加.txt
    :param clear_on_restart: 是否在服务重启时清空输出文件，默认为True
    :param show_timestamp: 是否显示时间戳，默认为False
    :param line_breaks: 每条记录之间的空行数，默认为1（即一条记录后空一行）
    :param folder: 子文件夹路径，例如'block'或'block/text'，默认为None
    :param forceWrite: 是否强制使用写入模式（覆盖已有内容）。
    
    注意：clear_on_restart的优先级高于forceWrite，即如果clear_on_restart=False，即使forceWrite=True也会使用追加模式。
    
    """
    # 在生产环境中，此函数不执行任何操作
    if _is_production:
        return

    global _temp_dir

    # 确保日志目录已初始化
    if _temp_dir is None:
        _initialize_log_dirs()

    main_log_dir, temp_log_dir = _get_log_dirs()

    # 检查文件名是否包含后缀，如果不包含则添加.txt后缀
    if "." not in filename:
        filename = f"{filename}.txt"

    # 根据clear_on_restart参数决定文件的存放位置和命名
    if clear_on_restart:
        # 非持久化文件，放在临时目录中
        log_dir = temp_log_dir
        # 如果指定了folder，则在临时目录下创建相应的子文件夹
        if folder:
            log_dir = os.path.join(log_dir, folder)
        log_file = os.path.join(log_dir, filename)
    else:
        # 持久化文件，添加前缀并放在主目录中（不考虑folder参数）
        log_dir = main_log_dir
        if not filename.startswith("persistent_"):
            filename = f"persistent_{filename}"
        log_file = os.path.join(log_dir, filename)

    # 确保目录存在
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 处理不同类型的内容
    if isinstance(content, (dict, list, set)):
        try:
            # 尝试将内容格式化为JSON字符串
            output = json.dumps(content, ensure_ascii=False, indent=2)
        except:
            # 如果无法转为JSON，则直接转为字符串
            output = str(content)
    else:
        output = str(content)

    # 构建输出字符串
    formatted_output = ""

    # 添加时间戳（如果需要）
    if show_timestamp:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        formatted_output += f"[{timestamp}]\n"

    # 添加内容
    formatted_output += output

    # 添加结尾的换行
    formatted_output += "\n" * (line_breaks + 1)

    # 根据参数和文件状态选择写入模式
    # 1. 如果clear_on_restart=False，则始终使用追加模式
    # 2. 如果clear_on_restart=True，则根据forceWrite和文件初始化情况决定
    write_mode = "a"
    if clear_on_restart:
        if (
            forceWrite
            or not os.path.exists(log_file)
            or not hasattr(printPro, "_initialized_files")
        ):
            write_mode = "w"
            # 创建已初始化文件集合（如果不存在）
            if not hasattr(printPro, "_initialized_files"):
                printPro._initialized_files = set()
            # 记录此文件已被初始化
            printPro._initialized_files.add(log_file)

    # 写入文件
    with open(log_file, write_mode, encoding="utf-8") as f:
        f.write(formatted_output)


def _migrate_files(source_dir, target_dir):
    """
    将源目录中的所有文件移动到目标目录

    :param source_dir: 源目录路径
    :param target_dir: 目标目录路径
    """
    if _is_production or not os.path.exists(source_dir):
        return

    # 确保目标目录存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 首先清空目标目录中的非持久化文件（处理带时间戳文件名的情况）
    if os.path.exists(target_dir):
        for item in os.listdir(target_dir):
            # 保留持久化文件和临时目录
            if item.startswith("persistent_") or item.startswith("temp_"):
                continue

            target_path = os.path.join(target_dir, item)
            if os.path.isfile(target_path):
                try:
                    os.remove(target_path)
                except Exception as e:
                    print(f"删除目标目录文件 {target_path} 时出错: {str(e)}")
            elif os.path.isdir(target_path):
                try:
                    shutil.rmtree(target_path)
                except Exception as e:
                    print(f"删除目标目录子文件夹 {target_path} 时出错: {str(e)}")

    # 遍历源目录中的所有文件和子目录
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        target_path = os.path.join(target_dir, item)

        if os.path.isfile(source_path):
            # 如果目标目录已存在同名文件，先删除（这一步现在可能冗余，但保留以确保安全）
            if os.path.exists(target_path):
                os.remove(target_path)
            # 移动文件
            shutil.move(source_path, target_path)
        elif os.path.isdir(source_path):
            # 如果是子目录，递归处理
            _migrate_files(source_path, target_path)


def _cleanup_non_persistent_files(directory):
    """
    清理指定目录中的所有非持久化文件

    :param directory: 要清理的目录路径
    """
    if _is_production or not os.path.exists(directory):
        return

    for item in os.listdir(directory):
        # 跳过临时目录和持久化文件
        if item.startswith("temp_") or item.startswith("persistent_"):
            continue

        path = os.path.join(directory, item)
        if os.path.isfile(path):
            try:
                os.remove(path)
            except Exception as e:
                print(f"删除文件 {path} 时出错: {str(e)}")


def cleanup():
    """
    执行清理和迁移操作：
    1. 清理主目录中的非持久化文件
    2. 将临时目录中的文件移动到主目录
    3. 删除临时目录
    """
    # 在生产环境中，不执行任何操作
    if _is_production:
        return

    global _temp_dir

    # 如果临时目录未初始化，则无需清理
    if _temp_dir is None:
        return

    main_log_dir, temp_log_dir = _get_log_dirs()

    try:
        # 1. 清理主目录中的非持久化文件
        _cleanup_non_persistent_files(main_log_dir)

        # 2. 将临时目录中的文件移动到主目录
        _migrate_files(temp_log_dir, main_log_dir)

        # 3. 删除临时目录
        if os.path.exists(temp_log_dir):
            shutil.rmtree(temp_log_dir)
    except Exception as e:
        print(f"执行清理操作时出错: {str(e)}")


def clear_printpro_logs(include_persistent=False):
    """
    清空printProLog目录下的文件

    :param include_persistent: 是否包括持久化文件，默认为False
    """
    # 在生产环境中，不执行任何操作
    if _is_production:
        return

    main_log_dir, _ = _get_log_dirs()

    if os.path.exists(main_log_dir):
        try:
            if include_persistent:
                # 如果包括持久化文件，则删除整个目录并重新创建
                shutil.rmtree(main_log_dir)
                os.makedirs(main_log_dir)
            else:
                # 否则，只删除非持久化文件
                for item in os.listdir(main_log_dir):
                    # 跳过持久化文件
                    if item.startswith("persistent_"):
                        continue

                    path = os.path.join(main_log_dir, item)
                    if os.path.isfile(path):
                        os.remove(path)
                    elif os.path.isdir(path):
                        shutil.rmtree(path)
        except Exception as e:
            print(f"清空printProLog目录时出错: {str(e)}")


# 注册程序退出时的清理函数
if not _is_production:
    atexit.register(cleanup)

# 在导入模块时初始化日志目录（非生产环境）
if not _is_production:
    _initialize_log_dirs()


# 为了兼容旧版本，保留这个函数
def is_file_empty_or_old(file_path, threshold_seconds=5):
    """
    检查文件是否为空或者是否在服务重启后新建的
    (此函数保留用于兼容性，在新版中不再使用)
    """
    # 在生产环境中，始终返回True（表示文件为空或过时）
    if _is_production:
        return True

    if not os.path.exists(file_path):
        return True

    # 检查文件大小是否为0
    if os.path.getsize(file_path) == 0:
        return True

    # 检查文件最后修改时间
    current_time = time.time()
    file_mod_time = os.path.getmtime(file_path)

    return (current_time - file_mod_time) > threshold_seconds
