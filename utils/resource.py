from pathlib import Path

# 项目根目录 = 当前文件(utils/resource.py)往上两层
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 默认资源子目录,可以在外部修改
RESOURCE_SUBDIR = "common"


def set_resource_subdir(subdir_name):
    """
    设置资源子目录名称,例如 'new_folder'
    用法: set_resource_subdir("new_folder")
    """
    global RESOURCE_SUBDIR
    RESOURCE_SUBDIR = subdir_name


# 通用资源路径函数
def IMG(name):
    """
    获取指定资源子目录下的图片路径
    用法: IMG("example.png")
    """
    filename = name if Path(name).suffix else name + ".png"
    return str(PROJECT_ROOT / "assets" / RESOURCE_SUBDIR / filename)


# 所用的资源图片路径
# COMMON_IMG = lambda name: f"assets/common/{name}.png"

def COMMON_IMG(name):
    """
    获取 common 文件夹下指定图片的完整路径
    用法: COMMON_IMG_PATH("example.png")
    """
    filename = name if Path(name).suffix else name + ".png"
    return str(PROJECT_ROOT / "assets" / "common" / filename)

