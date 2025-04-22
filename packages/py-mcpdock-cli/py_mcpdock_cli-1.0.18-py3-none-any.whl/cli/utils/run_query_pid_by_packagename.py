"""
Utility to query if a process with a specific package name is running by checking its PID.
"""
import os

from cli.utils.logger import verbose
from ..utils.process_utils import read_pid_file


def query_pid_by_packagename(package_names: list) -> dict:
    """
    检查指定包名的进程是否存在于PID文件中。

    参数：
        package_names (list): 要查询的包名列表。

    返回：
        dict: 包含每个包名的运行状态的字典，格式为 {package_name: is_running}。
    """
    try:
        # 如果输入的是字符串，转换为列表以保持向后兼容
        if isinstance(package_names, str):
            package_names = [package_names]

        results = {}
        pid_data = read_pid_file()

        if not pid_data:
            verbose(f"未找到任何 PID 文件记录")
            # 如果PID文件不存在，所有包名均返回False
            for package_name in package_names:
                results[package_name] = False
            return results

        # 检查每个包名的状态
        for package_name in package_names:
            is_running = False

            # 直接检查包名是否存在于 PID 数据中
            if package_name in pid_data and pid_data[package_name]:
                verbose(f"包名 '{package_name}' 的进程存在于PID文件中")
                is_running = True
            else:
                # 尝试部分匹配
                for server_name, entries in pid_data.items():
                    if package_name in server_name and entries:
                        verbose(f"包名 '{package_name}' 匹配服务器 '{server_name}' 存在于PID文件中")
                        is_running = True
                        break

                if not is_running:
                    verbose(f"未找到包名 '{package_name}' 的进程")

            # 存储该包名的运行状态
            results[package_name] = is_running

        return results
    except Exception as e:
        package_names_str = "', '".join(package_names)
        verbose(f"查询包名 '{package_names_str}' 的进程时出错: {e}")
        # 发生异常时，所有包名均返回False
        return {package_name: False for package_name in package_names}
