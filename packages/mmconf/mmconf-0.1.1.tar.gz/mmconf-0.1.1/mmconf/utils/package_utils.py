# Copyright (c) OpenMMLab. All rights reserved.
import os.path as osp
import subprocess
import importlib.util
import importlib.metadata
import sys
from types import ModuleType


def is_installed(package: str) -> bool:
    """Check if a package is installed without using pkg_resources

    检查逻辑：
    1. 优先检查sys.modules（已加载的模块）
    2. 使用importlib.util.find_spec查找模块规格
    3. 处理命名空间包（spec.origin可能为None的情况）
    """
    # 快速检查已加载的模块
    if package in sys.modules:
        return isinstance(sys.modules[package], ModuleType)

    # 查找模块规格
    spec = importlib.util.find_spec(package)

    # 处理不同情况的模块存在性
    if spec is None:
        return False  # 模块不存在
    if spec.origin:  # 标准文件/目录模块
        return True
    # 处理命名空间包（PEP 420）
    if hasattr(spec.loader, 'is_package') and spec.loader.is_package(package):
        return True
    return False


def get_installed_path(package: str) -> str:
    """Get installed path of package (pure standard library implementation)

    Args:
        package (str): Name of package (e.g. 'mmcls', 'mmcv-full')
    """
    # 优先通过importlib.metadata获取已安装包信息
    try:
        dist = importlib.metadata.distribution(package)
        pkg_location = dist.path  # type: ignore[attr-defined]  # Python 3.10+

        # 尝试直接使用包名作为模块目录
        possible_path = osp.join(pkg_location, package)
        if osp.exists(possible_path):
            return possible_path

        # 处理包名与模块名不一致的情况（如mmcv-full -> mmcv）
        module_name = package2module(package)
        module_path = osp.join(pkg_location, module_name)
        if osp.exists(module_path):
            return module_path

        # 最后尝试通过模块导入确认（处理命名空间包等特殊情况）
        spec = importlib.util.find_spec(module_name)
        if spec and spec.origin:
            return osp.dirname(spec.origin)

        raise FileNotFoundError(f"Module directory not found for {package}")

    except importlib.metadata.PackageNotFoundError:
        # 处理未安装但在PYTHONPATH中的包
        spec = importlib.util.find_spec(package)
        if spec and spec.origin:
            return osp.dirname(spec.origin)
        if spec and spec.submodule_search_locations:  # 命名空间包处理
            raise RuntimeError(
                f'{package} is a namespace package, which is not supported')
        raise FileNotFoundError(f"Package {package} not found")


def package2module(package: str) -> str:
    """Infer module name from package (pure standard library implementation)

    Args:
        package (str): Package name to infer module name (e.g. 'mmcv-full', 'numpy')

    Raises:
        ValueError: When top_level.txt not found or empty

    Example:
        >>> package2module('mmcv-full')
        'mmcv'
    """
    try:
        # 获取包的安装目录（兼容wheel/egg格式）
        dist = importlib.metadata.distribution(package)
        pkg_path = dist.path  # type: ignore[attr-defined]  # Python 3.10+

        # 标准wheel格式的top_level.txt路径
        top_level_path = osp.join(
            pkg_path,
            f"{dist.metadata['Name']}-{dist.version}.dist-info",  # type: ignore[attr-defined]
            'top_level.txt'
        )

        # 兼容旧版egg格式（虽然已不推荐，但保留兼容性）
        if not osp.exists(top_level_path):
            top_level_path = osp.join(pkg_path, 'EGG-INFO', 'top_level.txt')

        if not osp.exists(top_level_path):
            raise FileNotFoundError

        # 读取并解析top_level.txt（遵循PEP 345规范）
        with open(top_level_path, encoding='utf-8') as f:
            module_name = f.readline().strip()

        if not module_name:
            raise ValueError("top_level.txt is empty")

        return module_name

    except (importlib.metadata.PackageNotFoundError, FileNotFoundError):
        raise ValueError(f"Can not infer module name of {package} (top_level.txt not found)")
    except Exception as e:
        raise ValueError(f"Error reading top_level.txt: {str(e)}")


def call_command(cmd: list) -> None:
    try:
        subprocess.check_call(cmd)
    except Exception as e:
        raise e  # type: ignore


def install_package(package: str):
    if not is_installed(package):
        call_command(['python', '-m', 'pip', 'install', package])
