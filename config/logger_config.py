import logging
import os
from datetime import datetime

# 日志路径配置
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(root_dir, "logs")
os.makedirs(log_dir, exist_ok=True)

# 日志格式配置
log_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = os.path.join(log_dir, f"log_{log_time}.log")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=log_file,
    filemode="w",
    encoding="utf-8"
)

# 控制台输出
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # 如果需要调试脚本，把level=logging.INFO设置成logging.DEBUG即可查看全部操作


# 日志清理：最多保留 10 条
def cleanup_logs(max_logs=10):
    files = sorted(
        [f for f in os.listdir(log_dir) if f.endswith(".log")]
    )

    if len(files) > max_logs:
        remove_count = len(files) - max_logs
        old_files = files[:remove_count]  # 删除最旧的 N 个

        for f in old_files:
            os.remove(os.path.join(log_dir, f))
            print(f"[日志清理] 已删除旧日志: {f}")


cleanup_logs(max_logs=10)
