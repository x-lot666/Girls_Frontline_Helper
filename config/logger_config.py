import logging
import os
from datetime import datetime

# 参数设置
LOG_LEVEL = logging.INFO  # 控制台输出级别（如果要调试改成 logging.DEBUG）
MAX_LOG_FILES = 10  # 最多保留日志数量

# 生成日志目录与文件名
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(root_dir, "logs")
os.makedirs(log_dir, exist_ok=True)

log_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = os.path.join(log_dir, f"log_{log_time}.log")

# 本地化存储
logging.basicConfig(
    level=logging.DEBUG,  # 本地保存 DEBUG级别 日志
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=log_file,
    filemode="w",
    encoding="utf-8"
)

# 控制台输出 handler（根据 LOG_LEVEL 控制）
console = logging.StreamHandler()
console.setLevel(LOG_LEVEL)
console.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logging.getLogger().addHandler(console)


# 日志清理
def cleanup_logs(max_logs=MAX_LOG_FILES):
    files = sorted(f for f in os.listdir(log_dir) if f.endswith(".log"))
    if len(files) > max_logs:
        remove_count = len(files) - max_logs
        for old in files[:remove_count]:
            os.remove(os.path.join(log_dir, old))


cleanup_logs()
