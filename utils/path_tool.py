# 为整个项目提供统一的文件路径

from pathlib import Path


def get_project_root() -> str:
    '''
    获取项目根目录
    '''
    # Path(__file__)是当前文件路径
    # .parent是所在目录(utils)
    # .parent.parent是项目根目录
    return str(Path(__file__).parent.parent)


def get_abs_path(relative_path: str) -> str:
    '''
    通过相对路径返回绝对路径

    Args:
        relative_path: 相对于项目根目录的路径

    Returns:
        完整的绝对路径
    '''
    return str(Path(get_project_root()) / relative_path)


if __name__ == '__main__':
    # 测试代码仅在直接运行此文件时执行
    print(get_project_root())
    print(get_abs_path('utils/path_tool.py'))
